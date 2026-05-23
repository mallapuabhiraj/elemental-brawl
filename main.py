import random
import os
os.system("color")
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Black magic
fire = Spell("Fire", 10, 1000, "Black")
thunder = Spell("Thunder", 12, 1200, "Black")
blizzard = Spell("Blizzard", 14, 1400, "Black")
meteor = Spell("Meteor", 16, 1600, "Black")
quake = Spell("Quake", 20, 2000, "Black")

# Create White magic
cure = Spell("Cure", 12, 1200, "White")
cura = Spell("Cura", 40, 4000, "White")

# Inventory
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 150 HP", 150)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP for one party member", 2500)
hielixir = Item("MegaElixir", "elixir", "Fully restores HP/MP for all party members", 2500)
grenade = Item("Grenade", "attack", "Deals 500 damage", 5000)

# Spells
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, quake, cura]

# Inventory Items
player_items = [{"item": potion, "quantity": 5},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 5},
                {"item": grenade, "quantity": 5}]

# Initialize Players (FIXED: player1 atk from 30300 to 300)
player1 = Person("Valos  :", 3000, 125, 300, 80, player_spells, player_items)
player2 = Person("Abhi   :", 4000, 150, 300, 100, player_spells, player_items)
player3 = Person("Raj    :", 3500, 140, 300, 90, player_spells, player_items)

# Initialize Enemies
enemy1 = Person("Dragon  ", 15000, 85, 300, 250, enemy_spells, [])
enemy2 = Person("Reek    ", 1250, 512, 300, 200, enemy_spells, [])
enemy3 = Person("Reek-II ", 1250, 512, 300, 200, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=======================")
    print(bcolors.BOLD + bcolors.HEADER + bcolors.WARNING + "  NAME                       HP                                   MP" + bcolors.ENDC)

    # Stats
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose an action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy_idx = player.choose_target(enemies)
            enemies[enemy_idx].take_damage(dmg)
            print("You attacked " + enemies[enemy_idx].name.replace(" ", "") + " for", dmg, "points of damage")

            if enemies[enemy_idx].get_hp() == 0:
                print(enemies[enemy_idx].name, "has died.")
                del enemies[enemy_idx]
            if len(enemies) == 0:
                print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                running = False

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("     Choose a magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)
            if spell.type == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + str(spell.name) + " heals for " + str(magic_dmg) + bcolors.ENDC)
            elif spell.type == "Black":
                enemy_idx = player.choose_target(enemies)
                enemies[enemy_idx].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n", spell.name, "deals", str(magic_dmg), "points of damage to " + enemies[enemy_idx].name + bcolors.ENDC)

                if enemies[enemy_idx].get_hp() == 0:
                    print(enemies[enemy_idx].name.replace(" ", ""), "has died.")
                    del enemies[enemy_idx]
                    if len(enemies) == 0:
                        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                        running = False

        elif index == 2:
            player.choose_item()
            item_choice = int(input("     Choose an item: ")) - 1

            if item_choice == -1:
                continue

            item = player.item[item_choice]["item"]

            # FIX: Check quantity BEFORE using (was checking == -1 after decrement)
            if player.item[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n Not Enough potions \n" + bcolors.ENDC)
                continue

            player.item[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKBLUE + "\n" + str(item.name), "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for p in players:
                        p.hp = p.maxhp
                        p.mp = p.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKBLUE + "\n" + str(item.name), "fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy_idx = player.choose_target(enemies)
                enemies[enemy_idx].take_damage(item.prop)
                print(bcolors.FAIL, "\n", item.name, "deals", str(item.prop), "points of damage to ", enemies[enemy_idx].name + bcolors.ENDC)

                if enemies[enemy_idx].get_hp() == 0:
                    print(enemies[enemy_idx].name.replace(" ", ""), " has died.")
                    del enemies[enemy_idx]
                if len(enemies) == 0:
                    print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                    running = False

    # Enemy Attack phase
    for enemy in enemies:
        enemy_choice = random.randint(0, 1)
        # Enemy Attack
        if enemy_choice == 0:
            target = random.randint(0, len(players) - 1)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name, "attacks", players[target].name, "for", enemy_dmg)
            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", ""), " has died.")
                del players[target]
                if len(players) == 0:
                    print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
                    running = False
        # Enemy Magic
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            # FIX: Fallback to attack if no MP for spells
            if spell is None:
                target = random.randint(0, len(players) - 1)
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)
                print(enemy.name, "attacks", players[target].name, "for", enemy_dmg)
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", ""), " has died.")
                    del players[target]
                    if len(players) == 0:
                        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
                        running = False
                continue

            enemy.reduce_mp(spell.cost)
            if spell.type == "White":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n", enemy.name.replace(" ", ""), "chose", str(spell.name) + " heals for " + str(magic_dmg) + bcolors.ENDC)
            elif spell.type == "Black":
                target = random.randint(0, len(players) - 1)
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + "\n", enemy.name.replace(" ", "") + "'s", spell.name, "deals", str(magic_dmg), "points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", ""), " has died.")
                    del players[target]
                    if len(players) == 0:
                        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
                        running = False

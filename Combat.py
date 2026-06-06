import math, time
import random
from itertools import zip_longest
import requests
import Character
import Enemy

class Combat:
    def __init__(self, teamMembers, enemyMembers):
        self.team = teamMembers
        self.enemies = enemyMembers
    
    def start_combat(self):
        combatants = self.team + self.enemies # concat two lists
        combatants.sort(key=lambda x: self.calculate_initiative(x), reverse=True) # sort by speed, highest first, to get turn order
        print("\nTurn order:")
        for unit in combatants:
            print(unit.get_name())
        time.sleep(1)
        if not isinstance(combatants[0], Character.Character): # display combatants before enemies attack
            print("\nCombat report:")
            size = max(len(self.enemies), len(self.team))
            for position, enemy, teamMember in zip_longest(range(1,size+1), self.enemies, self.team, fillvalue=''):
                if teamMember == '' and enemy != '':
                    print(f"{position}: {enemy.get_name()} - {enemy.get_hp()}HP")
                elif teamMember != '' and enemy == '':
                    print(f"                                    {teamMember.get_name()} - {teamMember.get_hp()}HP")
                else:
                    print(f"{position}: {enemy.get_name()} - {enemy.get_hp()}HP                   {teamMember.get_name()} - {teamMember.get_hp()}HP")
        while True:
            for combatant in combatants:
                if isinstance(combatant, Enemy.Enemy): # enemy turn
                    if not combatant.is_alive(): # killed, no turn
                        continue
                    if not self.team:
                        return self.make_result(False) # all team members dead
                    # enemy attacks random team member
                    target = random.choice(list(self.team)) # gets a Character from the Party
                    hit_result = self.calculate_hit(combatant, target)
                    if hit_result[0]: # if successful attack roll... (True, ...)
                        combatant.attack(target, self.calculate_damage(combatant, target, hit_result[1])) # roll damage, pass in 1 for crit20 and 0 otherwise
                        if not target.is_alive(): # killed its target, remove from combat
                            self.team.remove(target)
                    elif not hit_result[0] and hit_result[1] != 1:
                        print(f"\n{combatant.get_name()} missed their attack on {target.get_name()}.")    
                
                else: # team member turn
                    if not combatant.is_alive():
                        continue
                    if not self.enemies:
                        return self.make_result(True) # all enemies dead
                    # player can choose an enemy to attack
                    print("\nCombat report:")
                    size = max(len(self.enemies), len(self.team))
                    for position, enemy, teamMember in zip_longest(range(1,size+1), self.enemies, self.team, fillvalue=''):
                        if teamMember == '' and enemy != '':
                            print(f"{position}: {enemy.get_name()} - {enemy.get_hp()}HP")
                        elif teamMember != '' and enemy == '':
                            print(f"                                    {teamMember.get_name()} - {teamMember.get_hp()}HP")
                        else:
                            print(f"{position}: {enemy.get_name()} - {enemy.get_hp()}HP                   {teamMember.get_name()} - {teamMember.get_hp()}HP")

                    print(f"\n{combatant.get_name()}'s turn! Choose an enemy to attack (enter the number):")
                    
                    while True:
                        choice = 0
                        try:
                            choice = int(input("> ").strip())
                            if choice <= len(list(self.enemies)) and choice > 0: # check both conditions here
                                break
                            else:
                                print("Invalid choice. Please select a new enemy with the numbers on the left.\n") # input is int but invalid
                        except:
                            print("Invalid choice. Please select a new enemy with the numbers on the left.\n") # input is not int
                    
                    target = list(self.enemies)[choice-1] # pick the Enemy object
                    hit_result = self.calculate_hit(combatant, target)
                    if hit_result[0]: # if successful attack roll... (True, ...)
                        combatant.attack(target, self.calculate_damage(combatant, target, hit_result[1])) # roll damage, pass in 1 for crit20 and 0 otherwise
                        if not target.is_alive(): # killed its target, remove from combat
                            self.enemies.remove(target)
                    elif not hit_result[0] and hit_result[1] != 1: # non-critical miss, display this message instead of crit miss message
                        print(f"\n{combatant.get_name()} missed their attack on {target.get_name()}.")

                    
            if not self.team:
                print("Your party has been defeated! Game over.")
                return False
            elif not self.enemies:
                print("You have defeated all enemies! Victory!")
                return True
    
    def calculate_hit(self, combatant, enemy): # combatant rolling the hit
        d20 = random.randint(1,20)
        if d20 == 1:
            print(f"\n{combatant.get_name()} critically missed!")
            return (False, 1) # 1 means crit, True means hit
        elif d20 == 20:
            return (True, 1) # True represents hit landing
        if isinstance(combatant, Enemy.Enemy): # enemy trying to hit party member PROFICIENCY TBD
            # look for ability bonus - determine type of weapon
            if combatant.get_weapon() != None: # unarmed, use strength for physical
                desiredStat = 'strength'
            else:
                wpnRange = combatant.get_weapon()['weapon_range'].lower() # melee or ranged
                if wpnRange == 'melee':
                    desiredStat = "strength"
                else:
                    desiredStat = "dexterity"
            url = f"https://www.dnd5eapi.co/api/2014/monsters/{combatant.get_type().lower()}"
            response = requests.get(url)
            monsterData = response.json()
            bonus = math.floor((monsterData[desiredStat] - 10) / 2) # bonus to add or subtract
            return ((d20 + bonus >= enemy.get_AC()), 0) # True if hit >= AC, false otherwise
        else: # party member trying to hit enemy PROFICIENCY TBD
            # ability bonus TBD for characters
            return ((d20 >= enemy.get_AC()),0) # True if hit >= AC, false otherwise, no crit
        
    def calculate_damage(self, combatant, enemy, crit): # return int for damage
        dmg = 0
        weapon = combatant.get_weapon()
        if weapon is not None:
            dmg = weapon['damage']['damage_dice'] # this is a string like "2d6", so we need to parse it
            dmg = dmg.split('d') # split into number of dice and sides
            numDice = int(dmg[0])
            if crit == 1:
                numDice *= 2 # double dice rolled in a crit
            bonusDmg = 0
            if "+" in dmg[1]: # some weapons have a bonus damage, so check for that too
                dmg[1] = dmg[1].split('+')[0] # make the bonus 2 for all weapons, simplicity
                bonusDmg = 2
            sides = int(dmg[1])
            totalDmg = 0
            for _ in range(numDice):
                totalDmg += random.randint(1, sides) # roll the dice once to determine dmg for the fight, simplified
            dmg = totalDmg + bonusDmg
            # now to add ability bonus dmg, if possible
            
            if isinstance(combatant, Character.Character):
                wpnRange = weapon['weapon_range'].lower() # melee or ranged (or magic tbd)
                if wpnRange == 'melee':
                    desiredStat = "str"
                else:
                    desiredStat = "dex"
                url = f"https://www.dnd5eapi.co/api/2014/races/{combatant.get_race()}"
                response = requests.get(url)
                raceData = response.json()
                for bonus in raceData['ability_bonuses']:
                    if bonus['ability_score']['index'] == desiredStat:
                        dmg += bonus['bonus'] # add the bonus if it matches
                        break
                dmg = max(1, dmg)
            else: # enemy bonus:
                if combatant.get_weapon() != None: # unarmed, use strength for physical
                    desiredStat = 'strength'
                else:
                    wpnRange = combatant.get_weapon()['weapon_range'].lower() # melee or ranged
                    if wpnRange == 'melee':
                        desiredStat = "strength"
                    else:
                        desiredStat = "dexterity"
                url = f"https://www.dnd5eapi.co/api/2014/monsters/{combatant.get_type().lower()}"
                response = requests.get(url)
                monsterData = response.json()
                bonus = math.floor((monsterData[desiredStat] - 10) / 2) # bonus to add or subtract
                dmg += bonus
                dmg = max(1, dmg)
        else: # unarmed, weapon == None
            bonusDmg = 0 # no str bonus by default
            if isinstance(combatant, Character.Character):
                url = f"https://www.dnd5eapi.co/api/2014/races/{combatant.get_race()}"
                response = requests.get(url)
                raceData = response.json()
                for bonus in raceData['ability_bonuses']:
                    if bonus['ability_score']['index'] == "str":
                        bonusDmg = bonus['bonus'] # add the bonus if it matches strength for unarmed attack
                        break
            else:
                url = f"https://www.dnd5eapi.co/api/2014/monsters/{combatant.get_type().lower()}"
                response = requests.get(url)
                monsterData = response.json()
                bonusDmg = math.floor((monsterData["strength"] - 10) / 2) # bonus to add or subtract
            dmg = max(0,1 + bonusDmg) # default unarmed dmg, can be changed later with better weapons
            print(f"\n{combatant.get_name()} is unarmed but hits {enemy.get_name()} for {dmg} damage!")
            return dmg
        if crit:
            print(f"\n{combatant.get_name()} landed a critical hit on {enemy.get_name()} with their {combatant.get_weapon()['name']} for {dmg} damage!")
        else:
            print(f"\n{combatant.get_name()} hits {enemy.get_name()} with their {combatant.get_weapon()['name']} for {dmg} damage!")
        return dmg
    
    def calculate_initiative(self, combatant): # Enemy or Character arg
        d20 = random.randint(1,20)
        if isinstance(combatant, Enemy.Enemy): # enemy initiative
            url = f"https://www.dnd5eapi.co/api/2014/monsters/{combatant.get_type().lower()}"
            response = requests.get(url)
            monsterData = response.json()
            bonus = math.floor((monsterData["dexterity"] - 10) / 2) # bonus to add or subtract
            return (d20 + bonus) # initiative value for the combat
        else:
            # ability bonus TBD for characters
            return d20

    
    def make_result(self, win):
            if not win:
                print("Your party has been defeated! Game over.")
                return False
            else:
                print("You have defeated all enemies! Victory!")
                return True
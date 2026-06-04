import math
import random

import requests
import Character
import Enemy

class Combat:
    def __init__(self, teamMembers, enemyMembers):
        team_dict = {}
        enemy_dict = {}
        for member in teamMembers:
            team_dict[member] = member.get_speed()
        for enemy in enemyMembers:
            enemy_dict[enemy] = enemy.get_speed()
        self.team = team_dict
        self.enemies = enemy_dict
    
    def start_combat(self):
        combatants = list(self.team.keys()) + list(self.enemies.keys())
        combatants.sort(key=lambda x: x.get_speed(), reverse=True) # sort by speed, highest first, to get turn order
        print("\nCombat starts!")
        while True:
            for combatant in combatants:
                if isinstance(combatant, Enemy.Enemy): # enemy turn
                    if not combatant.is_alive(): # killed, no turn
                        continue
                    if not self.team:
                        return self.make_result(False) # all team members dead
                    # enemy attacks random team member
                    target = random.choice(list(self.team.keys())) # gets a Character from the Party
                    hit_result = self.calculate_hit(combatant, target)
                    if hit_result[0]: # if successful attack roll... (True, ...)
                        combatant.attack(target, self.calculate_damage(combatant, target, hit_result[1])) # roll damage, pass in 1 for crit20 and 0 otherwise
                        if not target.is_alive(): # killed its target, remove from combat
                            del self.team[target]
                    else:
                        print(f"{combatant.get_name()} missed their attack on {target.get_name()}.\n")
                else: # team member turn
                    if not combatant.is_alive():
                        continue
                    if not self.enemies:
                        return self.make_result(True) # all enemies dead
                    # player can choose an enemy to attack
                    print("Enemy list:")
                    for i in range(len(self.enemies)):
                        enemy = list(self.enemies.keys())[i]
                        print(f"{i+1} - {enemy.get_name()} - HP: {enemy.get_hp()}")

                    print(f"\n{combatant.get_name()}'s turn! Choose an enemy to attack (enter the number):")
                    while True:
                        choice = int(input("> ").strip())
                        if choice <= len(list(self.enemies.keys())) and choice > 0:
                            break
                        else:
                            print("Invalid choice. Please select a new enemy.\n")
                    target = list(self.enemies.keys())[choice-1] # pick the Enemy object
                    hit_result = self.calculate_hit(combatant, target)
                    if hit_result[0]: # if successful attack roll... (True, ...)
                        combatant.attack(target, self.calculate_damage(combatant, target, hit_result[1])) # roll damage, pass in 1 for crit20 and 0 otherwise
                        if not target.is_alive(): # killed its target, remove from combat
                            del self.enemies[target]
                    else:
                        print(f"{combatant.get_name()} missed their attack on {target.get_name()}.\n")

                    
            if not self.team:
                print("Your party has been defeated! Game over.")
                return False
            elif not self.enemies:
                print("You have defeated all enemies! Victory!")
                return True
    
    def calculate_hit(self, combatant, enemy): # combatant rolling the hit
        if isinstance(combatant, Enemy.Enemy): # enemy trying to hit party member PROFICIENCY TBD
            d20 = random.randint(1,20)
            if d20 == 1:
                return (False, 0) # 0 represents not-crit-20, 1 means crit for double dmg dice
            elif d20 == 20:
                print(f"{combatant.get_name()} landed a critical hit!")
                return (True, 1) # True represents hit landing
            # not a crit:
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
            #print(f"ENEMY {combatant.get_name()} HIT: {d20 + bonus} vs {enemy.get_AC()} AC")
            return ((d20 + bonus >= enemy.get_AC()), 0) # True if hit >= AC, false otherwise
        else: # party member trying to hit enemy PROFICIENCY TBD
            d20 = random.randint(1,20)
            if d20 == 1:
                return (False,0)
            elif d20 == 20:
                return (True,1)
            # not a crit:
            # ability bonus TBD for characters
            #print(f"FRIENDLY {combatant.get_name()} HIT: {d20} vs {enemy.get_AC()} AC")
            return ((d20 >= enemy.get_AC()),0) # True if hit >= AC, false otherwise, no crit
        
    def calculate_damage(self, combatant, enemy, crit): # return int for damage
        dmg = 0
        weapon = combatant.get_weapon()
        if weapon != None:
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
        else: # unarmed
            dmg = 1 # default unarmed dmg, can be changed later with better weapons
        print(f"{combatant.get_name()} has hit {enemy.get_name()} for {dmg} damage!")
        return dmg
    
    def make_result(self, win):
            if not win:
                print("Your party has been defeated! Game over.")
                return False
            else:
                print("You have defeated all enemies! Victory!")
                return True
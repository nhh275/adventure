import random

import requests
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
                    combatant.attack(target) # monsters always have the same damage
                    
                    if not target.is_alive(): # killed its target, remove from combat
                        del self.team[target]
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
                    choice = int(input("> ").strip())
                    target = list(self.enemies.keys())[choice-1] # pick the Enemy object
                    combatant.attack(target, self.calculate_damage(combatant)) # roll damage
                    if not target.is_alive(): # killed its target, remove from combat
                        del self.enemies[target]
                    
            if not self.team:
                print("Your party has been defeated! Game over.")
                return False
            elif not self.enemies:
                print("You have defeated all enemies! Victory!")
                return True
    
    def calculate_damage(self, combatant): # return int for damage
        dmg = None
        for item in combatant.equipment:
            url = f"https://www.dnd5eapi.co/api/2014/equipment/{item['index']}"
            response = requests.get(url)
            itemData = response.json()
            if 'damage' in itemData: # check if the equipment has a damage attribute (it can be used as a weapon)
                dmg = itemData['damage']['damage_dice'] # this is a string like "2d6", so we need to parse it
                dmg = dmg.split('d') # split into number of dice and sides
                numDice = int(dmg[0])
                bonusDmg = 0
                if "+" in dmg[1]: # some monsters have a bonus damage, so check for that too
                    dmg[1] = dmg[1].split('+')[0] # make the bonus 2 for all weapons, simplicity
                    bonusDmg = 2
                sides = int(dmg[1])
                totalDmg = 0
                for _ in range(numDice):
                    totalDmg += random.randint(1, sides) # roll the dice once to determine dmg for the fight, simplified
                dmg = totalDmg + bonusDmg

                break # just use the first weapon we find for simplicity
        # no weapon found, set default dmg
        if not dmg:
            dmg = 1 # default unarmed dmg, can be changed later with better weapons
        return dmg
    
    def make_result(self, win):
            if not win:
                print("Your party has been defeated! Game over.")
                return False
            else:
                print("You have defeated all enemies! Victory!")
                return True
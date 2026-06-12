import math, time
import random
from itertools import zip_longest
import requests
import Character
import Enemy

class Combat:
    def __init__(self, teamMembers, enemyMembers): # lists of party members + enemies
        self.team = teamMembers
        self.enemies = enemyMembers
    
    def start_combat(self):
        combatants = self.team + self.enemies # concat two lists
        combatants.sort(key=lambda x: self.calculate_initiative(x), reverse=True) # sort by speed, highest first, to get turn order
        currentCombatantCount = len(combatants)
        print("\nTurn order:")
        for unit in combatants:
            print(unit.name)
        time.sleep(1)
        if not isinstance(combatants[0], Character.Character): # display combatants before enemies attack
            print("\nCombat report:")
            size = max(len(self.enemies), len(self.team))
            for position, enemy, teamMember in zip_longest(range(1,size+1), self.enemies, self.team, fillvalue=''):
                if teamMember == '' and enemy != '':
                    print(f"{position}) {enemy.name} - {enemy.hp}HP")
                elif teamMember != '' and enemy == '':
                    print(f"                                    {teamMember.name} - {teamMember.hp}HP")
                else:
                    print(f"{position}) {enemy.name} - {enemy.hp}HP                   {teamMember.name} - {teamMember.hp}HP")
        turn = 1
        while True: # combat loop
            print(f"\n                      Turn {turn}")
            new_combatants = [] # each turn, update combatants list if any died
            for i in range(len(combatants)):
                if combatants[i].alive:
                    new_combatants.append(combatants[i])
            for combatant in combatants:
                if len(combatants) != currentCombatantCount:
                    print("\nUpdated turn order:")
                    for unit in combatants:
                        print(unit.name)
                    currentCombatantCount = len(combatants)
                    
                if isinstance(combatant, Enemy.Enemy): # enemy turn
                    if not combatant.alive: # killed, no turn
                        continue
                    if not self.team:
                        return self.make_result(False) # all team members dead
                    # enemy attacks random team member
                    target = random.choice(list(self.team)) # gets a Character from the Party
                    hit_result = self.calculate_hit(combatant, target)
                    if hit_result[0]: # if successful attack roll... (True, ...)
                        combatant.attack(target, self.calculate_damage(combatant, target, hit_result[1])) # roll damage, pass in 1 for crit20 and 0 otherwise
                        if not target.alive: # killed its target, remove from combat
                            self.team.remove(target)
                    elif not hit_result[0] and hit_result[1] != 1:
                        print(f"\n{combatant.name} missed their attack on {target.name}.")    
                
                else: # team member turn
                    if not combatant.alive:
                        continue
                    if not self.enemies:
                        return self.make_result(True) # all enemies dead
                    # player can choose an enemy to attack
                    print("\nCombat report:")
                    size = max(len(self.enemies), len(self.team))
                    for position, enemy, teamMember in zip_longest(range(1,size+1), self.enemies, self.team, fillvalue=''):
                        if teamMember == '' and enemy != '':
                            print(f"{position}) {enemy.name} - {enemy.hp}HP")
                        elif teamMember != '' and enemy == '':
                            print(f"                                    {teamMember.name} - {teamMember.hp}HP")
                        else:
                            print(f"{position}) {enemy.name} - {enemy.hp}HP                   {teamMember.name} - {teamMember.hp}HP")

                    print(f"\n{combatant.name}, which weapon do you want to use this turn?")
                    combatant.choose_weapon()
                    print(f"Choose an enemy to attack (enter the number):")
                    
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
                        if not target.alive: # killed its target, remove from combat
                            self.enemies.remove(target)
                    elif not hit_result[0] and hit_result[1] != 1: # non-critical miss, display this message instead of crit miss message
                        print(f"\n{combatant.name} missed their attack on {target.name}.")
            turn += 1
            # at end of turn, check if either team is fully dead
            if not self.team:
                return self.make_result(False)
            elif not self.enemies:
                return self.make_result(True)
    
    def calculate_hit(self, combatant, enemy): # combatant rolling the hit
        d20 = random.randint(1,20)
        if d20 == 1:
            print(f"\n{combatant.name} critically missed!")
            return (False, 1) # 1 means crit, True means hit
        elif d20 == 20:
            return (True, 1) # True represents hit landing
        
        # look for ability bonus - determine type of weapon
        bonus = 0
        if combatant.weapon is None: # unarmed, use strength for physical
            desiredStat = 'strength'
        else:
            wpnRange = combatant.weapon['weapon_range'].lower() # melee or ranged
            if wpnRange == 'melee':
                desiredStat = "strength"
            else:
                desiredStat = "dexterity"
        
        if isinstance(combatant, Enemy.Enemy): # enemy trying to hit party member
            monsterData = combatant.enemyData
            bonus = combatant.get_bonus(monsterData[desiredStat]) # bonus to add or subtract
            return ((d20 + bonus >= enemy.AC), 0) # True if hit >= AC, false otherwise, no crit
        else: # party member trying to hit enemy
            bonus = combatant.get_bonus(getattr(combatant, desiredStat))
            return ((d20 + bonus >= enemy.AC),0) # True if hit >= AC, false otherwise, no crit
        
    def calculate_damage(self, combatant, enemy, crit): # return int for damage
        dmg = 0
        weapon = combatant.weapon
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
            
            bonus = 0
            wpnRange = combatant.weapon['weapon_range'].lower() # melee or ranged
            if wpnRange == 'melee':
                desiredStat = "strength"
            else:
                desiredStat = "dexterity"
            
            if isinstance(combatant, Character.Character): # character bonus
                bonus = combatant.get_bonus(getattr(combatant, desiredStat))
                dmg += bonus
                dmg = max(1, dmg)
            else: # enemy bonus:
                bonus = combatant.get_bonus(combatant.enemyData[desiredStat])
                dmg += bonus
                dmg = max(1, dmg)
        else: # unarmed, weapon == None
            desiredStat = "strength"
            bonusDmg = 0 # no str bonus by default
            if isinstance(combatant, Character.Character):
                bonusDmg = combatant.get_bonus(combatant.strength)
            else: # enemy hits unarmed
                bonusDmg = combatant.get_bonus(combatant.enemyData[desiredStat])
            dmg = max(0,1 + bonusDmg) # default unarmed dmg is 1 + bonus
            print(f"\n{combatant.name} is unarmed but hits {enemy.name} for {dmg} damage!")
            return dmg
        if crit:
            print(f"\n{combatant.name} landed a critical hit on {enemy.name} with their {combatant.weapon['name']} for {dmg} damage!")
        else:
            print(f"\n{combatant.name} hits {enemy.name} with their {combatant.weapon['name']} for {dmg} damage!")
        return dmg
    
    def calculate_initiative(self, combatant): # Enemy or Character arg
        d20 = random.randint(1,20)
        if isinstance(combatant, Enemy.Enemy): # enemy initiative
            monsterData = combatant.enemyData
            bonus = math.floor((monsterData["dexterity"] - 10) / 2) # bonus to add or subtract
            return (d20 + bonus) # initiative value for the combat
        else:
            return (d20 + combatant.get_bonus(combatant.dexterity))

    
    def make_result(self, win):
            if not win:
                print("Your party has been defeated! Game over.")
                return False
            else:
                print("You have defeated all enemies! Victory!")
                return True
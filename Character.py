import math
import random
import requests
from Being import Being
from console_utils import cprint as print


class Character(Being):
    def __init__(self, name, classData, raceData, equipment, proficiencies, s, d, c, i, w, ch, hp, level=1, xp=0):
        super().__init__(name, hp)
        self.classData = classData # whole JSON of class data
        self.raceData = raceData # ^^ race
        self.equipment = equipment # list
        self.proficiencies = proficiencies
        self.strength = s
        self.dexterity = d
        self.constitution = c
        self.intelligence = i
        self.wisdom = w
        self.charisma = ch
        self.maxHP = hp
        self.level = level
        self.xp = xp
        self.set_speed()
        self.set_weapon_list()
        self.set_weapon()
        self.proficientWeapon = 0 # prof bonus to add for attack rolls
        self.set_AC()
    
    def check_level_up(self):
        requiredXP = 300* 3**(self.level-1) # say it triples per level (unbalanced for post-4)
        if self.xp < requiredXP:
            return
        
        # level reached...
        self.level += 1
        self.xp = 0
        print(f"{self.name} has reached level {self.level}!", style="bold green")
        # class levelup TBD
        if self.proficientWeapon != 0: # proficient with current wpn
            self.proficientWeapon = 1 + math.ceil(self.level/4) # account for new level in proficiency bonus
        
        print(f"What should {self.name} level up with 2 points?", style="bold yellow")
        print(f"1) Strength ({self.strength})\n2) Dexterity ({self.dexterity})\n3) Constitution ({self.constitution})\n4) Intelligence ({self.intelligence})\n5) Wisdom ({self.wisdom})\n6) Charisma ({self.charisma})", style="green")

        while True:
            choice = 0
            try:
                choice = int(input("> ").strip())
                if choice <= 6 and choice > 0: # check both conditions here
                    break
                else:
                    print("Invalid choice. Please select a new skill with the numbers on the left.\n", style="bold red") # input is int but invalid
            except:
                print("Invalid choice. Please select a new skill with the numbers on the left.\n", style="bold red") # input is not int
        match (choice):
            case 1:
                self.strength = min(self.strength+2,20) # cap at 20
            case 2:
                self.dexterity = min(self.dexterity+2,20)
            case 3:
                self.constitution = min(self.constitution+2,20)
            case 4:
                self.intelligence = min(self.intelligence+2,20)
            case 5:
                self.wisdom = min(self.wisdom+2,20)
            case 6:
                self.charisma = min(self.charisma+2,20)
        # extra hit die...
        self.hp = self.level*self.classData['hit_die'] + self.get_bonus(self.constitution)*self.level # using potentially new constitution value, so recalculate
        self.maxHP = self.hp
        
    def show_equipment(self):
        prevItem = ""
        dupeCount = 1
        for item in self.equipment:
            if item != prevItem:
                if prevItem != "":
                    if dupeCount > 1:
                        print(f" x{dupeCount}", style="yellow")
                    else:
                        print()
                print(f"{item['name']}", style="bold", end='')
                dupeCount = 1
            else:
                dupeCount += 1
            prevItem = item
        if dupeCount > 1:
            print(f" x{dupeCount}", style="yellow")
        else:
            print()
    
    def choose_weapon(self):
        self.weapons = sorted(self.weapons, key=lambda d: int(d['damage']['damage_dice'][d['damage']['damage_dice'].index("d")+1:]), reverse=True)
        for i,item in enumerate(self.weapons):
            print(f"{i+1}) {item['name']} - {item['damage']['damage_dice']}", style="green")
        while True:
            try:
                choice = int(input("> ").strip())
                if 1 <= choice <= len(self.weapons):
                    self.set_weapon(self.weapons[choice-1])
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.weapons)}", style="bold red")
            except ValueError:
                print(f"Please enter a number between 1 and {len(self.weapons)}", style="bold red")
        
        
    def set_weapon_list(self):
        self.weapons = []
        for item in self.equipment:
            url = f"https://www.dnd5eapi.co/api/2014/equipment/{item['index']}"
            response = requests.get(url)
            itemData = response.json()
            self.add_weapon_to_list(itemData)

    
    def set_weapon(self, weaponToEquip=None): 
        if weaponToEquip is None:
            self.weapon = None
            self.weapon = random.choice(self.weapons) # pick random weapon from inventory
        elif weaponToEquip == self.weapon: # already equipped this
            return
        else: # weapon passed in to equip
            if "damage" in weaponToEquip: # equip this - do not add it to the list, new weapons will run add_weapon_to_list directly
                self.weapon = weaponToEquip
        
        if self.weapon is None: # no Weapon equipped, always proficient with unarmed
            self.proficientWeapon = 1 + math.ceil(self.level/4) # round up, so +2 for level 1-4 etc
        else: # a weapon has been equipped
            weaponType = self.weapon['weapon_category'].lower() # like "simple"
            for proficiency in self.proficiencies:
                if f"{weaponType}-weapons" in proficiency['index']: # like "simple-weapons", this matches...
                    self.proficientWeapon = 1 + math.ceil(self.level/4)
                    break
                else: # check for 1-1 proficiency in the weapon itself
                    if self.weapon['index'] in proficiency['index']: # like 'handaxe' in 'handaxes'
                        self.proficientWeapon = 1 + math.ceil(self.level/4)
                        break        
        
    
    def add_weapon_to_list(self, weaponToAdd):
        if 'damage' in weaponToAdd: # check if the equipment has a damage attribute (it can be used as a weapon)
            self.weapons.append(weaponToAdd)
            return True
        else:
            return False
        
    def set_AC(self):
        armour = 10
        usingArmour = False
        for item in self.equipment:
            url = f"https://www.dnd5eapi.co/api/2014/equipment/{item['index']}"
            response = requests.get(url)
            itemData = response.json()
            shieldAC = 0
            if itemData['equipment_category']['index'] == "armor": # this is armour
                if itemData['armor_category'] == "Shield":
                    shieldAC = itemData['armor_class']['base']
                else: # normal armour, not shield
                    armour = itemData['armor_class']['base'] # add base AC, then calculate bonus
                    usingArmour = True
                    
                    category = itemData['armor_category']
                    match category:
                        case "Light":
                            armour += self.get_bonus(self.dexterity)
                            break
                        case "Medium":
                            armour += min(2,self.get_bonus(self.dexterity))
            armour += shieldAC
            if shieldAC != 0 and usingArmour:
                break # already got shield and armour bonuses added, so stop searching
            
        if not usingArmour: # unarmoured gets dex bonus
            armour += self.get_bonus(self.dexterity)
        self.AC = armour
        
    def set_speed(self):
        self.speed = self.raceData['speed'] # should be an int
    
import random
import requests
from Being import Being


class Character(Being):
    def __init__(self, name, classData, raceData, equipment, proficiencies, s, d, c, i, w, ch, hp):
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
        self.set_speed()
        self.set_weapon_list()
        self.set_weapon()
        self.set_AC()
    
    def show_equipment(self):
        prevItem = ""
        dupeCount = 1
        for item in self.equipment:
            if item != prevItem:
                if prevItem != "":
                    if dupeCount > 1:
                        print(f" x{dupeCount}")
                    else:
                        print()
                print(f"{item['name']}", end='')
                dupeCount = 1
            else:
                dupeCount += 1
            prevItem = item
        if dupeCount > 1:
            print(f" x{dupeCount}")
        else:
            print()
    
    def choose_weapon(self):
        for i,item in enumerate(self.weapons):
            print(f"{i+1}) {item['name']} - {item['damage']['damage_dice']}")
        while True:
            try:
                choice = int(input("> ").strip())
                if 1 <= choice <= len(self.weapons):
                    self.set_weapon(self.weapons[choice-1])
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.weapons)}")
            except ValueError:
                print(f"Please enter a number between 1 and {len(self.weapons)}")
        
        
    def set_weapon_list(self):
        self.weapons = []
        for item in self.equipment:
            url = f"https://www.dnd5eapi.co/api/2014/equipment/{item['index']}"
            response = requests.get(url)
            itemData = response.json()
            self.add_weapon_to_list(itemData)

    
    def set_weapon(self, weaponToEquip=None): # return True if a weapon is equipped, False otherwise
        if weaponToEquip is None:
            self.weapon = None
            self.weapon = random.choice(self.weapons) # pick random weapon from inventory
            return True
        else: # weapon passed in to equip
            if "damage" in weaponToEquip: # equip this - do not add it to the list, new weapons will run add_weapon_to_list directly
                self.weapon = weaponToEquip
                return True
        return False
    
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
    
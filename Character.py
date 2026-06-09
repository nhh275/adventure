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
        self.set_speed()     
        self.set_weapon()
        self.set_AC()
    
    def show_equipment(self):
        for item in self.equipment:
            print(item['name'])
        
    def set_weapon(self):
        self.weapon = None
        for item in self.equipment:
            url = f"https://www.dnd5eapi.co/api/2014/equipment/{item['index']}"
            response = requests.get(url)
            itemData = response.json()
            if 'damage' in itemData: # check if the equipment has a damage attribute (it can be used as a weapon)
                self.weapon = itemData
                return # just use the first weapon
        # no weapon found
    
    def set_AC(self):
        armour = 0
        for item in self.equipment:
            url = f"https://www.dnd5eapi.co/api/2014/equipment/{item['index']}"
            response = requests.get(url)
            itemData = response.json()
            if itemData['equipment_category']['index'] == "armor": # this is armour
                armour = itemData['armor_class']['base']
                break
        # unarmoured also uses dex for bonus, start at 0 though
        # DEX BONUS TBD - ABILITY BONUSES NOT YET CREATED
        self.AC = armour    
        
    def set_speed(self):
        self.speed = self.raceData['speed'] # should be an int
    
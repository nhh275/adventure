import random

import requests


class Character:
    def __init__(self, name, player_class, race, equipment, proficiencies, hp=10):
        self.name = name
        self.player_class = player_class
        self.race = race
        self.equipment = equipment
        self.proficiencies = proficiencies
        self.hp = hp
        self.alive = True
        self.set_speed()     
        self.set_weapon() # weapon is a JSON of the item (equipment)
        self.set_AC()
        
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
        url = f"https://www.dnd5eapi.co/api/2014/races/{self.race.lower()}"
        response = requests.get(url)
        raceData = response.json()
        self.speed = raceData['speed'] # should be an int
    
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target, dmg=0):
        target.add_hp(-dmg) # armour tbd
    
    def get_name(self):
        return self.name
    
    def get_class(self):
        return self.player_class
    
    def get_race(self):
        return self.race
    
    def get_equipment(self):
        return self.equipment
    
    def get_proficiencies(self):
        return self.proficiencies
    
    def get_hp(self):
        return self.hp
    
    def add_hp(self, amount=0):
        self.hp += amount
        if self.hp <= 0:
            self.hp = 0
            self.die()
        else:
            print(f"{self.name} now has {self.hp} HP.")
        
    def is_alive(self):
        return self.alive
    
    def get_speed(self):
        return self.speed

    def get_weapon(self):
        return self.weapon
    
    def get_AC(self):
        return self.AC
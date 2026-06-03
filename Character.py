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
        
    def set_speed(self):
        url = f"https://www.dnd5eapi.co/api/2014/races/{self.race.lower()}"
        response = requests.get(url)
        raceData = response.json()
        self.speed = raceData['speed'] # should be an int
    
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target, dmg=None):
        # placeholder attack method, will be fleshed out later
        print(f"{self.name} attacks {target.name}!")
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
    
    def add_hp(self, amount):
        self.hp += amount
        if self.hp < 0:
            self.hp = 0
            self.die()
        else:
            print(f"{self.name}'s health changes by {amount} HP. Current HP: {self.hp}\n")
        
    def is_alive(self):
        return self.alive
    
    def get_speed(self):
        return self.speed
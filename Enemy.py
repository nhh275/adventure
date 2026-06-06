import math
import requests
from Being import Being


class Enemy(Being):
    def __init__(self, name, type, hp):
        super().__init__(name, hp)
        self.type = type
        self.set_speed()
        self.set_weapon()
        self.set_AC()
        
    def set_weapon(self):
        self.weapon = None  # in case no weapon found, set to None
        url = f"https://www.dnd5eapi.co/api/2014/monsters/{self.type.lower()}"
        response = requests.get(url)
        monsterData = response.json()        
        url = f"https://www.dnd5eapi.co/api/2014/equipment/{monsterData['actions'][0]['name'].lower()}"
        if url != None:
            response = requests.get(url)
            self.weapon = response.json()
        
    def set_AC(self):
        url = f"https://www.dnd5eapi.co/api/2014/monsters/{self.type.lower()}"
        response = requests.get(url)
        monsterData = response.json()  
        armour = monsterData['armor_class'][0]['value'] # armour AC, assume all can use dex
        modifier = min(2,math.floor((monsterData['dexterity']-10) / 2)) # cap it at +2 bonus
        self.AC = math.floor((armour + modifier) * 0.6)
        
    def set_speed(self):
        url = f"https://www.dnd5eapi.co/api/2014/monsters/{self.type.lower()}"
        response = requests.get(url)
        monsterData = response.json()
        self.speed = int(monsterData['speed']['walk'].split(' ')[0]) # get the int
    
    def get_type(self):
        return self.type
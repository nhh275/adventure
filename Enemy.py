import math
import random
import requests
from Being import Being


class Enemy(Being):
    def __init__(self, name, enemyData, hp):
        super().__init__(name, hp)
        self.enemyData = enemyData # whole JSON of monster data
        self.set_speed()
        self.set_weapon()
        self.set_AC()
        
    def set_weapon(self):
        self.weapon = None  # in case no weapon found, set to None     
        possible_weapons = [self.enemyData['actions'][i]['name'].lower() for i in range(len(self.enemyData['actions']))]
        if possible_weapons:
            chosen = random.choice(possible_weapons)
        else:
            chosen = ""
        url = f"https://www.dnd5eapi.co/api/2014/equipment/{chosen}" # search for data on randomly chosen weapon
        if url != None:
            response = requests.get(url)
            self.weapon = response.json()
        
    def set_AC(self):
        armour = self.enemyData['armor_class'][0]['value'] # armour AC, accounts for shield and bonus already
        modifier = min(2,math.floor((self.enemyData['dexterity']-10) / 2)) # cap it at +2 bonus
        self.AC = math.floor((armour + modifier) * 0.6)
        
    def set_speed(self):
        self.speed = int(self.enemyData['speed']['walk'].split(' ')[0]) # get the int

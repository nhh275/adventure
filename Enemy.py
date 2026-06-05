import math
import requests

class Enemy:
    def __init__(self, name, type, hp, dmg):
        self.name = name
        self.type = type
        self.hp = hp
        self.dmg = dmg
        self.alive = True
        self.set_speed()
        self.set_weapon() # weapon is a JSON of the item (equipment), None if none found
        self.set_AC()
        
    def set_weapon(self):
        self.weapon = None # in case no weapon found, set to None
        url = f"https://www.dnd5eapi.co/api/2014/monsters/{self.type.lower()}"
        response = requests.get(url)
        monsterData = response.json()        
        url = f"https://www.dnd5eapi.co/api/2014/equipment/{monsterData['actions'][0]['name'].lower()}" # like 'Scimitar'
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
    
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target, dmg=0):
        target.add_hp(-dmg) # armour tbd
    
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type
    
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
        
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def get_weapon(self):
        return self.weapon
    
    def get_AC(self):
        return self.AC
import requests


class Enemy:
    def __init__(self, name, type, hp, dmg):
        self.name = name
        self.type = type
        self.hp = hp
        self.dmg = dmg
        self.alive = True
        self.set_speed()
    
    def set_speed(self):
        url = f"https://www.dnd5eapi.co/api/2014/monsters/{self.type.lower()}"
        response = requests.get(url)
        monsterData = response.json()
        self.speed = int(monsterData['speed']['walk'].split(' ')[0]) # get the int
    
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target):
        print(f"{self.name} attacks {target.name}!")
        target.add_hp(-self.dmg) # armour tbd
    
    def get_name(self):
        return self.name
    
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
        
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
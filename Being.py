import math
import time
import requests
from abc import ABC, abstractmethod

class Being(ABC):
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.alive = True
        self.weapon = None
        self.AC = 10  # default AC
        self.speed = 30  # default speed in feet
        
    @abstractmethod
    def set_weapon(self):
        pass
    
    @abstractmethod
    def set_AC(self):
        pass
    
    @abstractmethod
    def set_speed(self):
        pass
    
    def get_bonus(self, score): # get ability bonus modifier from score
        return math.floor((score-10) / 2)
    
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target, dmg=0):
        target.add_hp(-dmg)
        time.sleep(0.5)

    
    def add_hp(self, amount=0):
        self.hp += amount
        if self.hp <= 0:
            self.hp = 0
            self.die()
        else:
            print(f"{self.name} now has {self.hp} HP.")
    
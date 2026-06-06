import requests
from abc import ABC, abstractmethod


class Being(ABC):
    """
    Abstract superclass representing any entity in the game (characters, enemies, etc.)
    Defines common attributes and behavior shared between different types of beings.
    """
    
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.alive = True
        self.weapon = None
        self.AC = 10  # default AC
        self.speed = 30  # default speed in feet
        
    @abstractmethod
    def set_weapon(self):
        """Fetch and set the weapon based on being type. Implemented by subclasses."""
        pass
    
    @abstractmethod
    def set_AC(self):
        """Calculate and set armor class. Implemented by subclasses."""
        pass
    
    @abstractmethod
    def set_speed(self):
        """Fetch and set movement speed. Implemented by subclasses."""
        pass
    
    def die(self):
        """Mark the being as dead."""
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target, dmg=0):
        """Attack another being, dealing damage."""
        target.add_hp(-dmg)
    
    def get_name(self):
        """Return the being's name."""
        return self.name
    
    def get_hp(self):
        """Return current HP."""
        return self.hp
    
    def add_hp(self, amount=0):
        """Add or subtract HP, triggering death if HP <= 0."""
        self.hp += amount
        if self.hp <= 0:
            self.hp = 0
            self.die()
        else:
            print(f"{self.name} now has {self.hp} HP.")
    
    def is_alive(self):
        """Return whether the being is alive."""
        return self.alive
    
    def get_speed(self):
        """Return movement speed."""
        return self.speed
    
    def get_weapon(self):
        """Return equipped weapon."""
        return self.weapon
    
    def get_AC(self):
        """Return armor class."""
        return self.AC

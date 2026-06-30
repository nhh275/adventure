import json
import time
import requests
from typing import Dict, Optional

class GameDataManager:    
    def __init__(self):
        self.monsters = {}
        self.spells = {}
        self.items = {}
        self.classes = {}
        self.races = {}
        self.is_loaded = False
        self.load_time = 0
        
    def load_all(self, use_cache=True) -> bool:
        # monsters
        url = 'https://www.dnd5eapi.co/api/2014/monsters/goblin'
        self.monsters['goblin'] = requests.get(url).json()
        url = 'https://www.dnd5eapi.co/api/2014/monsters/skeleton'
        self.monsters['skeleton'] = requests.get(url).json()
        url = 'https://www.dnd5eapi.co/api/2014/monsters/ghoul'
        self.monsters['ghoul'] = requests.get(url).json()
        
        # classes
        url = 'https://www.dnd5eapi.co/api/2014/classes'
        data = requests.get(url).json()
        for cls in data['results']: # list of class names
            self.classes[cls['index']] = requests.get(f"https://www.dnd5eapi.co{cls['url']}").json() # "barbarian": barbarianData
        
        # races
        url = 'https://www.dnd5eapi.co/api/2014/races'
        data = requests.get(url).json()
        for race in data['results']: # list of class names
            self.races[race['index']] = requests.get(f"https://www.dnd5eapi.co{race['url']}").json() # "barbarian": barbarianData
        
        self.is_loaded = True
        return True

    def save_item(self, item, use_cache=True):
        if not self.get_item(item['index']):
            self.items[item['index']] = item # 'scimitar' = scimitar data dict
    
    def get_item(self, index):
        return self.items.get(index) # return None if not found
            
    def get_monster(self, index: str) -> Optional[Dict]:
        return self.monsters.get(index) # the dict for an Enemy like "ghoul"
    
    def get_class(self, index: str) -> Optional[Dict]:
        return self.classes.get(index) 
    
    def get_race(self, index: str) -> Optional[Dict]:
        return self.races.get(index) 

game_data = GameDataManager()

def init_data(use_cache=True):
    return game_data.load_all(use_cache=use_cache)
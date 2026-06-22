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
        
        inline_weapons = [] # try to find weapons with inline damage data, like for Apes
        if 'actions' in self.enemyData:
            for action in self.enemyData['actions']:
                if 'damage' in action and isinstance(action['damage'], list) and len(action['damage']) > 0:
                    if 'damage_dice' in action['damage'][0]:
                        weapon_range = 'melee'
                        if 'actions' in action and isinstance(action['actions'], list):
                            for nested_action in action['actions']:
                                if 'type' in nested_action:
                                    weapon_range = nested_action['type']
                                    break
                        
                        # makes a weapon object in the format expected by Combat.py...
                        weapon_obj = {
                            'name': action.get('name', 'Unknown Weapon'),
                            'weapon_range': weapon_range,
                            'damage': {
                                'damage_dice': action['damage'][0]['damage_dice']
                            }
                        }
                        inline_weapons.append(weapon_obj)
        
        if inline_weapons:
            self.weapon = random.choice(inline_weapons)
        else: # if its formatted as an equipment item, api lookup the item for details
            possible_weapons = [self.enemyData['actions'][i]['name'].lower() for i in range(len(self.enemyData['actions']))] if 'actions' in self.enemyData else []
            if possible_weapons:
                chosen = random.choice(possible_weapons)
            else:
                chosen = ""
            if chosen != "":
                url = f"https://www.dnd5eapi.co/api/2014/equipment/{chosen}" # search for data on randomly chosen weapon
                response = requests.get(url)
                self.weapon = response.json()
        
    def set_AC(self):
        armour = self.enemyData['armor_class'][0]['value'] # armour AC, accounts for shield and bonus already
        self.AC = math.floor((armour + min(2,self.get_bonus(self.enemyData['dexterity'])))) # weakens enemy AC to be generous
        
    def set_speed(self):
        self.speed = int(self.enemyData['speed']['walk'].split(' ')[0]) # get the int

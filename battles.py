import pprint
import random, requests
from Enemy import Enemy
from Combat import Combat
def goblins(party):
    url = "https://www.dnd5eapi.co/api/2014/monsters/goblin"
    response = requests.get(url)
    goblinData = response.json() 
    numGoblins = random.randint(2, 4) # inclusive both ways
    goblins = [] # Enemy list
    for i in range(numGoblins):
        dmg = goblinData['actions'][0]['damage'][0]['damage_dice'] # this is a string like "2d6", so we need to parse it
        dmg = dmg.split('d') # split into number of dice and sides
        numDice = int(dmg[0])
        bonusDmg = 0
        if "+" in dmg[1]: # some monsters have a bonus damage, so check for that too
            dmg[1] = dmg[1].split('+')[0] # make the bonus 2 for all weapons, simplicity
            bonusDmg = 2
        sides = int(dmg[1])
        totalDmg = 0
        for _ in range(numDice):
            totalDmg += random.randint(1, sides) # roll the dice once to determine dmg for the fight, simplified
        
        goblins.append(Enemy(f"Goblin {i+1}", goblinData, goblinData['hit_points']))
    print(f"\nYou encounter {numGoblins} goblins!")
        
    # undergo combat
    combat = Combat(party.members, goblins)
    win = combat.start_combat()
    
    return win
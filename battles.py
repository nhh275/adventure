import pprint
import random, requests
from Enemy import Enemy
from Combat import Combat
from console_utils import cprint as print

def goblins(party):
    url = "https://www.dnd5eapi.co/api/2014/monsters/goblin"
    response = requests.get(url)
    goblinData = response.json() 
    numGoblins = random.randint(2, 3) # inclusive both ways, gen a random number of goblins
    goblins = [] # Enemy list
    for i in range(numGoblins):
        goblins.append(Enemy(f"Goblin {i+1}", goblinData, goblinData['hit_points']))
    print(f"\nYou encounter {numGoblins} goblins!", style="bold red")
    
    # undergo combat
    combat = Combat(party.members, goblins)
    return combat.start_combat() # returns tuple of (Success, xpListToAdd)

def skeleton(party):
    url = "https://www.dnd5eapi.co/api/2014/monsters/skeleton"
    response = requests.get(url)
    enemyData = response.json() 
    skeletonList = [Enemy(f"Skeleton", enemyData, enemyData['hit_points'])] # Enemy list (1 skelly)

    print(f"\nYou encounter a skeleton!", style="bold red")
    
    # undergo combat
    combat = Combat(party.members, skeletonList)
    return combat.start_combat()
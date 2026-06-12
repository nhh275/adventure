import pprint
import random, requests
from Enemy import Enemy
from Combat import Combat
def goblins(party):
    url = "https://www.dnd5eapi.co/api/2014/monsters/goblin"
    response = requests.get(url)
    goblinData = response.json() 
    numGoblins = random.randint(2, 3) # inclusive both ways
    goblins = [] # Enemy list
    for i in range(numGoblins):
        goblins.append(Enemy(f"Goblin {i+1}", goblinData, goblinData['hit_points']))
    print(f"\nYou encounter {numGoblins} goblins!")
    
    # undergo combat
    combat = Combat(party.members, goblins)
    win = combat.start_combat()
    
    return win

def skeleton(party):
    url = "https://www.dnd5eapi.co/api/2014/monsters/skeleton"
    response = requests.get(url)
    enemyData = response.json() 
    skeletonList = [Enemy(f"Skeleton", enemyData, enemyData['hit_points'])] # Enemy list (1 skelly)

    print(f"\nYou encounter a skeleton!")
    
    # undergo combat
    combat = Combat(party.members, skeletonList)
    win = combat.start_combat()
    
    return win
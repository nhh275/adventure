import pprint
import random, requests
from Enemy import Enemy
from Combat import Combat
from console_utils import cprint as print
from game_data import game_data

def battle(party, surprise, enemyIndex, numEnemiesLower, numEnemiesHigher=0): # DRY subroutine to work with any enemy, rather than 1 routine per enemy
    enemyData = game_data.get_monster(enemyIndex)
    if numEnemiesHigher < numEnemiesLower: # just 1 enemy, a higher bound has not been passed in (0 default)
        numEnemies = numEnemiesLower
    else:
        numEnemies = random.randint(numEnemiesLower, numEnemiesHigher) # random number of enemies from lower to upper bound
    enemies = [] # Enemy list
    for i in range(numEnemies):
        enemies.append(Enemy(f"{enemyData['name']} {i+1}", enemyData, enemyData['hit_points']))
    print(f"\nYou encounter {numEnemies} {enemyData['index']}/s!", style="bold red")
    
    # undergo combat
    combat = Combat(party.members, enemies, surprise)
    resultTuple = combat.start_combat() # returns tuple of (Success, xpListToAdd)
    if not resultTuple[0]: # loss
        return False
    
    party.heal_party()
    party.give_xp(resultTuple[1]) # list of xp from enemies to add to party members
    return True
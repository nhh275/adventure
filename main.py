import math

import requests, pprint
from Party import Party
from Character import Character
import battles


def beginAdventure(party):
    print("\nYour adventure begins in the magical city of Swindon, where you find yourself on the side of a road sparsely populated by vehicles. "
          "\nIt is a calm day, with the regular clouds scattered across the sky and no sun to be seen, as is typical for this land. "
          "\nYour ponderance is interrupted by the sound of a car drawing near, its engine rumbling as it slows its approach.")
    input("> ")
    print("\nFrom within the vehicle and through a crack in the window shouts a voice, 'Excuse me! Do you live here? I need some help navigating this area - "
          "\ndo you understand the Magic Roundabout?' The window is rolled down further to reveal a man of staggering size - a height that makes you wonder how " 
          "\nsuch an individual could even fit in a Hyundai i10, let alone drive it comfortably.")
    input("> ")
    print("\nPutting your bewilderment aside, you must say something in response. Do you help? (yes/no)")
    choice = input("> ").strip().lower()
    if choice == "yes" or choice == "y":
        print("\nYou offer to help the man and he slows the vehicle to a stop beside you on the double yellow lines, flashing his emergency lights. "
              "\nYou attempt to explain the wonder of the Roundabout, but its mystery is too complex, and he ends up inviting you into the passenger seat for a "
              "\nmore direct guide. You are tentative to accept, but remember that you've been trying to work on your bravery lately, so you hop in and buckle up.")
        input("> ")
        roundabout(party)
    else:
        print("\nYou shrug, mumbling something about just visiting, and leave the way hulking unit in disappointment, continuing on your path into the city.")
        input("> ")
        city(party)
    return

def roundabout(party):
    print("\nWhen you enter, the man introduces himself as a Rogue named Terry and explains that he's been stuck here for hours, desperate for some help. "
          "\nHe seems normal enough, despite his tremendous stature, and you drive in relative peace until you see the great sign for the Magic Roundabout up ahead. "
          "\nAs you approach, you sense Terry's nerves rising, sweat dripping down his face as he prepares to challenge the Roundabout with you by his side.")
    input("> ")
    print("\nYou are about to enter the start of the Roundabout, when all of a sudden, the boot of the following car flies open, giving way to a collection of "
          "\nwhat you can only assume to be goblins from some sort of fantasy world. The creatures leap out and mob the Hyundai, before any evasive maneouvres can be taken. "
          "\nThe only option is to fight, so you steel yourself and tell Terry 'I hope you've fought before, this won't be fun.'")
    input("> ")
    # make Terry
    
    url = "https://www.dnd5eapi.co/api/2014/classes/rogue"
    response = requests.get(url)
    classData = response.json()
    url = "https://www.dnd5eapi.co/api/2014/races/human"
    response = requests.get(url)
    raceData = response.json()
    equipmentToAdd = []
    for item in classData['starting_equipment']: # even if the class doesnt have starting equipment, check
        equipmentToAdd.append(item['equipment'])
    if 'starting_equipment_options' in classData: # some classes don't have this optional equipment, so check for it first
        if 'of' in classData['starting_equipment_options'][0]['from']['options'][0]: # some classes have options that aren't equipment, so check for that too
            equipmentToAdd.append(classData['starting_equipment_options'][0]['from']['options'][0]['of']) # just add the first option for simplicity
    proficienciesToAdd = []
    for item in classData['proficiencies']: 
        proficienciesToAdd.append(item)
    
    terry = Character("Terry", classData['index'], raceData['index'], equipmentToAdd, proficienciesToAdd, math.floor(classData['hit_die'] * 2))
    party.add_member(terry)
    # time to scrap 
    win = battles.goblins(party)
    return

def city(party):
    print()
    return


# start of game / setup
def main():
    print("\nWelcome to your grand adventure!")
    print("What is your name, adventurer? ") # unsanitised 
    playerName = input("> ").strip().title()
    if playerName == "":
        playerName = "Nameless One"

    url = "https://www.dnd5eapi.co/api/2014/classes"
    response = requests.get(url)
    data = response.json()
    for i in range(data['count']):
        print(data['results'][i]['name'])

    print("\nWhich class takes your fancy today? ")
    chosenClass = str(input("> ")).strip().lower()
    url = f"https://www.dnd5eapi.co/api/2014/classes/{chosenClass}"
    response = requests.get(url)
    classData = response.json()


    url = "https://www.dnd5eapi.co/api/2014/races"
    response = requests.get(url)
    data = response.json()
    for i in range(data['count']):
        print(data['results'][i]['name'])
        
    print("\nWhich race are you? ")
    chosenRace = str(input("> ")).strip().lower()
    url = f"https://www.dnd5eapi.co/api/2014/races/{chosenRace}"
    response = requests.get(url)
    raceData = response.json()

    print(f"\n{playerName} the mighty {raceData['name']} {classData['name']}! A wonderful choice.")
    print("\nYou have the following proficiencies and ability bonuses:")

    for i in range(len(classData['proficiencies'])):
        print(classData['proficiencies'][i]['name'])
    for i in range(len(raceData['ability_bonuses'])):
        print(f"+ {raceData['ability_bonuses'][i]['bonus']} to {raceData['ability_bonuses'][i]['ability_score']['name']}")

    equipmentToAdd = []
    for item in classData['starting_equipment']: # even if the class doesnt have starting equipment, check
        equipmentToAdd.append(item['equipment'])
    if 'starting_equipment_options' in classData: # some classes don't have this optional equipment, so check for it first
        if 'of' in classData['starting_equipment_options'][0]['from']['options'][0]: # some classes have options that aren't equipment, so check for that too
            equipmentToAdd.append(classData['starting_equipment_options'][0]['from']['options'][0]['of']) # just add the first option for simplicity

    proficienciesToAdd = []
    for item in classData['proficiencies']: 
        proficienciesToAdd.append(item)
    print(raceData['language_desc'])
    # leave further customisation for now

    player = Character(playerName, classData['index'], raceData['index'], equipmentToAdd, proficienciesToAdd, classData['hit_die'] * 2) 
    party = Party()
    party.add_member(player)
    # setup done 
    
    print("Your character is ready! Your adventure is about to unfold...\n\n")
    beginAdventure(party)
    return
    
if __name__ == "__main__":
    main()
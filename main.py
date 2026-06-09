import math
import random

import requests, pprint
from Party import Party
from Character import Character
import battles


def choose_from_equipment_category(url, equipmentToAdd, numChoices=1):
    response = requests.get(f"https://www.dnd5eapi.co{url}")
    listData = response.json() # json of equipment choice data
    print(f"Choose {numChoices} to add from the following list:")
    for i in range(len(listData['equipment'])):
        print(f"{chr(i+97)}) {listData['equipment'][i]['name']}") # show each option with a number to choose from

    for _ in range(numChoices):
        choice = str(input("> ").strip().lower()) # from a, b....
        itemToAdd = listData['equipment'][ord(choice)-97]
        equipmentToAdd.append(itemToAdd)


def add_default_equipment_from_category(url, equipmentToAdd, numChoices):
    response = requests.get(f"https://www.dnd5eapi.co{url}")
    listData = response.json() # json of equipment choice data
    for i in range(numChoices):
        itemToAdd = listData['equipment'][i]
        equipmentToAdd.append(itemToAdd)


def beginAdventure(party):
    print(
        "\nYour adventure begins in the magical city of Swindon, where you find yourself on the side of a road sparsely populated by vehicles. "
        "It is a calm day, with the regular clouds scattered across the sky and no sun to be seen, as is typical for this land. "
        "Your ponderance is interrupted by the sound of a car drawing near, its engine rumbling as it slows its approach."
    )
    input("> ")
    print(
        "\nFrom within the vehicle and through a crack in the window shouts a voice, 'Excuse me! Do you live here? I need some help navigating this area - "
        "do you understand the Magic Roundabout?' The window is rolled down further to reveal a man of staggering size - a height that makes you wonder how "
        "such an individual could even fit in a Hyundai i10, let alone drive it comfortably."
    )
    input("> ")
    print("\nPutting your bewilderment aside, you must say something in response. Do you help? (yes/no)")
    choice = input("> ").strip().lower()
    if choice == "yes" or choice == "y":
        print(
            "\nYou offer to help the man and he slows the vehicle to a stop beside you on the double yellow lines, flashing his emergency lights. "
            "You attempt to explain the wonder of the Roundabout, but its mystery is too complex, and he ends up inviting you into the passenger seat for a "
            "more direct guide. You are tentative to accept, but remember that you've been trying to work on your bravery lately, so you hop in and buckle up."
        )
        input("> ")
        roundabout(party)
    else:
        print("\nYou shrug, mumbling something about just visiting, and leave the way hulking unit in disappointment, continuing on your path into the city.")
        input("> ")
        city(party)
    return

def roundabout(party):
    print(
        "\nWhen you enter, the man introduces himself as Terry and explains that he's been stuck here for hours, desperate for some help. "
        "On closer inspection, you see reptilian scales on his neck and hands - this is no regular human, but you feel safe nonetheless. "
        "You drive in relative peace until you see the great sign for the Magic Roundabout up ahead. "
        "As you approach, you sense Terry's nerves rising, sweat dripping down his face as he prepares to challenge the Roundabout with you by his side."
    )
    input("> ")
    print(
        "\nYou are about to enter the start of the Roundabout, when all of a sudden, the boot of the following car flies open, giving way to a collection of "
        "what you can only assume to be goblins from some sort of fantasy world. The creatures leap out and mob the Hyundai, before any evasive maneouvres "
        "can be taken. The only option is to fight, so you steel yourself and tell Terry 'I hope you've fought before, this won't be fun.'"
    )
    input("> ")
    # make Terry
    
    url = "https://www.dnd5eapi.co/api/2014/classes/barbarian"
    response = requests.get(url)
    classData = response.json()
    url = "https://www.dnd5eapi.co/api/2014/races/dragonborn"
    response = requests.get(url)
    raceData = response.json()
    create_character(party, classData, raceData, "Terry")
    
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
    name = input("> ").strip().title()
    if name == "":
        name = "Nameless One"

    url = "https://www.dnd5eapi.co/api/2014/classes"
    response = requests.get(url)
    data = response.json()
    for i in range(data['count']):
        print(data['results'][i]['name'])

    print("\nWhich class takes your fancy today? ")
    while True:
        choice = str(input("> ").strip().lower())
        if choice in [data['results'][i]['index'] for i in range(data['count'])]:
            break
        else:
            print("Invalid choice. Please select a class from the list.\n")
    url = f"https://www.dnd5eapi.co/api/2014/classes/{choice}"
    response = requests.get(url)
    classData = response.json()
    print()
    
    url = "https://www.dnd5eapi.co/api/2014/races"
    response = requests.get(url)
    data = response.json()
    for i in range(data['count']):
        print(data['results'][i]['name'])
        
    print("\nWhich race are you? ")
    while True:
        choice = str(input("> ").strip().lower())
        if choice in [data['results'][i]['index'] for i in range(data['count'])]:
            break
        else:
            print("Invalid choice. Please select a race from the list.\n")
    url = f"https://www.dnd5eapi.co/api/2014/races/{choice}"
    response = requests.get(url)
    raceData = response.json()

    print(f"\n{name} the mighty {raceData['name']} {classData['name']}! A wonderful choice.")
    print("\nYou have the following proficiencies and ability bonuses:")

    for i in range(len(classData['proficiencies'])):
        print(classData['proficiencies'][i]['name'])
    for i in range(len(raceData['ability_bonuses'])):
        print(f"+ {raceData['ability_bonuses'][i]['bonus']} to {raceData['ability_bonuses'][i]['ability_score']['name']}")

    print(raceData['language_desc'])
    # leave further customisation for now
    
    equipmentToAdd = []
    for item in classData['starting_equipment']: # even if the class doesnt have starting equipment, check
        for _ in range(item['quantity']):
            equipmentToAdd.append(item['equipment'])
    
    if 'starting_equipment_options' in classData:
        for optionSet in classData['starting_equipment_options']:
            print("\nYour current equipment is as follows:") # to give more info to player about what to choose
            for item in equipmentToAdd:
                print(item['name'])
            
            numChoices = optionSet['choose']
            print(f"Choose {numChoices} to add from the following list:")
            print(optionSet['desc'])
            
            for _ in range(numChoices):
                choice = str(input("> ").strip().lower())
                numChosen = ord(choice) - 97 # 0 for a, for example
                if 'options' not in optionSet['from'].keys(): # multiple options?
                    if optionSet['from']['option_set_type'] == "equipment_category":
                        choose_from_equipment_category(optionSet['from']['equipment_category']['url'], equipmentToAdd)
                else:
                    itemType = optionSet['from']['options'][numChosen]

                    if itemType['option_type'] == "counted_reference": # simple, add X of this item
                        for _ in range(itemType['count']):
                            itemToAdd = itemType['of']
                            equipmentToAdd.append(itemToAdd)
                    
                    elif itemType['option_type'] == "choice": # expand into a category to choose from
                        choose_from_equipment_category(itemType['choice']['from']['equipment_category']['url'], equipmentToAdd, itemType['choice']['choose'])
                
    
    party = Party()
    create_character(party, classData, raceData, name, equipmentToAdd) # create player character
    # setup done 
    
    print("\nYour character is ready! Your adventure is about to unfold...\n\n")
    beginAdventure(party)
    return

def create_character(party, classData, raceData, name, equipmentToAdd=None):
    if equipmentToAdd is None: # non-player character
        equipmentToAdd = []
        for item in classData['starting_equipment']: # even if the class doesnt have starting equipment, check
            for _ in range(item['quantity']):
                equipmentToAdd.append(item['equipment'])
        if 'starting_equipment_options' in classData: # some classes don't have this optional equipment, so check for it first
            for optionSet in classData['starting_equipment_options']:
                numChoices = optionSet['choose']
                
                for _ in range(numChoices):
                    itemType = optionSet['from']['options'][0]

                    if itemType['option_type'] == "counted_reference": # simple, add X of this item
                        for _ in range(itemType['count']):
                            itemToAdd = itemType['of']
                            equipmentToAdd.append(itemToAdd)
                    
                    elif itemType['option_type'] == "choice": # expand into a category to choose from
                        add_default_equipment_from_category(itemType['choice']['from']['equipment_category']['url'], equipmentToAdd, itemType['choice']['choose'])
    
    proficienciesToAdd = []
    for item in classData['proficiencies']: 
        proficienciesToAdd.append(item)
    
    # create ability scores
    scores = []
    for _ in range(6):
        rolls = []
        for _ in range(4):
            d6 = random.randint(1,6)
            rolls.append(d6)    
        rolls.remove(min(rolls))
        scores.append(sum(rolls))

    hp = classData['hit_die'] + math.floor((scores[2]-10)/2) # generate hp from constitution modifier and class hit die
    character = Character(name, classData, raceData, equipmentToAdd, proficienciesToAdd, scores[0], scores[1], scores[2], scores[3], 
                          scores[4], scores[5], math.floor(hp*1.5)) # +50% hp to be more generous
    print(f"{name} has the following equipment:")
    character.show_equipment()
    party.add_member(character)
    
    
if __name__ == "__main__":
    main()
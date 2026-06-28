import math
import random
import requests, pprint
from Party import Party
from Character import Character
from console_utils import cprint as print
import events

def choose_from_equipment_category(url, equipmentToAdd, numChoices=1):
    response = requests.get(f"https://www.dnd5eapi.co{url}")
    listData = response.json() # json of equipment choice data
    print(f"Choose {numChoices} to add from the following list:", style="bold yellow")
    for i in range(len(listData['equipment'])):
        print(f"{i+1}) {listData['equipment'][i]['name']}", style="green")

    for _ in range(numChoices):
        while True:
            try:
                choice = int(input("> ").strip())
                if 1 <= choice <= len(listData['equipment']):
                    itemToAdd = listData['equipment'][choice - 1]
                    equipmentToAdd.append(itemToAdd)
                    break
                else:
                    print(f"Please enter a number between 1 and {len(listData['equipment'])}", style="bold red")
            except ValueError:
                print(f"Please enter a number between 1 and {len(listData['equipment'])}", style="bold red")

def add_default_equipment_from_category(url, equipmentToAdd, numChoices):
    response = requests.get(f"https://www.dnd5eapi.co{url}")
    listData = response.json() # json of equipment choice data
    for i in range(numChoices):
        itemToAdd = listData['equipment'][i]
        equipmentToAdd.append(itemToAdd)

def get_equipment_options(optionSet):
    options = []

    if 'options' not in optionSet['from'].keys():
        # single equipment_category case (like the cleric's holy symbol)
        if optionSet['from']['option_set_type'] == "equipment_category":
            url = optionSet['from']['equipment_category']['url']
            response = requests.get(f"https://www.dnd5eapi.co{url}")
            listData = response.json()
            for item in listData['equipment']:
                display_name = item['name'][0].upper() + item['name'][1:] if item['name'] else item['name']
                options.append((display_name, {'option_type': 'category_item', 'of': item}))
    else:
        # multiple options case
        for item in optionSet['from']['options']:
            if item['option_type'] == "counted_reference":
                count = item['count']
                name = item['of']['name']
                # show "a name" for single-count items, otherwise number of items x name
                if count == 1:
                    display_name = f"a {name.lower()}"
                else:
                    display_name = f"{name} x {count}"
                display_name = display_name[0].upper() + display_name[1:] if display_name else display_name
                options.append((display_name, item))
            elif item['option_type'] == "choice":
                display_name = item['choice']['desc']
                display_name = display_name[0].upper() + display_name[1:] if display_name else display_name
                options.append((display_name, item))
            elif item['option_type'] == "multiple":
                # output the display name from the items in the multiple list - use choice descriptions for nested choices and "a NAME" for single counted items.
                item_descriptions = []
                for sub_item in item.get('items', []):
                    if sub_item['option_type'] == "counted_reference":
                        c = sub_item['count']
                        n = sub_item['of']['name']
                        if c == 1:
                            item_descriptions.append(f"a {n.lower()}")
                        else:
                            item_descriptions.append(f"{c} x {n}")
                    elif sub_item['option_type'] == "choice":
                        desc = sub_item['choice'].get('desc', '')
                        item_descriptions.append(desc)
                    elif sub_item['option_type'] == "multiple":
                        nested_parts = []
                        for nested in sub_item.get('items', []):
                            if nested['option_type'] == 'counted_reference':
                                nc = nested['count']
                                nn = nested['of']['name']
                                nested_parts.append(f"{nc} x {nn}" if nc > 1 else f"a {nn.lower()}")
                        if nested_parts:
                            item_descriptions.append(' and '.join(nested_parts))
                display_name = ' and '.join(item_descriptions)
                display_name = display_name[0].upper() + display_name[1:] if display_name else display_name
                options.append((display_name, item))

    return options




# start of game / setup
def main():
    print("\nWelcome to your grand adventure!", style="bold green")
    print("What is your name, adventurer? ")
    name = input("> ").strip().title()
    if name == "":
        name = "Nameless One"

    url = "https://www.dnd5eapi.co/api/2014/classes"
    response = requests.get(url)
    data = response.json()
    for i in range(data['count']):
        print(data['results'][i]['name'], style="magenta")

    print("\nWhich class takes your fancy today? ")
    while True:
        choice = str(input("> ").strip().lower())
        if choice in [data['results'][i]['index'] for i in range(data['count'])]:
            break
        else:
            print("Invalid choice. Please select a class from the list.\n", style="bold red")
    url = f"https://www.dnd5eapi.co/api/2014/classes/{choice}"
    response = requests.get(url)
    classData = response.json()
    print()
    
    url = "https://www.dnd5eapi.co/api/2014/races"
    response = requests.get(url)
    data = response.json()
    for i in range(data['count']):
        print(data['results'][i]['name'], style="magenta")
        
    print("\nWhich race are you? ")
    while True:
        choice = str(input("> ").strip().lower())
        if choice in [data['results'][i]['index'] for i in range(data['count'])]:
            break
        else:
            print("Invalid choice. Please select a race from the list.\n", style="bold red")
    url = f"https://www.dnd5eapi.co/api/2014/races/{choice}"
    response = requests.get(url)
    raceData = response.json()

    print(f"\n{name} the mighty {raceData['name']} {classData['name']}! A wonderful choice.", style="bold green")
    print(raceData['language_desc'])
    # leave further customisation for now
    
    equipmentToAdd = []
    for item in classData['starting_equipment']: # even if the class doesnt have starting equipment, check
        for _ in range(item['quantity']):
            equipmentToAdd.append(item['equipment'])
    
    if 'starting_equipment_options' in classData:
        for optionSet in classData['starting_equipment_options']:
            print("\nYour current equipment is as follows:")
            prevItem = ""
            dupeCount = 1
            for item in equipmentToAdd:
                if item != prevItem:
                    if prevItem != "":
                        if dupeCount > 1:
                            print(f" x{dupeCount}", style="yellow")
                        else:
                            print()
                    print(f"{item['name']}", style="bold", end='')
                    dupeCount = 1
                else:
                    dupeCount += 1
                prevItem = item
            if dupeCount > 1:
                print(f" x{dupeCount}", style="yellow")
            else:
                print()

            numChoices = optionSet['choose']
            print(f"\nChoose {numChoices} from the following:", style="bold yellow")

            availableOptions = get_equipment_options(optionSet)
            for i, (displayName, _) in enumerate(availableOptions, 1):
                print(f"{i}) {displayName}")

            for _ in range(numChoices):
                while True:
                    try:
                        choice = int(input("> ").strip())
                        if 1 <= choice <= len(availableOptions):
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(availableOptions)}", style="bold red")
                    except ValueError:
                        print(f"Please enter a number between 1 and {len(availableOptions)}", style="bold red")

                chosenOption = availableOptions[choice - 1][1]

                if chosenOption['option_type'] == "counted_reference":
                    for _ in range(chosenOption['count']):
                        itemToAdd = chosenOption['of']
                        equipmentToAdd.append(itemToAdd)

                elif chosenOption['option_type'] == "multiple":
                    for newItem in chosenOption.get('items', []):

                        if newItem['option_type'] == 'counted_reference':
                            for _ in range(newItem['count']):
                                itemToAdd = newItem['of']
                                equipmentToAdd.append(itemToAdd)

                        elif newItem['option_type'] == 'choice':
                            choice_info = newItem['choice']

                            if choice_info['from']['option_set_type'] == 'equipment_category':
                                choose_from_equipment_category(choice_info['from']['equipment_category']['url'], equipmentToAdd, choice_info['choose'])

                            elif 'options' in choice_info['from']:
                                nested_options = get_equipment_options({'from': choice_info['from']})
                                for i, (dname, _) in enumerate(nested_options, 1):
                                    print(f"{i}) {dname}")
                                nested_choose = choice_info.get('choose', 1)
                                for _ in range(nested_choose):
                                    while True:
                                        try:
                                            nchoice = int(input("> ").strip())
                                            if 1 <= nchoice <= len(nested_options):
                                                break
                                            else:
                                                print(f"Please enter a number between 1 and {len(nested_options)}", style="bold red")
                                        except ValueError:
                                            print(f"Please enter a number between 1 and {len(nested_options)}", style="bold red")
                                    sel = nested_options[nchoice-1][1]

                                    if sel['option_type'] == 'counted_reference':
                                        for _ in range(sel['count']):
                                            equipmentToAdd.append(sel['of'])
                                    elif sel['option_type'] == 'category_item':
                                        equipmentToAdd.append(sel['of'])
                                    elif sel['option_type'] == 'choice':
                                        choose_from_equipment_category(sel['choice']['from']['equipment_category']['url'], equipmentToAdd, sel['choice']['choose'])

                        elif newItem['option_type'] == 'multiple':
                            for nested in newItem.get('items', []):
                                if nested['option_type'] == 'counted_reference':
                                    for _ in range(nested['count']):
                                        equipmentToAdd.append(nested['of'])

                elif chosenOption['option_type'] == "choice":
                    choose_from_equipment_category(chosenOption['choice']['from']['equipment_category']['url'], equipmentToAdd, chosenOption['choice']['choose'])
                elif chosenOption['option_type'] == "category_item":
                    equipmentToAdd.append(chosenOption['of'])
                
    
    party = Party()
    create_character(party, classData, raceData, name, equipmentToAdd) # create player character
    # setup done 
    
    print("\nYour character is ready! The adventure is about to unfold...\n\n", style="bold green")
    events.beginAdventure(party)
    return

def create_character(party, classData, raceData, name, equipmentToAdd=None):
    proficienciesToAdd = []
    for item in classData['proficiencies']: 
        proficienciesToAdd.append(item)
    
    url = f"https://www.dnd5eapi.co/api/2014/races/{raceData['index']}/proficiencies"
    profData = requests.get(url).json()
    if profData['count'] > 0:
        proficienciesToAdd.extend(result for result in profData['results'] if result not in proficienciesToAdd)
        
    # add equipment if None...
    if equipmentToAdd is None: # non-player character
        equipmentToAdd = []
        for item in classData['starting_equipment']: # even if the class doesnt have starting equipment, check
            for _ in range(item['quantity']):
                equipmentToAdd.append(item['equipment'])
        if 'starting_equipment_options' in classData: # some classes don't have this optional equipment, so check for it first
            for optionSet in classData['starting_equipment_options']:
                numChoices = optionSet['choose']
                
                for _ in range(numChoices):
                    if "options" not in optionSet['from'].keys(): # like cleric holy symbol
                        add_default_equipment_from_category(optionSet['from']['equipment_category']['url'], equipmentToAdd, optionSet['choose'])
                    else:
                        itemType = optionSet['from']['options'][0]
                        
                        if itemType['option_type'] == "counted_reference": # simple, add X of this item
                            for _ in range(itemType['count']):
                                itemToAdd = itemType['of']
                                equipmentToAdd.append(itemToAdd)
                        
                        elif itemType['option_type'] == "choice": # expand into a category to choose from
                            add_default_equipment_from_category(itemType['choice']['from']['equipment_category']['url'], equipmentToAdd, itemType['choice']['choose'])
    else:
        print("\nYou have the following proficiencies and ability bonuses:") # tell the player character proficiencies
        for prof in proficienciesToAdd:
            print(prof['name'])
        for i in range(len(raceData['ability_bonuses'])):
            print(f"+ {raceData['ability_bonuses'][i]['bonus']} to {raceData['ability_bonuses'][i]['ability_score']['name']}")

    
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
                          scores[4], scores[5], max(10,math.floor(hp*1))) # +50% hp to be more generous, lowest is 10hp
    print(f"\n{name} has the following equipment:")
    character.show_equipment()
    party.add_member(character)
        
if __name__ == "__main__":
    main()
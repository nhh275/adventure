import math
import random
import requests, pprint
from Party import Party
from Character import Character
import battles
from console_utils import cprint as print

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

def beginAdventure(party):
    print(
        "\nYour adventure begins in the magical city of Swindon, where you find yourself on the side of a road sparsely populated by vehicles. "
        "It is a calm day, with the regular clouds scattered across the sky and no sun to be seen, as is typical for this land. "
        "Your ponderance is interrupted by the sound of a car drawing near, its engine rumbling as it slows its approach.",
        style="cyan"
    )
    input("> ")
    print(
        "\nFrom within the vehicle and through a crack in the window shouts a voice, 'Excuse me! Do you live here? I need some help navigating this area - "
        "do you understand the Magic Roundabout?' The window is rolled down further to reveal a man of staggering size - a height that makes you wonder how "
        "such an individual could even fit in a Hyundai i10, let alone drive it comfortably.",
        style="cyan"
    )
    input("> ")
    print("\nPutting your bewilderment aside, you must say something in response. Do you help? (yes/no)", style="bold cyan")
    choice = input("> ").strip().lower()
    if choice == "yes" or choice == "y":
        print(
            "\nYou offer to help the man and he slows the vehicle to a stop beside you on the double yellow lines, flashing his emergency lights. "
            "You attempt to explain the wonder of the Roundabout, but its mystery is too complex, and he ends up inviting you into the passenger seat for a "
            "more direct guide. You are tentative to accept, but remember that you've been trying to work on your bravery lately, so you hop in and buckle up.",
            style="cyan"
        )
        input("> ")
        roundabout(party)
    else:
        print("\nYou shrug, mumbling something about just visiting, and leave the way hulking unit in disappointment, continuing on your path into the city.", style="cyan")
        input("> ")
        city(party)
    return

def roundabout(party):
    print(
        "\nWhen you enter, the man introduces himself as Terry and explains that he's been stuck here for hours, desperate for some help. "
        "On closer inspection, you see reptilian scales on his neck and hands - this is no regular human, but you feel safe nonetheless. "
        "You drive in relative peace until you see the great sign for the Magic Roundabout up ahead. "
        "As you approach, you sense Terry's nerves rising, sweat dripping down his face as he prepares to challenge the Roundabout with you by his side.",
        style="cyan"
    )
    input("> ")
    print(
        "\nYou are about to enter the start of the Roundabout, when all of a sudden, the boot of the following car flies open, giving way to a collection of "
        "what you can only assume to be goblins from some sort of fantasy world. The creatures leap out and mob the Hyundai, before any evasive maneouvres "
        "can be taken. The only option is to fight, so you steel yourself and tell Terry 'I hope you've fought before, this won't be fun.'",
        style="cyan"
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
    resultTuple = battles.goblins(party)
    if not resultTuple[0]:
        return
    party.give_xp(resultTuple[1]) # list of xp from enemies to add to party members
    party.heal_party()
    print(
        "\nFollowing your great victory, you pause in the traffic created by the commotion to rest and heal your wounds. "
        "Others around you seem to be relatively unfazed by what you've been through, as if this is just a regular occurrence in Swindon, and the car in front eventually drives off to "
        "the Roundabout anyways. Feeling a little shaken but rested, you decide to continue on, and pray that you are unbothered for the rest of your trip.",
        style="cyan"
    )
    input("> ")
    print(
        "\nYou navigate Terry through the Magic Roundabout. He can't tell that you don't really know what you're doing, though you've always been a good actor. "
        "The roads are perilous, with other drivers clearly distressed as they attempt to survive the beast that calls Swindon home, but in the end you come out of it alive. "
        "The two of you are now faced with the main street into the city centre, and Terry thanks you graciously for your help.",
        style="cyan"
    )
    input("> ")
    print(
        "\nHe asks you if you have any plans for the day, and when you reply with a 'no', he offers to spend some time with you in the city, suggesting various places to go. "
        "You feel quite comfortable with Terry by now, so you agree and think about what you would like to do today.",
        style="cyan"
    )
    input("> ")
    
    print("\nWhere would you like to go?\n1) Supermarket\n2) Cathedral\n3) Park", style="bold yellow")
    choice = 0
    while True:
        try:
            choice = int(input("> ").strip())
            if choice <= 3 and choice > 0: # check both conditions here
                break
            else:
                print("Invalid choice. Please select a new location with the numbers on the left.\n", style="bold red") # input is int but invalid
        except:
            print("Invalid choice. Please select a new location with the numbers on the left.\n", style="bold red") # input is not int
    
    match choice:
        case 1:
            supermarket(party)
        case 2:
            cathedral(party)
        case 3:
            park(party)

def city(party):
    print("\nAs you amble on, the heights of the city loom in front of you. The usual sights can be seen - houses, shops, a grand cathedral - but what surprises you most "
          "is the number of enormous car parks, both multi-level and sprawling across flat land. You consider what could possibly bring so many drivers to the city that "
          "appears to you as so lacklustre and even dangerous, but your thoughts are interrupted by a noise completely unexpected in such an environment.", style="cyan")
    input("> ")
    print("\nYou flick your head round and are taken aback by what you see standing there: a human skeleton completely devoid of flesh! It appears to be the source of the "
          "clanking sound, which emanates from its hollow body as it shifts in place. Looking down at it, its eyes turn red, piercing into your soul, and it charges you!", style="cyan")
    input("> ")
    
    resultTuple = battles.skeleton(party)
    if not resultTuple[0]:
        return
    party.give_xp(resultTuple[1]) # list of xp from enemies to add to party members
    party.heal_party()
    
    print(
        "\nFollowing your great victory, you pause by the roadside to rest and heal your wounds. "
        "Others in the area seem to be relatively unfazed by what you've been through, as if this is just a regular occurrence in Swindon, as they continue with their days. "
        "Feeling a little shaken but rested, you decide to continue on, and pray that you are unbothered for the rest of your trip.",
        style="cyan"
    )
    input("> ")
    print(
        "\nYou follow the path down to the city, and end up facing the main street into the centre of town. "
        "Now that you're past all that trouble, you ponder what you really came to Swindon today for."
    , style="cyan")
    input("> ")
    
    print("\nWhere would you like to go?\n1) Supermarket\n2) Cathedral\n3) Park", style="bold yellow")
    choice = 0
    while True:
        try:
            choice = int(input("> ").strip())
            if choice <= 3 and choice > 0: # check both conditions here
                break
            else:
                print("Invalid choice. Please select a new location with the numbers on the left.\n", style="bold red") # input is int but invalid
        except:
            print("Invalid choice. Please select a new location with the numbers on the left.\n", style="bold red") # input is not int
    
    match choice:
        case 1:
            supermarket(party)
        case 2:
            cathedral(party)
        case 3:
            park(party)

def supermarket(party):
    pass

def cathedral(party):
    pass

def park(party):
    pass


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
    beginAdventure(party)
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
                          scores[4], scores[5], max(10,math.floor(hp*1.5))) # +50% hp to be more generous, lowest is 10hp
    print(f"\n{name} has the following equipment:")
    character.show_equipment()
    party.add_member(character)
        
if __name__ == "__main__":
    main()
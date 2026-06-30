import requests, pprint
import battles, main
from console_utils import cprint as print
from game_data import game_data
# story events, in chronological order 

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
    print("\nPutting your bewilderment aside, you must say something in response. Do you help? (yes/no)", style="bold cyan") # choice 1
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
    

    classData = game_data.get_class("barbarian")
    raceData = game_data.get_race("dragonborn")
    main.create_character(party, classData, raceData, "Terry")
    
    # time to scrap 
    resultTuple = battles.battle(party, surprise=0, enemyIndex="goblin", numEnemiesLower=2, numEnemiesHigher=3)
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
    choice2(party)

def city(party):
    print("\nAs you amble on, the heights of the city loom in front of you. The usual sights can be seen - houses, shops, a grand cathedral - but what surprises you most "
          "is the number of enormous car parks, both multi-level and sprawling across flat land. You consider what could possibly bring so many drivers to the city that "
          "appears to you as so lacklustre and even dangerous, but your thoughts are interrupted by a noise completely unexpected in such an environment.", style="cyan")
    input("> ")
    print("\nYou flick your head round and are taken aback by what you see standing there: a human skeleton completely devoid of flesh! It appears to be the source of the "
          "clanking sound, which emanates from its hollow body as it shifts in place. Looking down at it, its eyes turn red, piercing into your soul, and it charges you!", style="cyan")
    input("> ")
    
    resultTuple = battles.battle(party, surprise=0, enemyIndex="skeleton", numEnemiesLower=1)
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
    choice2(party)


def choice2(party): # same choice after the Goblins and Skeleton fight pathways, DRY
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
    print(
        "\nYou decide you need to pick up some things while you're in town, so you pop in to the closest shop. Finding yourself in a Lidl, the best of all supermarket chains, you "
        "feel gleeful and prepared to tackle any further challenges that come your way. The immense supply of products of all kinds, from rice to lawnmowers to frozen pizza, fills your "
        "heart with joy as you wander the aisles.",
        style="cyan"
    )
    input("> ")
    print(
        "\nDuring your time in the shop, you can't help but find yourself drawn to the sweet smell of freshly baked pastries emanating from a corner of the room. The Lidl Bakery, one of "
        "the greatest creations God blessed her people with, now stands in front of you, inviting you to grab a bag and select some lovely treats for a very affordable price. You feel in "
        "this moment perhaps the happiest you ever have, despite your troubles earlier in the day, basking in the glow of croissants, pastéis de nata, and delectable pains au chocolat.",
        style="cyan"
    )
    party.give_xp([50]) # lidl xp, it's wonderful
    input("> ")
    print(
        "\nWhen you're done shopping, you amble up to the checkout, but something strikes you as peculiar about the cashier - something is... off. As you progress up the checkout line, "
        "you attempt to study their face and behaviour more deeply, trying to ascertain if there is a threat present, or this is simply a random feeling.",
        style="cyan"
    )
    input(">")
    player = party.members[0]
    check = player.ability_check(player.get_bonus(player.wisdom),10) # roll for perception with DC 10 (easy)
    if check: # successful perception
        print(
            "\nUpon further examination, you are alarmed to find out the cashier is actually a terrifying ghoul! The evil being does not realises it's been rumbled, so as it continues to "
            "scan groceries, you decide to be brave and jump it from across the conveyor, taking the monster by surprise!",
            style="cyan"
        )
        input("> ")
        resultTuple = battles.battle(party, surprise=2, enemyIndex="ghoul", numEnemiesLower=1) # enemies surprised
    else: # could not perceive anything
        print(
            "\nYou do not find anything wrong with the cashier, so you make idle small talk with them as is your duty as a British citizen, mentioning the terrible weather and so on. "
            "You pay and turn away, ready to leave the shop, when you are suddenly struck from behind and knocked onto the floor! It turns out this mysterious checkout employee is "
            "actually a horrifying ghoul!",
            style="cyan"
        )
        input(">")
        resultTuple = battles.battle(party, surprise=1, enemyIndex="ghoul", numEnemiesLower=1) # team surprised
    
    if not resultTuple[0]:
        return
    party.give_xp(resultTuple[1]) # list of xp from enemies to add to party members
    party.heal_party()
        
def cathedral(party):   
    print(
        "\nYou decide to visit the beautiful cathedral that takes up centre stage in the city. As you enter through the grand front door, you are stunned by the breathtaking architecture "
        "and stained glass windows. The building must be centuries old, and you can't help but wonder about what these walls have withstood and been home to over the years.",
        style="cyan"
    )
    input("> ")
    print(
        "\nDeep in contemplation, you are approached by a person clad in peculiarly black religious attire who introduces themselves as a priest who works at the cathedral. You're surprised "
        "to learn that there are still regular services occurring in such a historic place, and you're told all about the wonderful lore behind the building. The priest offers you their name, " 
        "Raven, and inquires about the reason for your visit - to both the city and their workplace.",
        style="cyan"
    )
    input(">")
    print(
        "\nWhen you enlighten Raven about your earlier experience in combat, they seem to pay extra attention to you, but do not seem especially alarmed. You feel as if you are being "
        "studied, like the priest is scrutinising your expressions as you regale them with your tale, but you try to act unbothered and continue as normal.",
        style="cyan"
    )
    input(">")
    player = party.members[0]
    check = player.ability_check(player.get_bonus(player.charisma),10) # roll for acting with DC 10 (easy)
    if check: # success
        print(
            "\nRaven seems pleased by your heroism, and pauses in thought before responding to you. With a gentle nod, they say 'Hmm, yes. You're perfect...' and trail off. You are "
            "reasonably taken aback by these words, and ask the priest to elaborate. 'You seem a great warrior, fit to handle a tremendous burden that has been plaguing our city.' "
            "You were not expecting to hear this during a touristic visit to a cathedral, but are intrigued nonetheless, and demand further details.",
            style="cyan"
        )
        input("> ")
        print(
            "\nThe priest was impressed by your story, and granted you a level up!", style="bold green"
        )
        party.level_party_up()
    else:
        print(
            "\nYou feel yourself clam up as the nerves of being intensely observed get to you. Mumbling through the end of your encounter, Raven sports a mild grimace and a shrug. "
            "'I suppose you'll do', they say, rightfully confusing you and provoking you to ask 'What does that mean?'. The priest elaborates, talking of an 'awful monster spreading "
            "evil through the city', and it seems that they have designated you as the warrior to stave it off.",
            style="cyan"
        )
        input(">")
    
    print(
        "\nRaven tells you all you need to know, and you have little choice but to accept this quest that has been thrust upon you. They attempt to guide you on where to go and what to "
        "do next, but since you're no local, the directions are of little help. In the end, the priest offers to join your party in this grand adventure to save the city of Swindon.",
        style="cyan"
    )
    input("> ")

    classData = game_data.get_class("cleric")
    raceData = game_data.get_race("elf")
    main.create_character(party, classData, raceData, "Raven")
    party.get_member_by_name("Raven").check_level_up(freeLevel=True) # start Raven at lv2, lets user choose what ability to level up

def park(party):
    print(
        "\nPlaceholder. "
        "Here.",
        style="cyan"
    )
    input("> ")
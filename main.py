import os
import time
from PIL import Image


#################################################################################################

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Display title screen
# TODO uncomment when done testing
# def prompt():
#     print("---------------- Welcome to Beer Delivery Service \U0001F642 Nice to have you ----------------\n\n"
#           "Pay attention to the words in all CAPS.\n\n"
#           "If you end up getting stuck, you can type 'help' to learn various "
#           "commands that may be useful.\n\n"
#           "Have fun and good luck (it ain't hard... yet)!")
#     time.sleep(8)
#     clear()


def handle_help():
    print('Commands:\n'
          'CLEAR -- Clear screen\n'
          'GIVE -- Opens a menu to give an item to someone\n'
          'GO (DIRECTION/ROOM NAME) -- Go a direction\n'
          'INVENTORY -- Shows what you\'re carrying\n'
          'LOOK (OBJECT/DIRECTION) -- Look around, look at an object, etc\n'
          'MAP -- Shows the map\n'
          'TAKE (ITEM) -- Take an item\n'
          'TALK (PERSON) -- Talk to someone\n'
          'USE (OBJECT) -- Use an object')


def handle_open(noun, current_room, rooms, containers, vowels):
    if noun == "":
        print("You need to be more specific.")
    # if the room has a container in it and that container matches the input
    elif 'container' in rooms[current_room].keys() and rooms[current_room]["container"] == noun.lower():
        container_open = containers[noun]["open"]
        container_locked = containers[noun]['locked']
        # if the container is both unlocked and unopened, it will do the following
        if container_locked == 'no' and container_open == 'no':
            # container is now set to open
            containers[noun]["open"] = 'yes'
            rooms[current_room]["item"] = containers[noun]["item"]
            # goes through rooms{} and checks to see if there are any items
            if 'item' in rooms[current_room].keys():
                nearby_item = rooms[current_room]["item"]
                # if the last character of the item is an 's' (as in a plural item)
                if nearby_item[-1] == 's':
                    print(f'You open the {noun} and see {nearby_item.upper()}')
                # else if the first letter of the item is a vowel
                elif nearby_item[0] in vowels:
                    print(f'You open the {noun} and see an {nearby_item.upper()}')
                # else if the item is singular and starts with a consonant
                else:
                    print(f'You open the {noun} and see a {nearby_item.upper()}')
        elif container_locked == 'yes':
            print(f'The {noun} is locked. Maybe I should find a key...')
        elif container_open == 'yes':
            print(f'The {noun} is already open, dumb dumb.')
    else:
        print(f'You don\'t see a {noun} to open.')


def handle_close(noun, current_room, rooms, containers):
    if noun == "":
        print("You need to be more specific.")
    # if the room has a container in it and that container matches the input
    elif 'container' in rooms[current_room].keys() and rooms[current_room]["container"] == noun.lower():
        container_open = containers[noun]["open"]
        # if the container is both unlocked and unopened, it will do the following
        if container_open == 'yes':
            containers[noun]["open"] = 'no'
            try:
                del rooms[current_room]["item"]
                print(f'You close the {noun}')
            except KeyError:
                print(f'You don\'t see a {noun} to close.')
    else:
        print(f'You don\'t see a {noun} to close.')


def handle_go(noun, currentRoom, rooms):
    # declares current_room as global to modify it
    global current_room
    if noun == '':
        print("You need to be more specific.")
    else:
        # iterates through the keys of rooms and checks for tuples using isinstance()
        # e.g. ('left', 'west'): 'kitchen'
        # if there is a tuple, then it sets the current_room to the value of that tuple
        for key, value in rooms[currentRoom].items():
            if isinstance(key, tuple) and noun in key:
                current_room = value
                game_state["current_room"] = current_room
                return
        # if there is no tuple, it sets the current room like before
        if noun in rooms[currentRoom].keys():
            current_room = rooms[currentRoom][noun]
            game_state["current_room"] = current_room
        else:
            print('I can\'t go that way.')


def handle_talk(noun, current_room, rooms, dialogue):
    if noun == "":
        print("You need to be more specific.")
    # goes through rooms, checks to see if there's any npc's and checks if the input is a valid npc
    elif 'npc' in rooms[current_room].keys() and rooms[current_room]["npc"] == noun.lower():
        # gets the npc's dialogue
        npc_name = rooms[current_room]["npc"]
        npc = dialogue.get(npc_name)

        if npc:
            print(f'\n{npc["greeting"]}')

            while True:
                # prints the dialogue menu in a numbered list
                for index, question in enumerate(npc["questions"].keys(), start=1):
                    print(f'[{index}] {question}')
                print('[9] Exit\n')
                try:
                    choice_index = int(input('> '))
                    # if they choose 9, it clears the console, prints the description, and breaks the loop
                    if choice_index == 9:
                        clear()
                        print(rooms[current_room]["description"])
                        break
                    # if they choose an actual option, it prints the value of the key
                    if 1 <= choice_index <= len(npc["questions"]):
                        question_key = list(npc["questions"].keys())[choice_index - 1]
                        print(f'{npc["questions"][question_key]}\n')
                    else:
                        print('Invalid choice. Enter a number from the menu above.')
                except ValueError:
                    print("Invalid input. Please enter a number from the menu above.")
    else:
        print(f"There's no one here to talk to named {noun.capitalize()}.")


def handle_take(noun, current_room, rooms, game_state):
    inventory = game_state["inventory"]

    if noun == "":
        print("You need to be more specific.")
    elif 'item' in rooms[current_room].keys() and rooms[current_room]["item"] == noun.lower():
        inventory.append(rooms[current_room]["item"])
        print(f'You take the {noun}.')
        del rooms[current_room]["item"]
    else:
        print(f'You look around and you don\'t see one of those.')


def handle_use(noun, current_room, rooms, containers, game_state):
    inventory = game_state["inventory"]

    if noun == "bed":
        if game_state["beer_delivered"]:
            print('You rest your weary, beer-delivering eyes. '
                  'You wake up the next day, ready for whatever may lie ahead.\n\n'
                  'GAME OVER')
            time.sleep(10)
            exit()
        else:
            print('It isn\'t sleepy time yet, dad need his beer!')
    elif noun == "cigar key":
        if noun in inventory:
            print("What do you want to use the key on?")
            use_key_on = input("> ").lower()
            if use_key_on == 'cigar case':
                if use_key_on in rooms[current_room]["object"]:
                    inventory.remove(noun)
                    containers[use_key_on]["locked"] = "no"
                    print(f"You unlocked the {use_key_on}.")
                else:
                    print(f"There is no {use_key_on} to use that on.")
            else:
                print(f"That key doesn't open {use_key_on}")
        else:
            print("You don't have a cigar key.")
    else:
        print('Nothing interesting happens.')


def handle_give(noun, current_room, rooms, game_state, npcs, dialogue):
    successful_give = False
    inventory = game_state["inventory"]
    npc_name = rooms[current_room]["npc"]
    npc = dialogue.get(npc_name)

    # If noun is empty, prompt the user for an item
    if noun == "":
        if not inventory:
            print("You don't have any items to give.")
        else:
            while not successful_give:
                print("What do you want to give?")
                print(f'Inventory: {", ".join(inventory)}')
                item = input("> ").lower()
                if item == 'back':
                    break
                elif item in inventory:
                    inventory.remove(item)
                    while True:
                        print(f"Who do you want to give the {item} to?")
                        next_noun = input('> ').lower()
                        if 'npc' in rooms[current_room].keys() and rooms[current_room]["npc"] == next_noun:
                            npc_name = rooms[current_room]["npc"]
                            npc = npcs.get(npc_name)

                            # Check if the item is required by the NPC
                            if npc and item in npcs[npc_name]["required_items"]:
                                # update the game state when the beer is delivered
                                game_state["beer_delivered"] = True
                                # updates the flag so the loop can break
                                successful_give = True
                                # quest success dialogue
                                print(dialogue[npc_name]['give_response'])
                                # clears the terminal after 3-second delay
                                time.sleep(3)
                                clear()
                                # prompt to go to bed
                                print('Boy I sure am beat from all that gathering. Time to go to bed.')
                                break
                        else:
                            print(f"{next_noun.capitalize()} isn't here to give {item} to.")
                else:
                    print(f"You don't have {item}.")


def handle_look_around(current_room, rooms):
    print(rooms[current_room]["description"])


def handle_look_obj(noun, current_room, rooms, game_state):
    try:
        # Use the game_state dictionary to check if the beer has been delivered
        if noun in rooms[current_room]["object"]:
            if noun == 'bed':
                # Check if beer has been delivered using the game_state dictionary
                if not game_state["beer_delivered"]:
                    print('The bed looks mad comfy but it isn\'t time for sleep yet! '
                          'I still need to get dad his beer.')
                else:
                    print(rooms[current_room]["object"][noun])
            else:
                print(rooms[current_room]["object"][noun])
    except KeyError:
        print(f"I don't see a {noun} to look at.")


def handle_inventory(game_state):
    inventory = game_state["inventory"]

    # checks if inventory is empty
    if not inventory:
        print('You aren\'t carrying anything.')
    else:
        print(f'Inventory: {", ".join(inventory)}')


def handle_map():
    folder_path = "map_files"  # Specify the folder path where the map images are located
    image_path = os.path.join(folder_path, f'{current_room}.png')
    try:
        Image.open(image_path).show()
        print('Pulling out the map.')
    except FileNotFoundError:
        print(f"Map image for {current_room} not found.")


#################################################################################################

game_state = {
    'beer_delivered': False,
    'inventory': [],
    'current_room': 'living room'
}

containers = {
    'fridge': {
        'open': 'no',
        'locked': 'no',
        'item': 'beer'
    },
    'cigar case': {
        'open': 'no',
        'locked': 'yes',
        'item': 'cigar'
    }
}

# list of npcs to handle if they have their proper quest items
npcs = {
    'dad': {
        'required_items': ['beer'],
        'item_delivered': False
    },
    ####################################################
    'bernard': {
        'required_items': ['dog food'],
        'item_delivered': False
    }
}

rooms = {
    'living room': {
        'description': 'You\'re in your living room. DAD is on the couch watching TV.\n'
                       'The KITCHEN is to your LEFT and the HALLWAY is to the RIGHT. '
                       'BEHIND you is the door going out to the FRONT YARD',
        ('back', 'behind', 'front yard'): 'front yard',
        ('left', 'kitchen'): 'kitchen',
        ('right', 'hallway'): 'hallway',
        'npc': 'dad',
        'item': 'beer',
        'object': {
            'around': 'There\'s probably half a case of empty Miller Light cans '
                      'on the ottoman and another 3 on the table next to Dad.',
            'dad': 'He looks pretty hammered.',
            'tv': 'Dad\'s watching Tucker Carlson\'s podcast. His favorite.'
        }
    },
    ####################################################
    'hallway': {
        'description': 'You stop in the hallway, contemplating if you want to go '
                       'LEFT, to your BEDROOM, or RIGHT, to the STUDY. A hard choice, you know.',
        ('left', 'bedroom'): 'bedroom',
        ('right', 'study'): 'study',
        ('back', 'behind', 'living room'): 'living room',
        'object': {
            'around': '',
            'bedroom': '',
            'study': '',
        }
    },
    ####################################################
    'study': {
        'description': 'You enter Dad\'s study. Around you is a DESK where Dad reads his books, '
                       'a few SHELVES where he keeps those books, and a MINI-FRIDGE where he keeps his '
                       'more expensive alcohol.',
        ('back', 'behind', 'hallway'): 'hallway',
        'container': 'cigar case',
        'object': {
            'around': 'Dad\'s study. I don\'t know what he studies, but what I do know is that '
                      'I\'m not usually allowed in here. This time, however, duty calls.',
            'desk': 'On Dad\'s desk you see the story he is currently reading, "The Beast in the Cave." '
                    'You also see some sort of BOX',
            'box': 'You read the lid of the box. "Fine Blend Cigars." This must be Dad\'s CIGAR CASE.',
            'mini-fridge': '',
            'shelf': '',
            'shelves': '',
            'cigar case': ''
        },
    },
    ####################################################
    'bedroom': {
        'description': 'Your room is pretty tidy. You see your BED. It looks pretty damn comfy.',
        ('left', 'living room'): 'living room',
        ('back', 'behind', 'hallway'): 'hallway',
        'object': {
            'around': 'You have RuneScape posters and Star Wars legos hanging on your wall... Sick.',
            'bed': 'I could really go for a rest about now.'
        }
    },
    ####################################################
    'kitchen': {
        'description': 'In the kitchen, you can smell something cooking on the STOVE. '
                       'Around you is the FRIDGE. '
                       'STRAIGHT ahead leads the the BACKYARD and the LIVING ROOM is to the RIGHT.',
        ('right', 'living room'): 'living room',
        ('straight', 'forward', 'backyard'): 'backyard',
        'container': 'fridge',
        'object': {
            'around': 'The fridge is slightly ajar, probably from when dad went to get his last beer.',
            'stove': 'You look inside the pots and pans and it looks like a shrimp is frying some rice.',
            'fridge': 'I think Dad said something about getting him something out of here.'
        }
    },
    ####################################################
    'front yard': {
        'description': 'Out in the front yard, you see MOM diligently doing yard work. '
                       'She is tending to her GARDEN, watering the FLOWERS.',
        ('back', 'behind', 'living room'): 'living room',
        'npc': 'mom',
        'object': {
            'around': 'Mom\'s flowers make the front yard really ',
            'mom': '',
            'garden': '',
            'flowers': '',
        }
    },
    ####################################################
    'backyard': {
        'description': 'Out back, this is where you and BERNARD like to play. '
                       'You look about and see BERNARD in the DOGHOUSE and you also see the SHED.',
        ('back', 'behind', 'kitchen'): 'kitchen',
        'shed': 'shed',
        'npc': 'bernard',
        'object': {
            'around': '',
            'doghouse': '',
            'shed': '',
            'flowers': '',
        }
    },
    ####################################################
    'shed': {
        'description': '',
        ('back', 'behind', 'backyard'): 'backyard',
        'object': {
            'around': '',
            'obj1': '',
            'obj2': '',
            'obj3': '',
        }
    }
}

dialogue = {
    'dad': {
        'greeting': 'Hey son, can you fetch me that BEER in the FRIDGE? '
                    'It\'s next to the leftovers. I\'m absolutely parched.',
        'give_response': 'Thanks son, I always liked you the best.',
        'questions': {
            'How are you?': 'I\'m great. Just watching Tuck and drinking my Millers. What else could I ask for?',
            'What are you doing?': 'Just kicking back. I still have the whole day ahead of me.',
            'Do you need anything?': 'Yeah, actually. I would love that BEER I just mentioned if you wouldn\'t mind.'
        }
    },
    ####################################################
    'mom': {
        'greeting': '',
        'questions': {
            'What are you doing?': '',
            'Do you need anything?': '',
        }
    },
    ####################################################
    'bernard': {
        'greeting': '',
        'questions': {
            'What are you doing?': '',
            'Do you need anything?': '',
        }
    },
}

#################################################################################################

# tracks current room
current_room = game_state['current_room']

# list of vowels
vowels = ['a', 'e', 'i', 'o', 'u']

# TODO uncomment when done testing
# prompt()
previous_room = current_room
print(rooms[current_room]["description"])

#################################################################################################

# gameplay loop
while True:
    beer_delivered = False
    # this prevents the room descript from printing after every action
    if current_room != previous_room:
        clear()
        print(rooms[current_room]["description"])
        previous_room = current_room

    user_in = input('> ')

    # split input on the first whitespace to separate the verb and the remaining input
    split_input = user_in.strip().split(' ', 1)

    # check if there is a verb and noun
    if len(split_input) == 2:
        verb, noun = split_input
        verb = verb.lower()
        noun = noun.lower()
    # if there's no whitespace in the input, the user might have only entered a verb
    else:
        verb = user_in.strip().lower()
        noun = ""

    if verb.lower() == 'exit':
        print("Exiting the game. Goodbye!")
        break
    elif verb.lower() == 'open':
        handle_open(noun, current_room, rooms, containers, vowels)
    elif verb.lower() == 'close':
        handle_close(noun, current_room, rooms, containers)
    elif verb.lower() == 'talk':
        handle_talk(noun, current_room, rooms, dialogue)
    elif verb.lower() == 'take':
        handle_take(noun, current_room, rooms, game_state)
    elif verb.lower() == 'give':
        handle_give(noun, current_room, rooms, game_state, npcs, dialogue)
    elif verb.lower() == 'go':
        handle_go(noun, current_room, rooms)
    elif verb.lower() == 'inventory':
        handle_inventory(game_state)
    elif verb.lower() == 'look':
        if noun == '':
            handle_look_around(current_room, rooms)
        else:
            handle_look_obj(noun, current_room, rooms, game_state)
    elif verb.lower() == 'use':
        handle_use(noun, current_room, rooms, containers, game_state)
    elif verb.lower() == 'help':
        handle_help()
    elif verb.lower() == 'clear':
        clear()
    elif verb.lower() == 'map':
        handle_map()
    else:
        print("I don't understand what you want me to do.")

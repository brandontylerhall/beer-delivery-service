import os
import time
from PIL import Image

#################################################################################################

################################################################################################

game_state = {
    'all_items_delivered': False,
    'has_visited_study': False,
    'talk_dad_after_study': False,
    'cigar_case_unlocked': False,
    'items_required': ['beer', 'cigar',],
    'items_delivered': [],
    # FIXME empty inventory
    'inventory': ['beer', 'cigar',],
    # FIXME set current_room to living room
    'current_room': 'living room',
}

containers = {
    'fridge': {
        'open': 'no',
        'locked': 'no',
        'item': 'beer'
    },
    'tuff box': {
        'open': 'no',
        'locked': 'no',
        'item': 'cigar key'
    },
    'cabinet': {
        'open': 'no',
        'locked': 'no',
        'item': 'dog food'
    },
    'cigar case': {
        'open': 'no',
        'locked': 'yes',
        'item': 'cigar'
    },

}

# list of npcs to handle if they have their proper quest items
npcs = {
    'dad': {
        'items_required': ['beer', 'cigar'],
        'items_delivered': []
    },
    # 'bernard': {
    #     'items_required': ['dog food'],
    #     'items_delivered': []
    # },
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
            'around': 'Family photos are hung up all through the hallway. '
                      'My favorite is the one of me and Dad when we both were super fat.',
            'bedroom': 'My room is just through that door.',
            'study': 'Dad\'s study is just through this door.',
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
            'desk': 'On Dad\'s desk you see the story he is currently reading: "The Beast in the Cave." '
                    'You also see some sort of BOX',
            'box': {
                'locked': 'You read the lid of the box. "Fine Blend Cigars." '
                          'This must be Dad\'s CIGAR CASE. It appears to be locked.',
                'unlocked': 'You read the lid of the box. "Fine Blend Cigars." This must be Dad\'s CIGAR CASE.',
            },
            'mini-fridge': 'Dad hides his Blanton\'s in here. He doesn\'t know that I '
                           'take a sip every once in a while.',
            'shelf': 'Dad has some pretty good books here. '
                     'He\'s mostly got classic horror and things I\'ve never read. '
                     'They have cool covers, though.',
            'shelves': 'Dad has some pretty good books here. '
                       'He\'s mostly got classic horror and things I\'ve never read. '
                       'They have cool covers, though.',
            'cigar case': {
                'locked': 'The lid says "Fine Blend Cigars." '
                          'They look pretty fancy. The case appears to be locked.',
                'unlocked': 'The lid says "Fine Blend Cigars." They look pretty fancy.'
            }
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
        'container': ('fridge', 'cabinet'),
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
            'around': 'Mom\'s garden make the front yard look very colorful.',
            'mom': 'Mom loves planting her hydrangeas.',
            'garden': 'There\'s a wide variety of flowers and bushes in a patch of straw',
            'flowers': 'I think Mom might be in a relationship with a bee because '
                       'she\'s always out here when they\'re pollinating.',
        }
    },
    ####################################################
    'backyard': {
        'description': 'Out back, this is where you and BERNARD like to play. '
                       'You look about and see BERNARD in the DOGHOUSE, as well as the SHED.',
        ('back', 'behind', 'kitchen'): 'kitchen',
        'shed': 'shed',
        'npc': 'bernard',
        'object': {
            'around': 'The treehouse dad built when I was little is still up in the oak.',
            'doghouse': 'Bernard loves hanging out in his mighty palace.',
            'shed': 'Outside of his study, this is Dad\'s favorite place to be.',
        }
    },
    ####################################################
    'shed': {
        'description': '',
        ('back', 'behind', 'backyard'): 'backyard',
        'container': 'tuff box',
        'object': {
            'around': 'Woodworking tools are meticulously laid about the shed.',
            'tuff box': 'This is where Dad likes to put his random junk after he\'s '
                        'done working on his projects.',
            'toolbox': 'You don\'t see anything of use to you. '
                       'Just screwdrivers and the like.',
            'cooler': 'This is Dad\'s portable beer fridge. He doesn\'t work without this '
                      'thing being stocked.',
        }
    }
}

dialogue = {
    'dad': {
        'greeting': 'Hey son, can you fetch me that BEER in the FRIDGE? '
                    'It\'s next to the leftovers. I\'m absolutely parched.',
        'one_more_item': 'You know... a CIGAR would go absolutely great with this beer.',
        'no_more_items': 'Thanks son, I always liked you the best.',
        'before_study': {
            'How are you?': 'I\'m great. Just watching Tuck and drinking my Millers. What else could I ask for?',
            'What are you doing?': 'Just kicking back. I still have the whole day ahead of me.',
            'Do you need anything?': 'Yeah, actually. I would love that BEER I just mentioned if you wouldn\'t mind.'
        },
        "after_study":
            {
                'How are you?':
                    'I\'m great. Just watching Tuck and drinking my Millers. What else could I ask for?',
                'What are you doing?':
                    'Just kicking back. I still have the whole day ahead of me.',
                'Do you need anything?':
                    'Yeah, actually. I would love that BEER I just mentioned if you wouldn\'t mind.',
                "Do you happen to know where the key is to your cigar box?":
                    "No, I last remember giving it to your mother. Maybe check with her."
            }

    },
    ####################################################
    'mom': {
        'greeting': 'Hey sweetie, what\'s up?',
        'before_talk_dad': {
            'What are you doing?':
                'I\'m just planting my hydrangea\'s, dear. '
                'It\'s probably my favorite thing to do these days.',
            'Do you need anything?': 'No, I\'m going to head inside soon '
                                     'to get some water. Thank you though, dear :)',
        },
        'after_talk_dad': {
            'What are you doing?':
                'I\'m just planting my hydrangea\'s, dear. '
                'It\'s probably my favorite thing to do these days.',
            'Do you need anything?':
                'No, I\'m going to head inside soon '
                'to get some water. Thank you though, dear :)',
            'Do you know what Dad did with the cigar case key?':
                'I think he hid it somewhere in the shed. You know he likes to be extra.'
        }
    },
    ####################################################
    'bernard': {
        'greeting': 'Greetings, compatriot. How may I be of service to you?',
        'no_more_items': 'Thank you, human.',
        'before_talk_dad': {
            'What are you doing?': '',
            'Do you need anything?': '',
        },
        'after_talk_dad': {
            'What are you doing?': '',
            'Do you need anything?': '',
            'Do you know what Dad did with the cigar case key?': ''
        }
    },
}

#################################################################################################

# tracks current room
current_room = game_state['current_room']

# list of vowels
vowels = ['a', 'e', 'i', 'o', 'u']

# FIXME: uncomment after testing
# prompt()
previous_room = current_room
print(rooms[current_room]["description"])


#################################################################################################

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Display title screen
def prompt():
    print("---------------- Welcome to Beer Delivery Service \U0001F642 Nice to have you ----------------\n\n"
          "Pay attention to the words in all CAPS.\n\n"
          "If you end up getting stuck, you can type 'help' to learn various "
          "commands that may be useful.\n\n"
          "Have fun and good luck (it ain't hard... yet)!")
    time.sleep(8)
    clear()


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
    # checks if there is a container in the room
    elif 'container' in rooms[current_room]:
        # if so, will check
        containers_in_room = rooms[current_room]['container']
        if noun.lower() in containers_in_room:
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


def handle_go(noun, currentRoom, rooms, game_state):
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
                if current_room == 'study':
                    game_state['has_visited_study'] = True
                return
        # if there is no tuple, it sets the current room like before
        if noun in rooms[currentRoom].keys():
            current_room = rooms[currentRoom][noun]
            game_state["current_room"] = current_room
        else:
            print('I can\'t go that way.')


def handle_talk(noun, current_room, rooms, dialogue, game_state):
    if noun == "":
        print("You need to be more specific.")
    elif 'npc' in rooms[current_room].keys() and rooms[current_room]["npc"] == noun.lower():
        npc_name = rooms[current_room]["npc"]
        npc = dialogue.get(npc_name)

        if npc:
            if npc_name == "mom":
                # check game state to determine which set of dialogue options to use
                if game_state.get("talk_dad_after_study", True):
                    # if player talked to Dad, use Mom's "after_dad" dialogue
                    dialogue_options = npc.get("after_talk_dad", {})
                else:
                    dialogue_options = npc.get("before_talk_dad", {})
            elif npc_name == "dad":
                if game_state.get("has_visited_study", True):
                    dialogue_options = npc.get("after_study", {})
                    game_state["talk_dad_after_study"] = True
                else:
                    dialogue_options = npc.get("before_study", {})
            elif npc_name == "bernard":
                if game_state.get("talk_dad_after_study", True):
                    dialogue_options = npc.get("after_talk_dad", {})
                else:
                    dialogue_options = npc.get("before_talk_dad", {})

            print(f'\n{npc["greeting"]}')

            while True:
                index = 0
                for index, (question, response) in enumerate(dialogue_options.items(), start=1):
                    print(f'[{index}] {question}')
                exit_index = index + 1
                print(f'[{exit_index}] Exit\n')
                try:
                    choice_index = int(input('> '))
                    if choice_index == exit_index:
                        clear()
                        print(rooms[current_room]["description"])
                        break
                    if 1 <= choice_index <= len(dialogue_options):
                        question_key = list(dialogue_options.keys())[choice_index - 1]
                        print(f'{dialogue_options[question_key]}\n')
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
        if game_state["items_delivered"]:
            print('You rest your weary, beer-delivering eyes. '
                  'You wake up the next day, ready for whatever may lie ahead.\n\n'
                  'GAME OVER')
            time.sleep(10)
            exit()
        else:
            print('It isn\'t sleepy time yet, I have things I need to do!')
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
    try:
        successful_give = False
        inventory = game_state["inventory"]
        npc_name = rooms[current_room]["npc"]
        item_reqs = game_state['items_required']
        reqs_delivered = game_state['items_delivered']
        dialogue.get(npc_name)

        # If noun is empty, prompt the user for an item
        if noun == "":
            if not inventory:
                print("You don't have any items to give.")
            else:
                while not successful_give:
                    print("What do you want to give?")
                    handle_inventory(game_state)
                    item = input("> ").lower()

                    if item == 'back':
                        break
                    elif item in inventory:
                        while True:
                            try:
                                print(f"Who do you want to give the {item} to?")
                                next_noun = input('> ').lower()
                                npc_item_reqs = npcs[next_noun]['items_required']

                                if 'npc' in rooms[current_room].keys() and rooms[current_room]["npc"] == next_noun:
                                    npc_name = rooms[current_room]["npc"]
                                    npc = npcs.get(npc_name)

                                    # Check if the item is required by the NPC
                                    if npc and item in item_reqs:
                                        # update the delivered items when the item is delivered
                                        inventory.remove(item)
                                        npc_item_reqs.remove(item)
                                        reqs_delivered.append(item)

                                        # updates the flag so the loop can break
                                        successful_give = True
                                        # quest success dialogue
                                        if len(npc_item_reqs) == 0:
                                            print(dialogue[npc_name]['no_more_items'])
                                        else:
                                            print(dialogue[npc_name]['one_more_item'])
                                    # checks to see if the list of required items matches the list of items delivered
                                    # if it does, it prints a message prompting the user to go to bed (i.e. endgame)
                                    if item_reqs == reqs_delivered:
                                        game_state['items_delivered'] = True
                                        time.sleep(3)
                                        clear()
                                        # prompt to go to end game
                                        print('Boy I sure am beat from all that gathering. Time to go to bed.')
                                        break
                                    else:
                                        break
                            except KeyError:
                                print(f"{next_noun.capitalize()} isn't here to give {item} to.")
                                time.sleep(2)
                                clear()
                    else:
                        print(f"You don't have {item}.")
                        time.sleep(1)
                        clear()
    except KeyError:
        print("There isn't anyone here to give anything to.")


def handle_look_around(current_room, rooms):
    print(rooms[current_room]["description"])


def handle_look_obj(noun, current_room, rooms, game_state):
    try:
        # Use the game_state dictionary to check if the items have been delivered
        if noun in rooms[current_room]["object"]:
            if noun == 'bed':
                # Check if all items have been delivered using the game_state dictionary
                if not game_state["items_delivered"]:
                    print('The bed looks mad comfy but it isn\'t time for sleep yet! '
                          'I still need to get dad his beer.')
                else:
                    print(rooms[current_room]["object"][noun])
            elif noun in ['cigar case', 'box']:
                if game_state.get('cigar_case_unlocked', False):
                    print(rooms[current_room]["object"][noun]['unlocked'])
                else:
                    print(rooms[current_room]["object"][noun]['locked'])
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
    # ***** CHANGE FILE PATH TO WHEREVER YOU SAVE THE GAME *****
    folder_path = "C:\\Users\\bth0060\\PycharmProjects\\simple_game\\map_files"
    image_path = os.path.join(folder_path, f'{current_room}.png')
    try:
        Image.open(image_path).show()
        print('Pulling out the map.')
    except FileNotFoundError:
        print(f"Map image for {current_room} not found.")


# gameplay loop
while True:

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
        handle_talk(noun, current_room, rooms, dialogue, game_state)
    elif verb.lower() == 'take':
        handle_take(noun, current_room, rooms, game_state)
    elif verb.lower() == 'give':
        handle_give(noun, current_room, rooms, game_state, npcs, dialogue)
    elif verb.lower() == 'go':
        handle_go(noun, current_room, rooms, game_state)
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

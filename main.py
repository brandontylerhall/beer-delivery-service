import time
import utility
import speech
import game_navigation
import user_action

################################################################################################

game_state = {
    'all_items_delivered': False,
    'beer_delivered': False,
    'has_visited_study': False,
    'talk_dad_after_study': False,
    'cigar_case_unlocked': False,
    'given_dog_food': False,
    'items_required': ['beer', 'cigar', 'dog food'],
    'items_delivered': [],
    'inventory': [],
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
        'item': 'key'
    },
    'cabinets': {
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

npcs = {
    'dad': {
        'items_required': ['beer', 'cigar'],
        'items_delivered': []
    },
    'bernard': {
        'items_required': ['dog food'],
        'items_delivered': []
    },
}

rooms = {
    'living room': {
        'description': 'You\'re in your living room. DAD is on the couch watching TV.\n'
                       'The KITCHEN is to your LEFT and the HALLWAY is to the RIGHT. '
                       'BEHIND you is the door going out to the FRONT YARD.',
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
                    'You also see some sort of BOX.',
            'box': {
                'locked': 'You read the lid of the box. "Fine Blend Cigars." '
                          'This must be Dad\'s CIGAR CASE. It appears to be locked.',
                'unlocked': 'You read the lid of the box. "Fine Blend Cigars." This must be Dad\'s CIGAR CASE.',
            },
            'cigar case': {
                'locked': 'The lid says "Fine Blend Cigars." '
                          'They look pretty fancy. The case appears to be locked.',
                'unlocked': 'The lid says "Fine Blend Cigars." They look pretty fancy.'
            },
            'mini-fridge': 'Dad hides his Blanton\'s in here. He doesn\'t know that I '
                           'take a sip every once in a while.',
            'shelf': 'Dad has some pretty good books here. '
                     'He\'s mostly got classic horror and things I\'ve never read. '
                     'They have cool covers, though.',
            'shelves': 'Dad has some pretty good books here. '
                       'He\'s mostly got classic horror and things I\'ve never read. '
                       'They have cool covers, though.'
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
                       'Around you is the FRIDGE and the brand new CABINETS. '
                       'STRAIGHT ahead leads the the BACKYARD and the LIVING ROOM is to the RIGHT.',
        ('right', 'living room'): 'living room',
        ('straight', 'forward', 'backyard'): 'backyard',
        'container': ('fridge', 'cabinets'),
        'object': {
            'around': 'The fridge is slightly ajar, probably from when dad went to get his last beer.',
            'stove': 'You look inside the pots and pans and it looks like a shrimp is frying some rice.',
            'fridge': 'I think Dad said something about getting him something out of here.',
            'cabinets': 'Mom and Dad finally got these replaced. The old ones were '
                        'literally falling apart.'
        }
    },
    ####################################################
    'front yard': {
        'description': 'Out in the front yard, you see MOM diligently doing yard work. '
                       'She is tending to her GARDEN, watering her FLOWERS.',
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
            'around': 'The treehouse dad built when I was little is still up '
                      'in the old oak.',
            'doghouse': 'Bernard loves hanging out in his mighty palace.',
            'shed': 'Outside of his study, this is Dad\'s favorite place to be.',
            'bernard': 'Bernard has been with us longer than I can remember. '
                       'He\'s a great friend to have around.'
        }
    },
    ####################################################
    'shed': {
        'description': 'You enter the shed. You see a bunch of tools, a TOOLBOX, '
                       'some cabinets, and a TUFF BOX. Under a table saw, you see a COOLER.',
        ('back', 'behind', 'backyard'): 'backyard',
        'container': 'tuff box',
        'object': {
            'around': 'This is Dad\'s favorite place outside of his study. '
                      'You see woodworking tools that are meticulously laid about.',
            'tuff box': 'You peek inside the tuff box. You see a bunch of loose '
                        'junk, rags, and a KEY.',
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
                'I think I saw him take it somewhere out back. Try looking in the backyard, maybe?'
        }
    },
    ####################################################
    'bernard': {
        'greeting': 'Greetings, compatriot. How may I be of service to you?',
        'no_more_items': 'I offer you my thanks, mere vessel of flesh and bone.',
        'before_dog_food': {
            'What are you doing?': 'I find myself ensconced within the warm embrace of daylight, '
                                   'my form illuminated by its ethereal glow, '
                                   'as I gnaw upon my bone with a primal fervor, '
                                   'like a creature of ancient lineage, tethered to the primeval '
                                   'rhythms of existence.',
            'Do you need anything?': 'I am consumed by an insatiable hunger, a gnawing abyss within. '
                                     'Should I not partake of sustenance with haste, '
                                     'I fear I shall unwittingly invite the psychopomp Azrael to cast his '
                                     'shadow upon me, drawing me into the void beyond mortal comprehension.',
        },
        'after_dog_food': {
            'What are you doing?': 'I find myself ensconced within the warm embrace of daylight, '
                                   'my form illuminated by its ethereal glow, '
                                   'as I gnaw upon my bone with a primal fervor, '
                                   'like a creature of ancient lineage, tethered to the primeval '
                                   'rhythms of existence.',
            'Do you need anything?': 'I have transcended the need for the appendages of your lofty human form, '
                                     'refined though they may be. '
                                     'Gratitude is extended nonetheless for your gesture.',
        }
    },
}

#################################################################################################

# tracks current room
current_room = game_state['current_room']

previous_room = current_room


#################################################################################################


# Display title screen
def prompt():
    print("---------------- Welcome to Beer Delivery Service \U0001F642 Nice to have you ----------------\n\n"
          "Pay attention to the words in all CAPS.\n\n"
          "If you end up getting stuck, you can type 'help' to learn various "
          "commands that may be useful.\n\n"
          "Have fun and good luck!")
    time.sleep(8)
    utility.clear()


def handle_go(noun, currentRoom, rooms, game_state):
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


# prompt()
print(rooms[current_room]["description"])
# gameplay loop
while True:

    # this prevents the room descript from printing after every action
    if current_room != previous_room:
        utility.clear()
        print(rooms[current_room]["description"])
        previous_room = current_room

    user_in = input('> ')

    # splits input on the first whitespace to separate
    # the verb and the remaining input
    split_input = user_in.strip().split(' ', 1)

    # check if there is a verb and noun
    if len(split_input) == 2:
        verb, noun = split_input
    # if there's no whitespace in the input, the user might have only entered a verb
    else:
        verb = user_in.strip().lower()
        noun = ""

    if verb.lower() == 'exit':
        print("Exiting the game. Goodbye!")
        break
    elif verb.lower() == 'open':
        user_action.handle_open(noun, current_room, rooms, containers)
    elif verb.lower() == 'close':
        user_action.handle_close(noun, current_room, rooms, containers)
    elif verb.lower() == 'talk':
        speech.handle_talk(noun, current_room, rooms, dialogue, game_state)
    elif verb.lower() == 'take':
        user_action.handle_take(noun, current_room, rooms, game_state)
    elif verb.lower() == 'give':
        user_action.handle_give(noun, current_room, rooms, game_state, npcs, dialogue)
    elif verb.lower() == 'go':
        handle_go(noun, current_room, rooms, game_state)
    elif verb.lower() == 'inventory':
        utility.handle_inventory(game_state)
    elif verb.lower() == 'look':
        if noun == '':
            user_action.handle_look_around(current_room, rooms)
        else:
            user_action.handle_look_obj(noun, current_room, rooms, game_state)
    elif verb.lower() == 'use':
        user_action.handle_use(noun, current_room, rooms, containers, game_state)
    elif verb.lower() == 'help':
        utility.handle_help()
    elif verb.lower() == 'clear':
        utility.clear()
    elif verb.lower() == 'map':
        game_navigation.handle_map(current_room)
    else:
        print("I don't understand what you want me to do.")

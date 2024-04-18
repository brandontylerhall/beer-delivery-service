# Display title screen
import os


def prompt():
    print("----------------Welcome to Simple Game \U0001F642 Nice to have you----------------")
    print()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


containers = {
    'fridge': {'open': 'no', 'locked': 'no', 'item': 'ice cold beer'}
}

# Map
rooms = {
    'living room': {'left': 'kitchen', 'right': 'bedroom', 'npc': 'dad'},
    'kitchen': {'right': 'living room', 'container': 'fridge'},
    'bedroom': {'left': 'living room'}
}

# List to track inventory
inventory = []

# Tracks current room
current_room = 'living room'

# List of vowels
vowels = ['a', 'e', 'i', 'o', 'u']

prompt()

# user input, split into 2 parts
user_in = input('> ')
user_move = user_in.split(' ')

# 1st half of the input
verb = user_move[0].lower()

# 2nd half of the input
noun = user_move[1].lower()

# TODO need to add a try/except for if there is no container in the room
if verb == 'open':
    # if the room has a container in it and that container matches the input
    if 'container' in rooms[current_room].keys() and rooms[current_room]['container'] == noun:
        container_open = containers[noun]['open']
        container_locked = containers[noun]['locked']
        # if the container is both unlocked and unopened, it will do the following
        if container_locked == 'no' and container_open == 'no':
            # container is now set to open
            containers[noun]['open'] = 'yes'
            rooms[current_room]['item'] = containers[noun]['item']
            # goes through rooms{} and checks to see if there are any items
            if 'item' in rooms[current_room].keys():
                nearby_item = rooms[current_room]['item']
                # if the last character of the item is an 's' (as in a plural item)
                if nearby_item[-1] == 's':
                    print(f'You open the {noun} and find {nearby_item}')
                # else if the first letter of the item is a vowel
                elif nearby_item[0] in vowels:
                    print(f'You open the {noun} and see an {nearby_item}')
                # else if the item is singular and starts with a consonant
                else:
                    print(f'You open the {noun} and see a {nearby_item}')
        elif container_locked == 'yes':
            print(f'The {noun} is locked. Maybe I should find a key...')
        elif container_open == 'yes':
            print(f'The {noun} is already open, dumb dumb')


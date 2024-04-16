# Display title screen
import os


def prompt():
    print("----------------Welcome to Simple Game \U0001F642 Nice to have you----------------")
    print()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


containers = {
    'fridge': {'locked': 'no', 'item': 'ice cold beer'}
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
current_room = 'kitchen'

# List of vowels
vowels = ['a', 'e', 'i', 'o', 'u']

prompt()
print(containers)
print(rooms)
user_in = input('> ')
user_move = user_in.split(' ')

verb = user_move[0].lower()

noun = user_move[1].lower()

if verb == 'open':
    if 'container' in rooms[current_room].keys() and rooms[current_room]['container'] == noun:
        container_locked = containers[noun]['locked']
        if container_locked == 'no':
            print(f'You open the {noun}')
            rooms[current_room]['item'] = 'ice cold beer'
            # Goes through rooms{} and checks to see if there are any items
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
            print(f'The {noun} is locked')

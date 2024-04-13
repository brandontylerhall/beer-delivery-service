# Display title screen
def prompt():
    print("----------------Welcome to Simple Game \U0001F642 Nice to have you----------------")
    print()
    print()


# Map
rooms = {
    'living_room': {'left': 'kitchen', 'right': 'bedroom', 'npc': 'dad'},
    'kitchen': {'right': 'living_room', 'item': 'ice_cold_beer'},
    'bedroom': {'left': 'living_room'}
}

# List to track inventory
inventory = []

# Tracks current room
current_room = 'living_room'

# Result of last move
msg = ''


def play_game():
    user_input = "> "
    print("You're in the LIVING ROOM. Your DAD is on the COUCH watching Fox News.\n"
          "The KITCHEN is to your LEFT and your ROOM is to the RIGHT.\n")

    input(user_input)


prompt()

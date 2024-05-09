import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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

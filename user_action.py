import time

import utility


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
    elif noun == "key":
        if noun in inventory:
            print("What do you want to use the key on?")
            use_key_on = input("> ").lower()
            if use_key_on == 'cigar case':
                if use_key_on in rooms[current_room]["object"]:
                    inventory.remove(noun)
                    containers[use_key_on]["locked"] = "no"
                    game_state['cigar_case_unlocked'] = True
                    print(f"You unlocked the {use_key_on}.")
                else:
                    print(f"There is no {use_key_on} to use that on.")
            else:
                print(f"That key doesn't open {use_key_on}")
        else:
            print("You don't have a key.")
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

        # if noun is empty, prompt the user for an item
        if noun == "":
            if not inventory:
                print("You don't have any items to give.")
            else:
                while not successful_give:
                    print("What do you want to give?")
                    utility.handle_inventory(game_state)
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

                                    # check if the item is required by the NPC
                                    if npc and item in item_reqs:

                                        # update the delivered items when the item is delivered
                                        inventory.remove(item)
                                        npc_item_reqs.remove(item)
                                        reqs_delivered.append(item)

                                        # updates the flag so the loop can break
                                        successful_give = True
                                        if item == 'dog food':
                                            game_state['given_dog_food'] = True
                                        if item == 'beer':
                                            game_state['beer_delivered'] = True
                                        # quest success dialogue
                                        if len(npc_item_reqs) == 0:
                                            print(dialogue[npc_name]['no_more_items'])
                                        else:
                                            print(dialogue[npc_name]['one_more_item'])
                                    # checks to see if the list of required items matches the list of items delivered
                                    # if it does, it prints a message prompting the user to go to bed (i.e. endgame)
                                    if len(item_reqs) == len(reqs_delivered):
                                        game_state['items_delivered'] = True
                                        time.sleep(3)
                                        utility.clear()
                                        # prompt to go to end game
                                        print('Boy I sure am beat from all that gathering. Time to go to bed.')
                                        break
                                    else:
                                        break
                            except KeyError:
                                print(f"{next_noun.capitalize()} isn't here to give {item} to.")
                                time.sleep(2)
                                utility.clear()
                    else:
                        print(f"You don't have {item}.")
                        time.sleep(1)
                        utility.clear()
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


def handle_open(noun, current_room, rooms, containers):
    if noun == "":
        print("You need to be more specific.")
    # checks if there is a container in the room
    elif 'container' in rooms[current_room]:
        containers_in_room = rooms[current_room]['container']
        # if so, will check if what the user input is in fact the container in the current room
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
                    print(f'You open the {noun} and see: {nearby_item.upper()}.')
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

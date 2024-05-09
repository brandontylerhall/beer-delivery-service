from utility import clear


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
                if game_state.get("beer_delivered", False):
                    dialogue['dad']['before_study']['Do you need anything?'] = \
                        'Yeah, actually. I would love that CIGAR I just mentioned if you wouldn\'t mind.'
                    dialogue['dad']['after_study']['Do you need anything?'] = \
                        'Yeah, actually. I would love that CIGAR I just mentioned if you wouldn\'t mind.'

                if game_state.get("has_visited_study", True):
                    dialogue_options = npc.get("after_study", {})
                    game_state["talk_dad_after_study"] = True
                else:
                    dialogue_options = npc.get("before_study", {})
            elif npc_name == "bernard":
                # Check if talk_dad_after_study is True
                if game_state.get("talk_dad_after_study", False):
                    extra_option = "Do you know what Dad did with the cigar case key?"
                    extra_response = ("The certainty eludes me, shrouded in the mists of uncertainty, "
                                      "yet my gaze did perceive his descent into the stygian confines "
                                      "of the shed, bearing with him that which incites dread. "
                                      "Beyond that threshold, I dare not venture, "
                                      "lest I invoke the horrors lurking within.")
                    # if true, update both before and after dog food dialogue options
                    if extra_option not in npc.get("before_dog_food", {}):
                        npc["before_dog_food"][extra_option] = extra_response
                    if extra_option not in npc.get("after_dog_food", {}):
                        npc["after_dog_food"][extra_option] = extra_response

                if game_state.get("given_dog_food", True):
                    dialogue_options = npc.get("after_dog_food", {})
                else:
                    dialogue_options = npc.get("before_dog_food", {})

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

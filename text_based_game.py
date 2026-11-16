"""Project Two: Parasite Protocol, a sci-fi mystery text-based game."""

# Name: Freddy Salas Miranda

# Constants used throughout the game.
START_ROOM = 'Crew Quarters'
VILLAIN_ROOM = 'Reactor Room'
VILLAIN_NAME = 'Nadia'
REVEAL_ITEM = 'Bloodstained Scarf'
TOTAL_ITEMS = 6
VALID_DIRECTIONS = ('north', 'south', 'east', 'west')

# Who each piece of evidence belongs to, used for the message on pickup.
ITEM_OWNERS = {
    'Stuffed Rabbit': 'Jess',
    'Old Film Camera': 'Devon',
    'Harmonica': 'you',
    'MP3 Player': 'Marcus',
    'Potted Plant': 'Priya',
    'Bloodstained Scarf': 'Nadia',
}


def get_villain_name(inventory):
    """Return the villain's name, which changes once the scarf is found."""
    if REVEAL_ITEM in inventory:
        return f'{VILLAIN_NAME} (Infected)'
    return VILLAIN_NAME


def with_article(item_name):
    """Return the item name with 'a' or 'an' in front of it."""
    if item_name[0].lower() in 'aeiou':
        return f'an {item_name}'
    return f'a {item_name}'


def show_instructions():
    """Display the game objective and the commands the player can use."""
    print('Parasite Protocol: A Space Mystery')
    print('One of your crewmates is carrying a mind-controlling parasite.')
    print(f'Collect all {TOTAL_ITEMS} pieces of evidence, then confront')
    print(f'the infected crewmate in the {VILLAIN_ROOM}.')
    print('Go in too early and it is GAME OVER.')
    print('Move commands: go north, go south, go east, go west')
    print("Add to Inventory: get 'item name'")


def show_status(current_room, inventory, rooms):
    """Display the current room, the inventory, and the item in the room."""
    print()
    print(f'You are in the {current_room}')
    print(f'Inventory: {inventory}')

    # Only show an item if the room still has one.
    if 'item' in rooms[current_room]:
        print(f"You see {with_article(rooms[current_room]['item'])}")

    print('----------------------')


def main():
    """Run the main gameplay loop until the player wins or loses."""

    # A dictionary linking each room to its neighbors and to its item.
    # The start room and the villain room have no item.
    rooms = {
        'Crew Quarters': {'north': 'Bridge', 'south': 'Engine Room',
                          'east': 'Mess Hall', 'west': 'Observation Deck'},
        'Bridge': {'south': 'Crew Quarters', 'item': 'Stuffed Rabbit'},
        'Observation Deck': {'east': 'Crew Quarters',
                             'item': 'Old Film Camera'},
        'Mess Hall': {'west': 'Crew Quarters', 'south': 'Med Bay',
                      'item': 'Harmonica'},
        'Med Bay': {'north': 'Mess Hall', 'west': 'Engine Room',
                    'item': 'MP3 Player'},
        'Engine Room': {'north': 'Crew Quarters', 'east': 'Med Bay',
                        'south': 'Cargo Bay', 'item': 'Potted Plant'},
        'Cargo Bay': {'north': 'Engine Room', 'south': 'Reactor Room',
                      'item': 'Bloodstained Scarf'},
        'Reactor Room': {'north': 'Cargo Bay'},  # villain room
    }

    current_room = START_ROOM
    inventory = []
    game_over = False

    show_instructions()

    # Gameplay loop: keeps going until the player wins or loses.
    while not game_over:
        show_status(current_room, inventory, rooms)

        # Lowercase and trim the input so any capitalization is accepted.
        player_command = input('Enter your move:\n').strip().lower()
        command_parts = player_command.split()

        if len(command_parts) == 0:
            print('Invalid Input!')

        # ----- Movement commands -----
        elif command_parts[0] == 'go':
            # Must be exactly "go <direction>" with a real direction.
            if (len(command_parts) != 2
                    or command_parts[1] not in VALID_DIRECTIONS):
                print('Invalid Input!')
            elif command_parts[1] not in rooms[current_room]:
                print("You can't go that way!")
            else:
                current_room = rooms[current_room][command_parts[1]]

                # Entering the villain room ends the game, win or lose.
                if current_room == VILLAIN_ROOM:
                    villain = get_villain_name(inventory)
                    print()
                    print(f'You are in the {current_room}')
                    print(f'You see {villain}')

                    if len(inventory) == TOTAL_ITEMS:
                        print(f'You confront {villain} with all the '
                              'evidence and seal her in the reactor '
                              'shielding. The crew is safe.')
                        print('Congratulations! You have collected all '
                              'items and exposed the parasite!')
                    else:
                        print(f'{villain} lunges at you before you can '
                              'prove anything...GAME OVER!')

                    print('Thanks for playing the game. Hope you enjoyed it.')
                    game_over = True

        # ----- Get-item commands -----
        elif command_parts[0] == 'get':
            item_name = ' '.join(command_parts[1:])
            room_item = rooms[current_room].get('item')

            if item_name == '':
                print('Invalid Input!')
            elif room_item is None or item_name != room_item.lower():
                print(f"Can't get {item_name}!")
            else:
                # Valid pickup: move the item from the room to inventory.
                inventory.append(room_item)
                del rooms[current_room]['item']
                print(f'{room_item} retrieved!')

                # Story message based on whose item it was.
                owner = ITEM_OWNERS[room_item]
                if room_item == REVEAL_ITEM:
                    print(f"It's {VILLAIN_NAME}'s scarf, and it's "
                          'soaked in blood.')
                    print(f'{VILLAIN_NAME} is the infected one! She is '
                          f'now {get_villain_name(inventory)}.')
                elif owner == 'you':
                    print('Your own harmonica. At least you can trust '
                          'yourself.')
                else:
                    print(f'This belongs to {owner}. {owner} is cleared.')

                # Tell the player how close they are to the confrontation.
                if len(inventory) == TOTAL_ITEMS:
                    print("You've found all the evidence! Go confront "
                          f'{get_villain_name(inventory)} in the '
                          f'{VILLAIN_ROOM}.')
                else:
                    remaining = TOTAL_ITEMS - len(inventory)
                    print(f'You still need {remaining} more piece(s) of '
                          'evidence before you can confront the villain.')

        # ----- Anything else -----
        else:
            print('Invalid Input!')


if __name__ == '__main__':
    main()

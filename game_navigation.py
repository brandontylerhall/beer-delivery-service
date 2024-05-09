from PIL import Image
import os

"""
Displays the map image for the current room.

The following function retrieves the map image for the current room and displays it. It first gets the current
directory using `os.path.dirname(os.path.abspath(__file__))`. Then, it constructs the path to the
`map_files` directory by joining the current directory with the `map_files` directory name. Next, it
constructs the path to the image file by joining the `map_files` directory with the name of the
current room followed by the file extension `.png`. It tries to open the image using the
`Image.open()` function from the `PIL` library and displays it using the `show()` method. If the map
image is found, it prints "Pulling out the map." If the map image is not found, it prints a message
indicating that the map image for the current room was not found.

Parameters:
None

Returns:
None
"""


def handle_map(current_room):
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the map_files directory
    map_files_directory = os.path.join(current_directory, 'map_files')

    # Construct the path to the image file
    image_path = os.path.join(map_files_directory, f'{current_room}.png')

    try:
        Image.open(image_path).show()
        print('Pulling out the map.')
    except FileNotFoundError:
        print(f"Map image for {current_room} not found.")

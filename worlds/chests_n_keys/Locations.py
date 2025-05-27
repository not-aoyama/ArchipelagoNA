from typing import Dict, NamedTuple

from BaseClasses import Location

# There will be 256 total possible locations: Chests 1 through 256.

class ChestsNKeysLocation(Location):
    game = "Chests 'n' Keys"

class ChestsNKeysLocationData(NamedTuple):
    address: int

location_data_table : Dict[str, ChestsNKeysLocationData] = {}

def initialize_location_data():
    # Add each chest to the location data table.
    for i in range(1, 257):
        location_data_table.update({f"Chest {i}": ChestsNKeysLocationData(420000 + i)})

initialize_location_data()
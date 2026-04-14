from typing import Dict, NamedTuple

from BaseClasses import Location

# There will be 300 total possible locations: Chests 1 through 300.
# Chests 2 through 300 may or may not be locked, but Chest 1 is always unlocked, 
# guaranteeing that the player starts with at least one item.

class ChestsNKeysLocation(Location):
    game = "Chests 'n' Keys"

class ChestsNKeysLocationData(NamedTuple):
    address: int

location_data_table : Dict[str, ChestsNKeysLocationData] = {}

def initialize_location_data():
    # Add each chest to the location data table.
    for i in range(1, 301):
        location_data_table.update({f"Chest {i}": ChestsNKeysLocationData(420000 + i)})

initialize_location_data()
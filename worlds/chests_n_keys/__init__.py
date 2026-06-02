from typing import Dict, List, Any

from BaseClasses import Region
from worlds.AutoWorld import WebWorld, World

from .Items import ChestsNKeysItem, item_data_table
from .Locations import ChestsNKeysLocation, location_data_table
from .Options import ChestsNKeysOptions
from .Rules import get_chest_rule

class ChestsNKeysWebWorld(WebWorld):
    theme = "partyTime"

    # TODO: finish class

class ChestsNKeysWorld(World):
    """The most original Archipelago game of all time."""

    game = "Chests 'n' Keys"
    web = ChestsNKeysWebWorld()
    options : ChestsNKeysOptions
    options_dataclass = ChestsNKeysOptions
    item_name_to_id = {item_name: item_data.code for item_name, item_data in item_data_table.items()}
    location_name_to_id = {
        location_name : location_data.address for location_name, location_data in location_data_table.items()
    }

    def create_item(self, name) -> ChestsNKeysItem:
        return ChestsNKeysItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self):
        item_pool : List[ChestsNKeysItem] = []

        # Force the number of locked chests to be no greater than the total number of chests minus 1.
        number_of_locked_chests : int = min(self.options.number_of_locked_chests.value, self.options.number_of_chests - 1)
        
        # Create as many keys as there are locked chests, and create as many filler items as there are unlocked chests.
        number_of_unlocked_chests : int = self.options.number_of_chests.value - number_of_locked_chests
        for _ in range (0, number_of_unlocked_chests):
            item_pool.append(self.create_item("Item That Does Nothing"))
        # The locked chests come after the unlocked chests, so they have higher numbers.
        for i in range (number_of_unlocked_chests + 1, self.options.number_of_chests.value + 1):
            item_pool.append(self.create_item(f"Key {i}"))
        
        self.multiworld.itempool += item_pool
    
    def create_regions(self):
        # There will only be one region. It will have the default origin region name, "Menu".
        self.multiworld.regions.append(Region("Menu", self.player, self.multiworld))

        # Create locations, i.e. the chests. There will be as many chests as specified in the options.
        region = self.get_region("Menu")
        for i in range(1, self.options.number_of_chests.value + 1):
            location_name = f"Chest {i}"
            region.add_locations({location_name: location_data_table[location_name].address}, ChestsNKeysLocation)

        # TODO: consider whether to make Chest 1 a priority location, since Chest 1 will always be unlocked.
        
    def get_filler_item_name(self) -> str:
        return "Item That Does Nothing"

    def set_rules(self):
        # Set access rules for each of the chests.
        # Also make it so that a chest cannot contain its own key.
        for i in range(1, self.options.number_of_chests.value + 1):
            self.get_location(f"Chest {i}").access_rule = get_chest_rule(self, i)
            self.get_location(f"Chest {i}").item_rule = lambda item : item.name != "Key {i}"
        
        # Set the completion condition.
        # Completion is only possible if the player has enough keys to open the required number of chests.
        # Force the number of locked chests to be no greater than the total number of chests minus 1.
        number_of_locked_chests : int = min(self.options.number_of_locked_chests.value, self.options.number_of_chests.value - 1)
        # If none of the chests are locked, the game is always winnable no matter what!
        if number_of_locked_chests == 0:
            self.multiworld.completion_condition[self.player] = lambda _ : True
        else:
            # If there are locked chests, we need to make a list of all keys corresponding to those locked chests.
            all_keys : List[str] = []
            # Number of unlocked chests
            number_of_unlocked_chests : int = self.options.number_of_chests.value - number_of_locked_chests
            # Number of the first locked chest (comes immediately after all the unlocked chests)
            first_locked_chest : int = number_of_unlocked_chests + 1
            # Number of the last locked chest (the last chest of them all)
            last_locked_chest : int = self.options.number_of_chests.value
            for i in range(first_locked_chest, last_locked_chest + 1):
                all_keys.append(f"Key {i}")
            # Force the number of required chests to be no greater than the total number of chests.
            number_of_required_chests : int = min(self.options.number_of_required_chests.value, self.options.number_of_chests.value)
            # The number of keys that is required is the number of required chests minus the number of unlocked chests,
            # since unlocked chests can be opened without keys.
            self.multiworld.completion_condition[self.player] = lambda state : state.has_from_list_unique(
                all_keys, self.player, number_of_required_chests - number_of_unlocked_chests)

    def fill_slot_data(self) -> Dict[str, Any]:
        # In order for our client to handle the generated seed correctly, 
        # it needs to know how many chests start out locked
        # and how many chests are required to goal.
        return self.options.as_dict("number_of_locked_chests", "number_of_required_chests")
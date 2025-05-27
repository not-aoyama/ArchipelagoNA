from typing import List

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
    web = ChestsNKeysWebWorld
    options : ChestsNKeysOptions
    options_dataclass = ChestsNKeysOptions
    item_name_to_id = {item_name: item_data.code for item_name, item_data in item_data_table}
    location_name_to_id = {
        location_name : location_data.address for location_name, location_data in location_data_table
    }

    def create_item(self, name) -> ChestsNKeysItem:
        return ChestsNKeysItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self):
        item_pool : List[ChestsNKeysItem] = []

        # If keys are enabled, create as many keys as there will be chests.
        # Otherwise, create as many filler items as there will be chests.
        if self.options.keys_enabled:
            for i in range(1, self.options.number_of_chests.value + 1):
                item_pool.append(self.create_item(f"Key {i}"))
        else:
            for i in range(self.options.number_of_chests.value):
                item_pool.append(self.create_item("Item That Does Nothing"))
        
        self.multiworld.itempool += item_pool
    
    def create_regions(self):
        # There will only be one region. It will have the default origin region name, "Menu".
        self.multiworld.regions.append(Region("Menu", self.player, self.multiworld))

        # Create locations, i.e. the chests. There will be as many chests as specified in the options.
        region = self.get_region("Menu")
        for i in range(1, self.options.number_of_chests.value + 1):
            location_name = f"Chest {i}"
            region.add_locations({location_name: location_data_table[location_name].address}, ChestsNKeysLocation)
        
    def get_filler_item_name(self) -> str:
        return "Item That Does Nothing"

    def set_rules(self):
        # Set access rules for each of the chests.
        # Also make it so that a chest cannot contain its own key.
        for i in range(1, self.options.number_of_chests.value + 1):
            self.get_location(f"Chest {i}").access_rule = get_chest_rule(self, i)
            self.get_location(f"Chest {i}").item_rule = lambda item : item.name != "Key {i}"
        
        # Set the completion condition.
        # If keys are enabled, completion is only possible if the player has every key.
        if self.options.keys_enabled:
            all_keys : List[str] = []
            for i in range(1, self.options.number_of_chests.value + 1):
                all_keys.append(f"Key {i}")
            self.multiworld.completion_condition[self.player] = lambda state : state.has_all(all_keys, self.player)
        # If keys are disabled, completion is always possible, so the completion condition is true.
        else:
            self.multiworld.completion_condition[self.player] = lambda state : True
from typing import Dict, NamedTuple

from BaseClasses import Item, ItemClassification

from .Options import MAX_NUMBER_CHESTS

# There can be up to 359 keys (each a different type of item) and one type of filler item.

class ChestsNKeysItem(Item):
    game = "Chests 'n' Keys"

class ChestsNKeysItemData(NamedTuple):
    code: int
    type: ItemClassification

item_data_table : Dict[str, ChestsNKeysItemData] = {}

def initialize_item_data():
    # Add in Keys 1 through 359
    for i in range(1, MAX_NUMBER_CHESTS):
        item_data_table.update({
            f"Key {i}":
            ChestsNKeysItemData(69000 + i, ItemClassification.progression)
        })
    
    # Add the filler item
    item_data_table.update({
        "Item That Does Nothing":
        ChestsNKeysItemData(69420, ItemClassification.filler)
    })

initialize_item_data()
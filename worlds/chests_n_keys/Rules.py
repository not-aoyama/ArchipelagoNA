from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import ChestsNKeysWorld

def get_chest_rule(world : "ChestsNKeysWorld", i : int) -> Callable[[CollectionState], bool]:
    # Force the number of locked chests to be no greater than the total number of chests minus 1.
    number_of_locked_chests : int = min(world.options.number_of_locked_chests.value, world.options.number_of_chests - 1)

    # If this chest starts out unlocked, it will always be accessible.
    # The chests that start out unlocked all come before the chests that start out locked, so they have the lowest numbers.
    number_of_unlocked_chests : int = world.options.number_of_chests.value - number_of_locked_chests
    if i <= number_of_unlocked_chests:
        return lambda _: True
    
    # If this chest starts out locked, it will only be accessible if the player has the corresponding key.
    return lambda state: state.has(f"Key {i}", world.player)
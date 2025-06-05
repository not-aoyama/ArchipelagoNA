from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import ChestsNKeysWorld

def get_chest_rule(world : "ChestsNKeysWorld", i : int) -> Callable[[CollectionState], bool]:
    # If keys are enabled, a chest will only be accessible if the player has the corresponding key.
    if world.options.keys_enabled:
        return lambda state: state.has(f"Key {i}", world.player)
    
    # If keys are disabled, all chests will always be accessible.
    return lambda _: True

def get_desk_rule():
    # The desk is always accessible.
    return lambda _: True
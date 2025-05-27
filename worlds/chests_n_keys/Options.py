from dataclasses import dataclass
from Options import Range, Toggle, PerGameCommonOptions

class KeysEnabled(Toggle):
    """
    The \"keys\" part of Chests 'n' Keys. 
    If you turn this on, the chests will be locked, and their respective keys will be needed to open them.
    """
    internal_name = "keys_enabled"
    display_name = "Keys Enabled"

class NumberOfChests(Range):
    """How many chests there are."""
    internal_name = "number_of_chests"
    display_name = "Number of Chests"
    range_start = 1
    range_end = 256
    default = 1

@dataclass
class ChestsNKeysOptions(PerGameCommonOptions):
    keys_enabled : KeysEnabled
    number_of_chests : NumberOfChests
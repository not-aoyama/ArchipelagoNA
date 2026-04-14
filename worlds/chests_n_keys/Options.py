from dataclasses import dataclass
from Options import Range, NamedRange, PerGameCommonOptions

class NumberOfChests(Range):
    """How many chests there are."""
    internal_name = "number_of_chests"
    display_name = "Number of Chests"
    range_start = 1
    range_end = 300
    default = 1

class NumberOfLockedChests(NamedRange):
    """
    How many of the chests are locked.
    If a chest is locked, it will require its respective key to open.
    This number must be at least 1 less than the total number of chests. If it isn't, this number will be changed automatically.
    """
    internal_name = "number_of_locked_chests"
    display_name = "Number of Locked Chests"
    range_start = 0
    range_end = 299
    default = 0

    special_range_names = {
        "none": 0,
        "maximum": 299
    }

class NumberOfRequiredChests(NamedRange):
    """
    How many chests must be opened in order to goal.
    This number must be no greater than the total number of chests. If it isn't, this number will be changed automatically.
    """
    internal_name = "number_of_required_chests"
    display_name = "Number of Required Chests"
    range_start = 0
    range_end = 299
    default = 299

    special_range_names = {
        "none": 0,
        "all": 299
    }

@dataclass
class ChestsNKeysOptions(PerGameCommonOptions):
    number_of_chests : NumberOfChests
    number_of_locked_chests : NumberOfLockedChests
    number_of_required_chests : NumberOfRequiredChests
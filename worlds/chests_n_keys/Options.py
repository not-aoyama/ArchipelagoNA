from dataclasses import dataclass
from Options import Range, NamedRange, PerGameCommonOptions

"""The maximum number of chests that can exist in a single Chests 'n' Keys slot."""
MAX_NUMBER_CHESTS = 360

class NumberOfChests(Range):
    """How many chests there are."""
    internal_name = "number_of_chests"
    display_name = "Number of Chests"
    range_start = 1
    range_end = MAX_NUMBER_CHESTS
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
    range_end = MAX_NUMBER_CHESTS - 1
    default = 0

    special_range_names = {
        "none": 0,
        "maximum": MAX_NUMBER_CHESTS - 1
    }

class NumberOfRequiredChests(NamedRange):
    """
    How many chests must be opened in order to goal.
    This number must be no greater than the total number of chests. If it isn't, this number will be changed automatically.
    """
    internal_name = "number_of_required_chests"
    display_name = "Number of Required Chests"
    range_start = 0
    range_end = MAX_NUMBER_CHESTS
    default = MAX_NUMBER_CHESTS

    special_range_names = {
        "none": 0,
        "all": MAX_NUMBER_CHESTS
    }

@dataclass
class ChestsNKeysOptions(PerGameCommonOptions):
    number_of_chests : NumberOfChests
    number_of_locked_chests : NumberOfLockedChests
    number_of_required_chests : NumberOfRequiredChests
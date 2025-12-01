"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Bryce Bellerand

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    os.path.exists(filename)
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")
    quests = {}
    try:
        with open(filename, 'r') as file:
            content = file.read()
            quest_blocks = content.strip().split('\n\n')
            for block in quest_blocks:
                lines = block.strip().split('\n')
                quest_dict = parse_quest_block(lines)
                validate_quest_data(quest_dict)
                quests[quest_dict['quest_id']] = quest_dict
    except IOError:
        raise CorruptedDataError(f"Quest data file '{filename}' is corrupted or unreadable.")
    except InvalidDataFormatError as e:
        raise e
    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file

    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description

    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """

    # Validate file exists
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file '{filename}' not found.")

    items = {}

    try:
        with open(filename, 'r') as file:
            content = file.read().strip()

            # Handle empty file
            if not content:
                raise CorruptedDataError(f"Item data file '{filename}' is empty or corrupted.")

            item_blocks = content.split('\n\n')

            for block in item_blocks:
                lines = block.strip().split('\n')

                if not lines:
                    continue  # Skip accidental empty block

                # Parse each block into an item dictionary
                item_dict = parse_item_block(lines)

                # Validate expected fields and types
                validate_item_data(item_dict)

                # Insert into dictionary using item_id as key
                items[item_dict['item_id']] = item_dict

    except IOError:
        raise CorruptedDataError(f"Item data file '{filename}' is corrupted or unreadable.")

    except InvalidDataFormatError:
        # Let validation/parsing errors propagate for clarity
        raise

    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_keys = ['quest_id', 'title', 'description', 
                     'reward_xp', 'reward_gold', 
                     'required_level', 'prerequisite']
    for key in required_keys:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing required quest field: {key}")
    if not isinstance(quest_dict['reward_xp'], int):
        raise InvalidDataFormatError("Reward XP must be an integer.")
    if not isinstance(quest_dict['reward_gold'], int):
        raise InvalidDataFormatError("Reward Gold must be an integer.")
    if not isinstance(quest_dict['required_level'], int):
        raise InvalidDataFormatError("Required Level must be an integer.")
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    # Check that all required keys exist
    required_keys = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    valid_types = ['weapon', 'armor', 'consumable']
    for key in required_keys:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing required item field: {key}")

    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    if not os.path.exists("data"):
        os.makedirs("data")
    default_quests = """QUEST_ID: Random Town
    TITLE: Save the Village
    DESCRIPTION: Your first quest to get started.
    REWARD_XP: 50
    REWARD_GOLD: 25
    REQUIRED_LEVEL: 1
    PREREQUISITE: NONE
    QUEST_ID: second_quest
    TITLE: The Next Step
    DESCRIPTION: Continue your adventure with this quest.
    REWARD_XP: 200
    REWARD_GOLD: 100
    REQUIRED_LEVEL: 2
    PREREQUISITE: None"""
    default_items = """ITEM_ID: health_potion
    NAME: Health Potion
    TYPE: consumable
    EFFECT: health:50
    COST: 25
    DESCRIPTION: Restores 50 health points.
    ITEM_ID: iron_sword
    NAME: Iron Sword
    TYPE: weapon
    EFFECT: strength:10
    COST: 100
    DESCRIPTION: A sturdy iron sword that increases strength."""
    quest_file = "data/quests.txt"
    item_file = "data/items.txt"
    if not os.path.exists(quest_file):
        with open(quest_file, 'w') as f:
            f.write(default_quests)
    if not os.path.exists(item_file):
        with open(item_file, 'w') as f:
            f.write(default_items)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest_block = {}
    for line in lines:
        if ': ' not in line:
            raise InvalidDataFormatError(f"Invalid quest line format: {line}")
        key, value = line.split(': ', 1)
        key = key.strip().lower()
        value = value.strip()
        if key in ['reward_xp', 'reward_gold', 'required_level']:
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for {key}, got '{value}'")
        quest_block[key] = value
    
    return quest_block

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_block = {}
    for line in lines:
        if ': ' not in line:
            raise InvalidDataFormatError(f"Invalid item line format: {line}")
        key, value = line.split(': ', 1)
        key = key.strip().lower()
        value = value.strip()
        if key in ['cost']:
            try:
                value = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Expected integer for {key}, got '{value}'")
        item_block[key] = value
    return item_block

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")


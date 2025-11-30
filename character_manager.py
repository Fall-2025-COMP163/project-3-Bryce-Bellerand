"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Bryce Bellerand

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

warrior_base_stats = {
    'health': 120,
    'strength': 15,
    'magic': 5
}
mage_base_stats = {
    'health': 80,
    'strength': 8,
    'magic': 20
}
rogue_base_stats = {
    'health': 90,
    'strength': 12,
    'magic': 10
}
cleric_base_stats = {
    'health': 100,
    'strength': 10,
    'magic': 15
}
def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    if character_class not in ["Warrior", "Mage", "Rogue", "Cleric"]:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    else:
        if character_class == "Warrior":
            character_stats = warrior_base_stats
        elif character_class == "Mage":
            character_stats = mage_base_stats
        elif character_class == "Rogue":
            character_stats = rogue_base_stats
        elif character_class == "Cleric":
            character_stats = cleric_base_stats

    # Create character dictionary
    character = {
        'name': name,
        'class': character_class,
        'level': 1,
        'health': character_stats['health'],
        'max_health': character_stats['health'],
        'strength': character_stats['strength'],
        'magic': character_stats['magic'],
        'experience': 0,
        'gold': 100,
        'inventory': [],
        'active_quests': [],
        'completed_quests': []
    }

    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    file_path = os.path.join(save_directory, f"{character['name']}_save.txt")
    # checks if there isn't a save file, and makes one if not
    try:
        with open(file_path, 'w') as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True
    #stores character data in a text file
    except (PermissionError, IOError) as e:
        raise e

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    file_path = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(file_path):
        raise CharacterNotFoundError(f"Character {character_name} not found.")
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except IOError:
        raise SaveFileCorruptedError(f"Save file for {character_name} is corrupted.")

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    if not os.path.exists(save_directory):
        return []
    character_names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            character_name = filename[:-9]  # Remove '_save.txt'
            character_names.append(character_name)
    return character_names  

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    path = os.path.join(save_directory, f"{character_name}_save.txt")
    #creates path to character save file
    if not os.path.exists(path):
    #checks if file exists
        raise CharacterNotFoundError(f"Character {character_name} not found.")
    os.remove(path)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    character['experience'] += xp_amount
    while character['experience'] >= character['level'] * 100:
        character['level'] += 1
        character['max_health'] += 10
        character['strength'] += 2
        character['magic'] += 2
        character['health'] = character['max_health']
        character['experience'] -= character['level'] * 100

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    character['gold'] += amount
    if character['gold'] < 0:
        raise ValueError("Gold cannot be negative.")
    return character['gold']

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    character['health'] += amount
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return amount
def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    if character['health'] <= 0:
        return True
    else:
        return False

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if is_character_dead(character) == True:
        character['health'] = character['max_health'] // 2
        return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_fields = [
        'name', 'class', 'level', 'health', 'max_health',
        'strength', 'magic', 'experience', 'gold', 'inventory',
        'active_quests', 'completed_quests'
    ]
    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")
        if field in ['level', 'health', 'max_health', 'strength', 'magic', 'experience', 'gold']:
            if not isinstance(character[field], (int, float)):
                raise InvalidSaveDataError(f"Invalid type for {field}: {type(character[field])}")
        if field in ['inventory', 'active_quests', 'completed_quests']:
            if not isinstance(character[field], list):
                raise InvalidSaveDataError(f"Invalid type for {field}: {type(character[field])}")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
    
    # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")


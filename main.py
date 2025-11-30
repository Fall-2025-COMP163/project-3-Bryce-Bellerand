"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Bryce Bellerand

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("\n=== MAIN MENU ==="
          "\n1. New Game"
          "\n2. Load Game"
          "\n3. Exit")
    choice = input("Enter your choice (1-3): ")
    correct_input = False
    while not correct_input:
        if choice in ['1', '2', '3']:
            correct_input = True
        else:
            choice = input("Invalid choice. Please enter 1, 2, or 3: ")
    return int(choice)
        

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    character_name = input("Enter your character's name: ")
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    class_choice = input("Enter the number of your choice (1-3): ")
    class_dict = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
    correct_input = False
    while not correct_input:
        if class_choice in class_dict:
            character_class = class_dict[class_choice]
            correct_input = True
        else:
            class_choice = input("Invalid choice. Please enter 1, 2, or 3: ")
    try:
        current_character = character_manager.create_character(character_name, character_class)
        character_manager.save_character(current_character)
        print(f"Character '{character_name}' the {character_class} created successfully!")
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error creating character: {e}")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("No saved characters found.")
        return
    print("\n=== SAVED CHARACTERS ===")
    for idx, char_name in enumerate(saved_characters, start=1):
        print(f"{idx}. {char_name}")
    choice = input("Enter the number of the character to load: ")
    correct_input = False
    while not correct_input:
        if choice.isdigit() and 1 <= int(choice) <= len(saved_characters):
            selected_name = saved_characters[int(choice) - 1]
            correct_input = True
        else:
            choice = input(f"Invalid choice. Please enter a number between 1 and {len(saved_characters)}: ")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select a valid option.")

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\n=== GAME MENU ==="
          "\n1. View Character Stats"
          "\n2. View Inventory"
          "\n3. Quest Menu"
          "\n4. Explore (Find Battles)"
          "\n5. Shop"
          "\n6. Save and Quit")
    choice = input("Enter your choice (1-6): ")
    correct_input = False
    while not correct_input:
        if choice in ['1', '2', '3', '4', '5', '6']:
            correct_input = True
        else:
            choice = input("Invalid choice. Please enter a number between 1 and 6: ")
    return int(choice)

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    print("\n=== CHARACTER STATS ===")
    print(f"Name: {current_character['name']}")
    print(f"Class: {current_character['class']}")
    print(f"Level: {current_character['level']}")
    print(f"Health: {current_character['health']}/{current_character['max_health']}")
    print(f"Gold: {current_character['gold']}")
    print("Stats:")
    for stat, value in current_character['stats'].items():
        print(f"  {stat.capitalize()}: {value}")
    quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    print("\n=== INVENTORY ===")
    inventory = current_character['inventory']
    if not inventory:
        print("Your inventory is empty.")
        return
    for item, item_id in enumerate(inventory, start=1):
        items = all_items.get(item_id, {'name': 'Unknown Item'})
        print(f"{item}. {items['name']} (ID: {item_id})")
    print("Options:")
    print("1. Use Item")
    print("2. Equip Item")
    print("3. Drop Item")
    print("4. Back to Game Menu")
    choice = input("Enter your choice (1-4): ")
    correct_input = False
    while not correct_input:
        if choice in ['1', '2', '3', '4']:
            correct_input = True
        else:
            choice = input("Invalid choice. Please enter a number between 1 and 4: ")
    choice = int(choice)
    
def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    print("\n=== QUEST MENU ==="
          "\n1. View Active Quests"
          "\n2. View Available Quests"
          "\n3. View Completed Quests"
          "\n4. Accept Quest"
          "\n5. Abandon Quest"
          "\n6. Complete Quest (for testing)"
          "\n7. Back")
    choice = input("Enter your choice (1-7): ")
    correct_input = False
    while not correct_input:
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            correct_input = True
        else:
            choice = input("Invalid choice. Please enter a number between 1 and 7: ")
    choice = int(choice)

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    print("\n=== SHOP ===")
    print(f"Your Gold: {current_character['gold']}")
    print("Available Items:")
    for item_id, item_data in all_items.items():
        print(f"ID: {item_id} - {item_data['name']} - Cost: {item_data['cost']} Gold")
    print("Options:")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back to Game Menu")
    choice = input("Enter your choice (1-3): ")
    correct_input = False
    while not correct_input:
        if choice in ['1', '2', '3']:
            correct_input = True
        else:
            choice = input("Invalid choice. Please enter a number between 1 and 3: ")
    choice = int(choice)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    all_quests = game_data.load_quests()
    all_items = game_data.load_items()
    character_manager.load_character(current_character)

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print("\n=== YOU HAVE DIED ===")
    print("1. Revive (Cost: 50 Gold)")
    print("2. Quit to Main Menu")
    choice = input("Enter your choice (1-2): ")
    correct_input = False
    while not correct_input:
        if choice in ['1', '2']:
            correct_input = True
        else:
            choice = input("Invalid choice. Please enter 1 or 2: ")
    choice = int(choice)

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()
    


"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Bryce Bellerand

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    acceptable_quests = []
    for qid in quest_data_dict:
        quest = quest_data_dict[qid]
        if character['level'] >= quest['required_level']:
            prereq = quest['prerequisite']
            if prereq == "NONE" or prereq in character['completed_quests']:
                if qid not in character['completed_quests'] and qid not in character['active_quests']:
                    acceptable_quests.append(qid)

    if not acceptable_quests:
        return False

    # Accept the first available quest
    quest_to_accept = acceptable_quests[0]
    character['active_quests'].append(quest_to_accept)
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found.")
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest ID '{quest_id}' is not active.")
    quest = quest_data_dict[quest_id]
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    character['experience'] += quest['reward_xp']
    character['gold'] += quest['reward_gold']
    return {
        'reward_xp': quest['reward_xp'],
        'reward_gold': quest['reward_gold']
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest ID '{quest_id}' is not active.")
    character['active_quests'].remove(quest_id)
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    return [quest_data_dict[qid] for qid in character['active_quests'] if qid in quest_data_dict]
    

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    return [quest_data_dict[qid] for qid in character['completed_quests'] if qid in quest_data_dict]

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available_quests = []
    for qid in quest_data_dict:
        quest = quest_data_dict[qid]
        if character['level'] >= quest['required_level']:
            prereq = quest['prerequisite']
            if prereq == "NONE" or prereq in character['completed_quests']:
                if qid not in character['completed_quests'] and qid not in character['active_quests']:
                    available_quests.append(quest)
    return available_quests

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    check_completed = quest_id in character['completed_quests']
    if check_completed:
        return True
    else:
        return False
def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    check_active = quest_id in character['active_quests']
    if check_active:
        return True
    else:
        return False

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]
    if character['level'] < quest['required_level']:
        return False
    prereq = quest['prerequisite']
    if prereq != "NONE" and prereq not in character['completed_quests']:
        return False
    if quest_id in character['completed_quests']:
        return False
    if quest_id in character['active_quests']:
        return False
    else:
        return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found.")
    chain = []
    current_quest_id = quest_id
    while current_quest_id != "NONE":
        if current_quest_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest ID '{current_quest_id}' not found.")
        chain.insert(0, current_quest_id)
        current_quest = quest_data_dict[current_quest_id]
        current_quest_id = current_quest['prerequisite']
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    total_quests = len(quest_data_dict)
    completed_quests = len(character['completed_quests'])
    percentage = (completed_quests / total_quests) * 100
    return percentage

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0
    for qid in character['completed_quests']:
        if qid in quest_data_dict:
            quest = quest_data_dict[qid]
            total_xp += quest['reward_xp']
            total_gold += quest['reward_gold']
    return {
        'total_xp': total_xp,
        'total_gold': total_gold
    }

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    filtered_quests = []
    for qid in quest_data_dict:
        quest = quest_data_dict[qid]
        if min_level <= quest['required_level'] <= max_level:
            filtered_quests.append(quest)
    return filtered_quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"Rewards: {quest_data['reward_xp']} XP, {quest_data['reward_gold']} Gold")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    for quest in quest_list:
        print(f"Title: {quest['title']}")
        print(f"Required Level: {quest['required_level']}")
        print(f"Rewards: {quest['reward_xp']} XP, {quest['reward_gold']} Gold")
        print("---")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    active_count = len(character['active_quests'])
    completed_count = len(character['completed_quests'])
    completion_percentage = get_quest_completion_percentage(character, quest_data_dict)
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== CHARACTER QUEST PROGRESS ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion Percentage: {completion_percentage:.2f}%")
    print(f"Total Rewards Earned: {total_rewards['total_xp']} XP, {total_rewards['total_gold']} Gold")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for qid in quest_data_dict:
        quest = quest_data_dict[qid]
        prereq = quest['prerequisite']
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite quest ID '{prereq}' for quest '{qid}' not found.")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    #
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    #
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")


from reinforcement.feedback_store import load_feedback,save_feedback
from personalization.personalization_engine import update_preferences


REWARD_MAP = {
    "click": 1,
    "like": 2,
    "order": 3,
    "skip": -1
}


def store_feedback(user_id, food_id, event):

    # Ensure user_id is a string
    user_id = str(user_id)
    reward = REWARD_MAP.get(event, 0)

    feedback_df = load_feedback()

    new_row = {
        "user_id": user_id,
        "dish_name": food_id,
        "action": event,
        "reward": reward
    }

    feedback_df.loc[len(feedback_df)] = new_row

    save_feedback(feedback_df)

    update_preferences(user_id, food_id, reward)

    return new_row


def remove_feedback(user_id, food_id, event):
    """Remove a specific feedback action"""
    
    feedback_df = load_feedback()
    
    # Convert user_id to string for comparison
    user_id = str(user_id)
    
    # Find and remove the matching row(s) - only remove the LAST occurrence
    mask = (feedback_df['user_id'].astype(str) == user_id) & \
           (feedback_df['dish_name'] == food_id) & \
           (feedback_df['action'] == event)
    
    if mask.any():
        # Get the reward to reverse it
        reward = REWARD_MAP.get(event, 0)
        
        # Get indices where mask is True
        matching_indices = feedback_df[mask].index
        
        # Remove only the last occurrence
        last_index = matching_indices[-1]
        feedback_df = feedback_df.drop(last_index)
        
        # Reset index to maintain clean CSV
        feedback_df = feedback_df.reset_index(drop=True)
        
        save_feedback(feedback_df)
        
        # Reverse the preference update
        update_preferences(user_id, food_id, -reward)
        
        return {"removed": True, "action": event, "reward": -reward}
    
    return {"removed": False, "message": "Action not found"}
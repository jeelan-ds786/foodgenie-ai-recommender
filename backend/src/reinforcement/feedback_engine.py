from reinforcement.feedback_store import load_feedback,save_feedback
from personalization.personalization_engine import update_preferences


REWARD_MAP = {
    "click": 1,
    "order": 3,
    "skip": -1
}


def store_feedback(user_id, food_id, event):

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
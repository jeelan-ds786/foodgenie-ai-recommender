from reinforcement.feedback_store import load_feedback,save_feedback
from personalization.personalization_engine import update_preferences


REWARD_MAP = {
    "click":1,
    "order":3,
    "skip":-1
}


def record_feedback(user_id,dish_name,action):

    reward = REWARD_MAP.get(action,0)

    feedback_df = load_feedback()

    new_row = {
        "user_id":user_id,
        "dish_name":dish_name,
        "action":action,
        "reward":reward
    }

    feedback_df.loc[len(feedback_df)] = new_row

    save_feedback(feedback_df)

    update_preferences(user_id,dish_name,reward)

    return new_row
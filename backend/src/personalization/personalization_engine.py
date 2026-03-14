from personalization.preference_store import load_preferences, save_preferences


def update_preferences(user_id,dish_name,reward):
    df = load_preferences()

    user_rows = df[(df['user_id'] == user_id) & (df['dish_name']==dish_name)]

    if len(user_rows) ==0:

        df.loc[len(df)] = {
            "user_id":user_id,
            "dish_name":dish_name,
            "score":reward
        }

    else:

        idx = user_rows.index[0]
        df.loc[idx,"score"] += reward

    save_preferences(df)



def get_user_preferences(user_id):
    df = load_preferences()

    user_df = df[df["user_id"] == user_id]

    if len(user_df) == 0 :
        return []
    
    return list(
        user_df.sort_values("score",ascending=False).head(10)
    )

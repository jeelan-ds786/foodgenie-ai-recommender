from features.feature_store import load_features, save_features


def store_candidate_features(candidates):

    feature_df = candidates[[
        "dish_name",
        "similarity_score",
        "rating_num",
        "rating_count_num"
    ]]

    save_features(feature_df)

    return feature_df
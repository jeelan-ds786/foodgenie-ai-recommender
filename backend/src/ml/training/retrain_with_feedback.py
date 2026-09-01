"""
Retrain the XGBoost ranking model using real user feedback data
This should be run periodically (daily/weekly) to incorporate new user behavior
"""

import pandas as pd
import xgboost as xgb
import joblib
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR.parent.parent / "data"

# Real feedback files
FEEDBACK_FILE = DATA_DIR / "feedback" / "user_feedback.csv"
PREFERENCE_FILE = DATA_DIR / "feedback" / "user_preference.csv"

# Processed food data
FOOD_DATA_FILE = DATA_DIR / "processed" / "dataPreprocessed_FoodGenie_Dataset.parquet"

# Model paths
MODEL_DIR = BASE_DIR / "models"
CURRENT_MODEL = MODEL_DIR / "xgboost_food_ranker.pkl"
BACKUP_MODEL = MODEL_DIR / f"xgboost_food_ranker_backup_{datetime.now().strftime('%Y%m%d')}.pkl"
OUTPUT_MODEL = MODEL_DIR / "xgboost_food_ranker_updated.pkl"


def check_sufficient_data(min_interactions=100):
    """Check if we have enough real data to retrain"""
    if not FEEDBACK_FILE.exists():
        print("❌ No feedback data found yet")
        return False
    
    feedback_df = pd.read_csv(FEEDBACK_FILE)
    
    if len(feedback_df) < min_interactions:
        print(f"⚠️  Only {len(feedback_df)} interactions found. Need at least {min_interactions} to retrain.")
        return False
    
    print(f"✅ Found {len(feedback_df)} interactions - sufficient for retraining")
    return True


def build_training_data_from_feedback():
    """
    Convert real user feedback into training format for XGBoost
    """
    print("\n📊 Building training data from real feedback...")
    
    # Load real feedback
    feedback_df = pd.read_csv(FEEDBACK_FILE)
    food_data = pd.read_parquet(FOOD_DATA_FILE)
    
    # Load preferences (aggregated scores)
    if PREFERENCE_FILE.exists():
        preference_df = pd.read_csv(PREFERENCE_FILE)
    else:
        preference_df = pd.DataFrame()
    
    print(f"  - {len(feedback_df)} feedback events")
    print(f"  - {len(feedback_df['user_id'].unique())} unique users")
    print(f"  - {len(feedback_df['dish_name'].unique())} unique dishes")
    
    # Aggregate feedback per user-dish pair
    aggregated = (
        feedback_df
        .groupby(['user_id', 'dish_name'])
        .agg({
            'reward': 'sum',  # Sum all rewards for this user-dish
            'action': 'count'  # Count interactions
        })
        .rename(columns={'action': 'interaction_count'})
        .reset_index()
    )
    
    # Merge with food metadata to get features
    training_data = aggregated.merge(
        food_data[['dish_name', 'restaurant_name', 'cuisine', 'category', 
                   'rating_num', 'rating_count_num', 'city']],
        on='dish_name',
        how='left'
    )
    
    # Add preference scores if available
    if not preference_df.empty:
        training_data = training_data.merge(
            preference_df[['user_id', 'dish_name', 'score']].rename(columns={'score': 'preference_score'}),
            on=['user_id', 'dish_name'],
            how='left'
        )
        training_data['preference_score'].fillna(0, inplace=True)
    else:
        training_data['preference_score'] = 0
    
    # Create features
    training_data['context_score'] = 1.0  # Placeholder - can add time/weather context
    training_data['similarity_score'] = 1.0  # Placeholder - can add if we have query context
    
    # Ensure reward is non-negative for ranking
    training_data['reward'] = training_data['reward'].clip(lower=0)
    
    print(f"✅ Built training dataset with {len(training_data)} examples")
    
    return training_data


def retrain_model(training_data):
    """
    Retrain XGBoost model with new data
    """
    print("\n🤖 Retraining XGBoost model...")
    
    # Define features
    features = [
        'similarity_score',
        'rating_num',
        'rating_count_num',
        'context_score',
        'preference_score',
        'interaction_count'
    ]
    
    # Prepare data
    X = training_data[features].fillna(0)
    y = training_data['reward'].astype(int)
    
    # Group by user for ranking
    groups = training_data.groupby('user_id').size().to_list()
    
    print(f"  - Features: {len(features)}")
    print(f"  - Training examples: {len(X)}")
    print(f"  - User groups: {len(groups)}")
    
    # Load existing model as starting point (warm start)
    if CURRENT_MODEL.exists():
        print("  - Loading existing model as starting point...")
        old_model = joblib.load(CURRENT_MODEL)
        n_estimators = old_model.n_estimators
    else:
        n_estimators = 300
    
    # Train new model
    model = xgb.XGBRanker(
        objective="rank:ndcg",
        n_estimators=n_estimators,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="ndcg",
        random_state=42
    )
    
    model.fit(X, y, group=groups, verbose=True)
    
    print("✅ Model training complete")
    
    return model


def backup_and_deploy_model(model):
    """
    Backup old model and deploy new one
    """
    print("\n💾 Deploying updated model...")
    
    # Backup current model
    if CURRENT_MODEL.exists():
        joblib.dump(joblib.load(CURRENT_MODEL), BACKUP_MODEL)
        print(f"  - Backed up old model to: {BACKUP_MODEL.name}")
    
    # Save new model
    joblib.dump(model, OUTPUT_MODEL)
    print(f"  - Saved new model to: {OUTPUT_MODEL.name}")
    
    # Replace current model
    if OUTPUT_MODEL.exists():
        OUTPUT_MODEL.replace(CURRENT_MODEL)
        print(f"  - Deployed as: {CURRENT_MODEL.name}")
    
    print("✅ Model deployment complete")


def main():
    """
    Main retraining pipeline
    """
    print("=" * 60)
    print("🔄 RETRAINING MODEL WITH REAL USER FEEDBACK")
    print("=" * 60)
    
    # Step 1: Check if we have enough data
    if not check_sufficient_data(min_interactions=50):  # Lowered threshold for demo
        print("\n⚠️  Not enough data to retrain. Continue collecting feedback.")
        print("   Run this script again once you have more user interactions.")
        return
    
    # Step 2: Build training data from real feedback
    training_data = build_training_data_from_feedback()
    
    if len(training_data) == 0:
        print("❌ No valid training data generated")
        return
    
    # Step 3: Retrain model
    model = retrain_model(training_data)
    
    # Step 4: Backup and deploy
    backup_and_deploy_model(model)
    
    print("\n" + "=" * 60)
    print("🎉 RETRAINING COMPLETE!")
    print("=" * 60)
    print("\n📊 Stats:")
    print(f"  - Training examples: {len(training_data)}")
    print(f"  - Unique users: {training_data['user_id'].nunique()}")
    print(f"  - Unique dishes: {training_data['dish_name'].nunique()}")
    print("\n💡 Tip: Run this script weekly to keep the model updated!")
    print("   You can also set up a cron job for automated retraining.")


if __name__ == "__main__":
    main()

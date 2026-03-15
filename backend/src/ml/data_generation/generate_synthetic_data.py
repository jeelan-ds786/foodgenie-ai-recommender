import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

NUM_USERS = 1000
NUM_INTERACTIONS = 50000
MAX_FOODS = 20000

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve()
PROJECT_ROOT = BASE_DIR.parents[4]

DATA_DIR = PROJECT_ROOT / "data"

PROCESSED_DIR = DATA_DIR / "processed"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
FEATURE_STORE_DIR = SYNTHETIC_DIR / "feature_store"

PROCESSED_FILE = PROCESSED_DIR / "dataPreprocessed_FoodGenie_Dataset.parquet"

SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
FEATURE_STORE_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("FoodGenie Synthetic Data Generator")
print("=" * 60)

print("Project root:", PROJECT_ROOT)
print("Processed dataset:", PROCESSED_FILE)

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

print("\nLoading processed dataset...")

if not PROCESSED_FILE.exists():
    raise FileNotFoundError(
        f"Processed dataset not found at {PROCESSED_FILE}"
    )

dataset = pd.read_parquet(PROCESSED_FILE)

print(f"Dataset loaded with {len(dataset):,} rows")

# --------------------------------------------------
# FOOD CATALOG
# --------------------------------------------------

print("\nBuilding food catalog...")

foods = dataset[
    [
        "restaurant_id",
        "restaurant_name",
        "dish_name",
        "price",
        "veg_or_non_veg",
        "rating_num",
        "rating_count_num",
        "city",
        "cuisine"
    ]
].drop_duplicates()

# clean NaNs
foods["rating_num"] = foods["rating_num"].fillna(0)
foods["rating_count_num"] = foods["rating_count_num"].fillna(0)
foods["price"] = foods["price"].fillna(0)

# reduce catalog size
if len(foods) > MAX_FOODS:
    foods = foods.sample(MAX_FOODS, random_state=42)

foods = foods.reset_index(drop=True)

# create IDs
foods["food_id"] = ["F" + str(i) for i in range(len(foods))]

# rename columns
foods = foods.rename(
    columns={
        "veg_or_non_veg": "veg_flag",
        "rating_num": "rating",
        "rating_count_num": "rating_count"
    }
)

# spice level simulation
foods["spice_level"] = np.random.choice(
    ["low", "medium", "high"],
    len(foods),
    p=[0.2, 0.5, 0.3]
)

foods = foods[
    [
        "food_id",
        "restaurant_id",
        "restaurant_name",
        "dish_name",
        "price",
        "spice_level",
        "veg_flag",
        "rating",
        "rating_count",
        "city",
        "cuisine"
    ]
]

foods.to_parquet(SYNTHETIC_DIR / "foods.parquet", index=False)

print(f"✓ foods.parquet created ({len(foods):,} foods)")

# --------------------------------------------------
# USERS
# --------------------------------------------------

print("\nGenerating users...")

cities = foods["city"].dropna().unique()

users = pd.DataFrame({
    "user_id": [f"U{i}" for i in range(NUM_USERS)],
    "age": np.random.randint(18, 60, NUM_USERS),
    "diet": np.random.choice(["veg", "nonveg"], NUM_USERS, p=[0.4, 0.6]),
    "spice_preference": np.random.choice(
        ["low", "medium", "high"],
        NUM_USERS,
        p=[0.2, 0.5, 0.3]
    ),
    "budget": np.random.choice(
        ["low", "medium", "high"],
        NUM_USERS,
        p=[0.3, 0.5, 0.2]
    ),
    "city": np.random.choice(cities, NUM_USERS)
})

users.to_parquet(SYNTHETIC_DIR / "users.parquet", index=False)

print(f"✓ users.parquet created ({len(users):,} users)")

# --------------------------------------------------
# INTERACTIONS
# --------------------------------------------------

print("\nSimulating interactions...")

# safe probability calculation
rating_counts = foods["rating_count"].fillna(0)

food_prob = (rating_counts + 1).to_numpy(dtype=float)
food_prob = food_prob / food_prob.sum()

interactions = pd.DataFrame({
    "user_id": np.random.choice(users["user_id"], NUM_INTERACTIONS),
    "food_id": np.random.choice(
        foods["food_id"],
        NUM_INTERACTIONS,
        p=food_prob
    ),
    "impressions": np.ones(NUM_INTERACTIONS, dtype=int),
    "timestamp": pd.date_range(
        start="2025-01-01",
        periods=NUM_INTERACTIONS,
        freq="3min"
    )
})

# click probability
interactions["clicks"] = np.random.choice(
    [0, 1],
    NUM_INTERACTIONS,
    p=[0.7, 0.3]
)

# orders only after clicks
interactions["orders"] = 0

clicked_mask = interactions["clicks"] == 1

interactions.loc[clicked_mask, "orders"] = np.random.choice(
    [0, 1],
    clicked_mask.sum(),
    p=[0.75, 0.25]
)

interactions["time_of_day"] = np.random.choice(
    ["breakfast", "lunch", "dinner"],
    NUM_INTERACTIONS,
    p=[0.2, 0.4, 0.4]
)

interactions.to_parquet(
    SYNTHETIC_DIR / "interactions.parquet",
    index=False
)

print(f"✓ interactions.parquet created ({len(interactions):,} rows)")
print(f"Clicks: {interactions['clicks'].sum():,}")
print(f"Orders: {interactions['orders'].sum():,}")

# --------------------------------------------------
# FEATURE STORE
# --------------------------------------------------

print("\nBuilding feature store...")

feature_store = interactions[["user_id", "food_id"]].drop_duplicates()

feature_store["similarity_score"] = np.random.uniform(
    0.4, 1.0, len(feature_store)
)

feature_store["context_score"] = np.random.uniform(
    0, 1, len(feature_store)
)

feature_store["preference_score"] = np.random.uniform(
    0, 1, len(feature_store)
)

feature_store = feature_store.merge(
    foods[["food_id", "rating", "rating_count"]],
    on="food_id"
)

feature_store["rating_num"] = feature_store["rating"]
feature_store["rating_count_num"] = feature_store["rating_count"]

feature_store = feature_store.drop(columns=["rating", "rating_count"])

feature_store.to_parquet(
    FEATURE_STORE_DIR / "feature_store.parquet",
    index=False
)

print(f"✓ feature_store.parquet created ({len(feature_store):,} rows)")

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("Synthetic data generation completed")
print("=" * 60)

print("\nGenerated files:")
print(SYNTHETIC_DIR / "foods.parquet")
print(SYNTHETIC_DIR / "users.parquet")
print(SYNTHETIC_DIR / "interactions.parquet")
print(FEATURE_STORE_DIR / "feature_store.parquet")
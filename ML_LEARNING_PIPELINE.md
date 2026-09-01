# 🧠 ML Learning Pipeline - How FoodGenie Learns from Users

## 📖 Overview

Your FoodGenie AI system has a **continuous learning pipeline** that improves recommendations based on real user behavior. Here's how it works:

---

## 🔄 The Complete Learning Cycle

```
┌─────────────────────────────────────────────────────────┐
│  1. USER INTERACTIONS                                   │
│     - User searches for food                            │
│     - Views recommendations                             │
│     - Clicks Like ❤️, Skip ⏭️, or Order 🛒              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  2. FEEDBACK COLLECTION (Real-time)                     │
│     ✅ Already implemented!                             │
│                                                          │
│     data/feedback/user_feedback.csv                     │
│     ├─ user_id: "1"                                     │
│     ├─ dish_name: "Chicken Biryani"                     │
│     ├─ action: "like"                                   │
│     └─ reward: 2                                        │
│                                                          │
│     data/feedback/user_preference.csv                   │
│     ├─ Aggregated user-dish scores                      │
│     └─ Updated in real-time                             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  3. PERIODIC RETRAINING                                 │
│     🆕 New script: retrain_with_feedback.py             │
│                                                          │
│     Runs: Daily/Weekly (you decide)                     │
│                                                          │
│     Process:                                            │
│     a) Checks if enough new data (min 50-100 actions)   │
│     b) Converts feedback CSV to training format         │
│     c) Retrains XGBoost model                           │
│     d) Backs up old model                               │
│     e) Deploys new model                                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  4. IMPROVED RECOMMENDATIONS                            │
│     - New model loaded automatically                    │
│     - Better predictions based on real behavior         │
│     - Personalized to actual user preferences           │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  5. MORE USER INTERACTIONS                              │
│     - Cycle repeats continuously                        │
│     - Model keeps improving over time                   │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow Diagram

```
Current State:
--------------
Synthetic Data (Cold Start)
    └─> models/xgboost_food_ranker.pkl (Initial Model)
            └─> Used for recommendations

With Real Users:
---------------
User Actions (Like/Skip/Order)
    └─> feedback/user_feedback.csv (Growing daily)
    └─> feedback/user_preference.csv (Aggregated)
            │
            ▼
    retrain_with_feedback.py (Run weekly)
            │
            ▼
    models/xgboost_food_ranker_updated.pkl
            │
            ▼
    models/xgboost_food_ranker.pkl (Deployed)
            │
            ▼
    Better Recommendations!
```

---

## 🎯 What Each File Does

### **Real-time Feedback Collection** (Already Working ✅)

| File | Purpose |
|------|---------|
| `data/feedback/user_feedback.csv` | Stores every user action (like, skip, order) with timestamp |
| `data/feedback/user_preference.csv` | Aggregated scores per user-dish combination |
| `backend/src/reinforcement/feedback_engine.py` | Calculates rewards and updates preferences |
| `backend/src/api/v1/routes/feedback.py` | API endpoints for feedback |

### **Periodic Model Retraining** (New Script 🆕)

| File | Purpose |
|------|---------|
| `backend/src/ml/training/retrain_with_feedback.py` | **Main retraining script** |
| `backend/src/models/xgboost_food_ranker.pkl` | Current production model |
| `backend/src/models/xgboost_food_ranker_backup_YYYYMMDD.pkl` | Backup models |

---

## 🚀 How to Retrain the Model

### **Manual Retraining** (Recommended for now)

```bash
# Navigate to training directory
cd backend/src/ml/training

# Check how many interactions you have
cat ../../../../data/feedback/user_feedback.csv | wc -l

# Retrain when you have 50+ interactions
python retrain_with_feedback.py
```

**Output:**
```
============================================================
🔄 RETRAINING MODEL WITH REAL USER FEEDBACK
============================================================

✅ Found 156 interactions - sufficient for retraining

📊 Building training data from real feedback...
  - 156 feedback events
  - 12 unique users
  - 45 unique dishes
✅ Built training dataset with 45 examples

🤖 Retraining XGBoost model...
  - Features: 6
  - Training examples: 45
  - User groups: 12
✅ Model training complete

💾 Deploying updated model...
  - Backed up old model to: xgboost_food_ranker_backup_20260329.pkl
  - Saved new model to: xgboost_food_ranker_updated.pkl
  - Deployed as: xgboost_food_ranker.pkl
✅ Model deployment complete

============================================================
🎉 RETRAINING COMPLETE!
============================================================
```

### **Automated Retraining** (Production Setup)

Option 1: **Cron Job** (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line to retrain weekly (Sunday at 2 AM)
0 2 * * 0 cd /path/to/backend/src/ml/training && /path/to/venv/bin/python retrain_with_feedback.py >> /path/to/logs/retrain.log 2>&1
```

Option 2: **Python Scheduler** (Any OS)
```python
# Run this script continuously
import schedule
import time
from retrain_with_feedback import main

schedule.every().sunday.at("02:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

---

## 📈 Learning Metrics

### **Monitor Model Improvement**

Track these metrics over time:

1. **Feedback Volume**
   ```bash
   wc -l data/feedback/user_feedback.csv
   ```

2. **User Engagement**
   ```python
   df = pd.read_csv('data/feedback/user_feedback.csv')
   print(f"Total users: {df['user_id'].nunique()}")
   print(f"Avg actions per user: {len(df) / df['user_id'].nunique():.2f}")
   ```

3. **Action Distribution**
   ```python
   print(df['action'].value_counts())
   # Shows: like, order, skip ratios
   ```

4. **Model Version**
   ```bash
   ls -lt backend/src/models/xgboost_food_ranker*.pkl
   ```

---

## 🎓 The Learning Process Explained

### **Stage 1: Cold Start (Day 0)**
- Model trained on synthetic data
- No real user behavior yet
- "Best guess" recommendations

### **Stage 2: Early Learning (Week 1-4)**
- Collecting real user feedback
- CSV files growing
- Still using synthetic model

### **Stage 3: First Update (Week 4+)**
```bash
# Once you have ~100 interactions
python retrain_with_feedback.py
```
- Model learns real preferences
- Better recommendations
- User satisfaction improves

### **Stage 4: Continuous Learning (Month 2+)**
- Weekly retraining
- Model adapts to trends
- Seasonal preferences captured
- New dishes learned

---

## 🧪 Example Learning Scenario

### **Week 1: Initial State**
```
User searches "biryani"
→ Model recommends based on ratings only
→ User orders "Chicken Biryani"
→ Feedback saved: action=order, reward=3
```

### **Week 4: After 100 Interactions**
```bash
python retrain_with_feedback.py
```
Model learns:
- "Chicken Biryani" is popular
- User X prefers spicy food
- Orders spike on weekends

### **Week 5: Improved Recommendations**
```
Same user searches "biryani"
→ Model now prioritizes "Chicken Biryani" (learned preference)
→ Also suggests "Mutton Biryani" (similar to liked items)
→ Higher chance of order!
```

---

## 🔧 Configuration

### **Retraining Thresholds**

Edit in `retrain_with_feedback.py`:

```python
# Minimum interactions before retraining
MIN_INTERACTIONS = 100  # Increase for production

# Model parameters
n_estimators = 300       # More trees = better but slower
learning_rate = 0.05     # Lower = more careful learning
max_depth = 6            # Tree complexity
```

### **Reward System**

Edit in `feedback_engine.py`:

```python
REWARD_MAP = {
    "click": 1,    # Viewed item
    "like": 2,     # Liked item
    "order": 3,    # Strongest signal
    "skip": -1     # Negative feedback
}
```

---

## 📊 Monitoring Dashboard (Future Enhancement)

Track model performance:

```python
# Create training_metrics.json after each retrain
{
    "timestamp": "2026-03-29T10:30:00",
    "total_interactions": 456,
    "unique_users": 25,
    "unique_dishes": 120,
    "model_accuracy": 0.85,
    "avg_ndcg": 0.92
}
```

---

## 🎯 Best Practices

### ✅ DO:
- Retrain weekly/bi-weekly initially
- Monitor feedback volume
- Keep model backups
- Track user engagement metrics
- Test new model before full deployment

### ❌ DON'T:
- Retrain with < 50 interactions
- Delete old model without backup
- Ignore error logs
- Retrain too frequently (waste compute)

---

## 🚨 Troubleshooting

### Issue: "Not enough data to retrain"
**Solution:** Wait until you have 50+ user interactions

### Issue: "Model performance worse after retrain"
**Solution:** Restore backup model:
```bash
cp models/xgboost_food_ranker_backup_20260329.pkl models/xgboost_food_ranker.pkl
```

### Issue: "Training fails with error"
**Solution:** Check data quality:
```python
df = pd.read_csv('data/feedback/user_feedback.csv')
print(df.isnull().sum())  # Check for missing values
print(df.dtypes)           # Check data types
```

---

## 🎉 Summary

**You have a complete learning pipeline!**

1. ✅ **Feedback Collection** - Working (likes, skips, orders saved)
2. 🆕 **Retraining Script** - Ready to use
3. 📈 **Continuous Improvement** - Just run the script weekly

**Start learning from real users today:**
```bash
# After collecting some feedback
cd backend/src/ml/training
python retrain_with_feedback.py
```

**The model will automatically improve over time! 🚀**

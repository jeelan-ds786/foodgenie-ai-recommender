# 🎯 Quick Reference: Model Learning from Users

## ❓ Your Question

**"We don't have real user interactions. How will the model learn customer behavior?"**

## ✅ Answer

**You DO have a complete learning system!** Here's what's already working:

---

## 🔄 The System You Built

### **1. Real-Time Feedback Collection** ✅ Already Working

Every time a user clicks Like/Skip/Order:

```
User Action → API → feedback_engine.py → CSV Files
```

**Files Being Updated:**
- `data/feedback/user_feedback.csv` - Every action logged
- `data/feedback/user_preference.csv` - Aggregated scores

**Example Data:**
```csv
user_id,dish_name,action,reward
1,Chicken Biryani,like,2
1,Paneer Tikka,order,3
1,Fish Curry,skip,-1
```

### **2. Model Retraining** 🆕 New Script Added

When you have enough data (50+ interactions), run:

```bash
cd backend/src/ml/training
python retrain_with_feedback.py
```

**What it does:**
1. ✅ Reads real user feedback from CSV
2. ✅ Converts to ML training format
3. ✅ Retrains XGBoost model
4. ✅ Backs up old model
5. ✅ Deploys new model
6. ✅ Restart server → Better recommendations!

---

## 📊 Learning Timeline

### **Week 1-4: Data Collection Phase**
```
Users interact → Feedback saved to CSV → Model stays same
```
- **Goal:** Collect 50-100 interactions
- **Check progress:** `wc -l data/feedback/user_feedback.csv`

### **Week 4: First Retraining**
```bash
python retrain_with_feedback.py
```
- **Result:** Model learns real preferences
- **Better recommendations immediately**

### **Ongoing: Weekly Retraining**
```bash
# Manual (run every Sunday)
python retrain_with_feedback.py

# OR Automated (runs continuously)
python schedule_retraining.py
```

---

## 🚀 Quick Start Commands

### **Check Current Feedback**
```bash
# How many interactions collected?
cat data/feedback/user_feedback.csv | wc -l

# View recent feedback
tail -20 data/feedback/user_feedback.csv
```

### **Retrain Model (Manual)**
```bash
cd backend/src/ml/training
python retrain_with_feedback.py
```

### **Automated Retraining**
```bash
# Start scheduler (runs in background)
cd backend/src/ml/training
python schedule_retraining.py

# Check logs
tail -f ../../../logs/retraining_schedule.log
```

---

## 🎓 How It Learns

### **Before Retraining (Synthetic Data)**
```
User searches "biryani"
→ Model: Uses initial synthetic training
→ Recommends: Based on ratings only
```

### **After Retraining (Real Data)**
```
User searches "biryani"
→ Model: Learned from 200 real interactions
→ Knows: User X likes spicy food
→ Knows: Chicken Biryani gets most orders
→ Recommends: Personalized suggestions
→ Result: Higher order rate! 📈
```

---

## 📈 Monitor Learning Progress

### **Track Feedback Volume**
```python
import pandas as pd

df = pd.read_csv('data/feedback/user_feedback.csv')

print(f"Total interactions: {len(df)}")
print(f"Unique users: {df['user_id'].nunique()}")
print(f"Action breakdown:\n{df['action'].value_counts()}")
```

### **Check Model Updates**
```bash
# List all model versions
ls -lt backend/src/models/*.pkl

# Current model
ls -lh backend/src/models/xgboost_food_ranker.pkl
```

---

## 🔧 Files You Need to Know

| File | Purpose | Status |
|------|---------|--------|
| `feedback/user_feedback.csv` | Stores all user actions | ✅ Working |
| `feedback/user_preference.csv` | Aggregated scores | ✅ Working |
| `ml/training/retrain_with_feedback.py` | Retraining script | 🆕 New |
| `ml/training/schedule_retraining.py` | Auto scheduler | 🆕 New |
| `models/xgboost_food_ranker.pkl` | Current model | ✅ deployed |

---

## 💡 Key Points

1. **You ARE collecting user feedback** - Every like/skip/order is saved ✅
2. **Model can learn** - Run `retrain_with_feedback.py` ✅
3. **Automatic updates** - Use scheduler for hands-off operation ✅
4. **Cold start solved** - Initial synthetic data gets you going ✅
5. **Continuous improvement** - Model gets better weekly ✅

---

## ⚠️ Important Notes

### **Minimum Data Threshold**
- Need **50-100 interactions** minimum for first retrain
- More data = better model
- Check current count: `wc -l data/feedback/user_feedback.csv`

### **Retraining Frequency**
- **Week 1-4:** No retraining (collecting data)
- **Week 4:** First retrain
- **After that:** Weekly retraining
- **Don't:** Retrain every day (waste of compute)

### **Model Backups**
- Old models backed up automatically
- Format: `xgboost_food_ranker_backup_YYYYMMDD.pkl`
- Keep for 30 days

---

## 🎉 Summary

### **What You Have:**
✅ Feedback collection system (working)  
✅ CSV storage (growing daily)  
✅ Retraining script (ready to use)  
✅ Automated scheduler (optional)  
✅ Model backup system  

### **What To Do:**
1. Let users interact (collecting data happens automatically)
2. When you reach 50+ interactions, run:
   ```bash
   python retrain_with_feedback.py
   ```
3. Restart backend server
4. Enjoy better recommendations!
5. Repeat weekly

### **The Model WILL Learn! 🧠**

Your system is designed to continuously improve from real user behavior. The more users interact, the smarter it gets!

---

## 📚 Documentation

- **Full Details:** [ML_LEARNING_PIPELINE.md](ML_LEARNING_PIPELINE.md)
- **Setup Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)

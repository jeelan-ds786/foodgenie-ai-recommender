"""
Automated scheduler for periodic model retraining
Run this script continuously to automatically retrain the model weekly
"""

import schedule
import time
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from retrain_with_feedback import main as retrain_model

# Setup logging
LOG_DIR = Path(__file__).resolve().parents[4] / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "retraining_schedule.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def scheduled_retrain():
    """
    Wrapper function for scheduled retraining
    """
    try:
        logger.info("=" * 60)
        logger.info("🔄 Scheduled retraining started")
        logger.info("=" * 60)
        
        retrain_model()
        
        logger.info("=" * 60)
        logger.info("✅ Scheduled retraining completed successfully")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Retraining failed: {str(e)}", exc_info=True)


def main():
    """
    Setup and run the scheduler
    """
    print("=" * 60)
    print("📅 FoodGenie ML Model Retraining Scheduler")
    print("=" * 60)
    print()
    print("Configuration:")
    print("  - Schedule: Every Sunday at 2:00 AM")
    print("  - Log file:", LOG_FILE)
    print()
    print("The scheduler is now running...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Schedule weekly retraining (every Sunday at 2 AM)
    schedule.every().sunday.at("02:00").do(scheduled_retrain)
    
    # Optional: Add daily check at different times
    # schedule.every().day.at("03:00").do(scheduled_retrain)
    
    logger.info("Scheduler started successfully")
    logger.info("Next retraining: %s", schedule.next_run())
    
    # Run continuously
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        print("\n👋 Scheduler stopped")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}", exc_info=True)
        print(f"\n❌ Scheduler crashed: {str(e)}")


if __name__ == "__main__":
    main()

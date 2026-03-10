import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from context_engine import get_context_preferences

context = get_context_preferences("Chennai")

print(context)
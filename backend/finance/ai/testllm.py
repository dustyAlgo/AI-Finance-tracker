import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
# test_agent.py
from finance.ai.agent import run_finance_agent
try:
    result = run_finance_agent(123, 2026, 2)
    print("✅ SUCCESS:", result[:200])
except Exception as e:
    print("❌ ERROR:", str(e))


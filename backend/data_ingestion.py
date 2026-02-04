# synthetic_data_ingestion_django.py
"""
Django ORM-based Synthetic Data Ingestion Script

- Generates 50 users
- Creates standard categories per user
- Creates 100 transactions per user with dates in the last year
- predicted_category and anomaly_z_score are left NULL
- MonthlySummary is left empty for later computation

Usage:
    python manage.py shell
    >>> exec(open('data_ingestion.py').read())

Requirements:
    - Django project configured with your models.py
    - Faker installed: pip install faker
"""

import random
from datetime import datetime, timedelta
from faker import Faker

from django.contrib.auth import get_user_model
from finance.models import Category, Transaction  # adjust 'finance_app' to your app name

fake = Faker()
User = get_user_model()

NUM_USERS = 50
NUM_TRANSACTIONS_PER_USER = 100
CATEGORY_NAMES = ["Food", "Rent", "Travel", "Utilities", "Entertainment", "Healthcare", "Other"]

# ---------------------------
# CREATE USERS
# ---------------------------

users = []
for _ in range(NUM_USERS):
    username = fake.user_name()
    email = fake.unique.email()
    password = "password123"  # default password for all users
    user = User.objects.create_user(username=username, email=email, password=password)
    users.append(user)
print(f"Created {len(users)} users.")

# ---------------------------
# CREATE CATEGORIES PER USER
# ---------------------------

for user in users:
    for cat_name in CATEGORY_NAMES:
        Category.objects.create(user=user, name=cat_name)
print(f"Created {len(CATEGORY_NAMES)} categories per user.")

# ---------------------------
# CREATE TRANSACTIONS
# ---------------------------

for user in users:
    user_categories = list(Category.objects.filter(user=user))
    for _ in range(NUM_TRANSACTIONS_PER_USER):
        type_ = random.choices(["INCOME", "EXPENSE"], weights=[0.3, 0.7])[0]
        amount = round(random.uniform(100, 5000), 2) if type_ == "EXPENSE" else round(random.uniform(5000, 20000), 2)
        category = random.choice(user_categories) if type_ == "EXPENSE" else random.choice(user_categories)
        date = datetime.now().date() - timedelta(days=random.randint(0, 365))
        note = fake.sentence(nb_words=6)
        
        Transaction.objects.create(
            user=user,
            category=category,
            predicted_category=None,
            anomaly_z_score=None,
            type=type_,
            amount=amount,
            date=date,
            note=note
        )
print(f"Created {NUM_TRANSACTIONS_PER_USER} transactions per user.")

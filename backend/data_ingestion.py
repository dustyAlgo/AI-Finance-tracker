import random
from datetime import datetime, timedelta
from faker import Faker

from django.contrib.auth import get_user_model
from finance.models import Category, Transaction

fake = Faker()
User = get_user_model()

NUM_USERS = 50
NUM_TRANSACTIONS_PER_USER = 100

CATEGORY_NAMES = [
    "Food",
    "Rent",
    "Travel",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Other",
]

# Category-specific keywords for realistic notes
CATEGORY_KEYWORDS = {
    "Food": ["pizza", "restaurant", "burger", "lunch", "dinner", "cafe"],
    "Rent": ["rent", "apartment", "house", "flat", "lease", "landlord"],
    "Travel": ["uber", "flight", "bus", "train", "taxi", "airport"],
    "Utilities": ["electricity", "water", "internet", "gas", "bill"],
    "Entertainment": ["movie", "concert", "game", "netflix", "theater"],
    "Healthcare": ["doctor", "medicine", "hospital", "clinic", "pharmacy"],
    "Other": ["misc", "shopping", "purchase", "general", "item"],
}

# ---------------------------
# CREATE USERS
# ---------------------------

users = []
for _ in range(NUM_USERS):
    username = fake.user_name()
    email = fake.unique.email()
    password = "password123"
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
        type_ = random.choices(
            ["INCOME", "EXPENSE"],
            weights=[0.3, 0.7]
        )[0]

        if type_ == "EXPENSE":
            category = random.choice(user_categories)
            amount = round(random.uniform(100, 5000), 2)

            # Generate category-aware note
            keywords = CATEGORY_KEYWORDS.get(category.name, ["purchase"])
            keyword = random.choice(keywords)
            note = f"{keyword} {fake.word()} {fake.word()}"

        else:
            category = random.choice(user_categories)
            amount = round(random.uniform(5000, 20000), 2)
            note = f"salary {fake.word()}"

        date = datetime.now().date() - timedelta(days=random.randint(0, 365))

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

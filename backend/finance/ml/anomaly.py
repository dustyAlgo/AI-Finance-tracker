import numpy as np
from finance.models import Transaction


def compute_z_score(user, amount):
    transactions = Transaction.objects.filter(user=user, type="EXPENSE")

    amounts = list(transactions.values_list("amount", flat=True))

    if len(amounts) < 5:
        return None

    mean = np.mean(amounts)
    std = np.std(amounts)

    if std == 0:
        return 0

    z_score = (amount - mean) / std
    return float(z_score)

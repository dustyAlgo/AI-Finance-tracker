import os
import pickle
from collections import defaultdict
from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from finance.models import Transaction


class Command(BaseCommand):
    help = "Compute per-user, per-category anomaly statistics (Z-score baselines)"

    def handle(self, *args, **options):
        today = date.today()
        three_months_ago = today - relativedelta(months=3)

        stats = defaultdict(dict)

        users = (
            Transaction.objects
            .values_list("user_id", flat=True)
            .distinct()
        )

        for user_id in users:
            user_txns = Transaction.objects.filter(
                user_id=user_id,
                type=Transaction.TransactionType.EXPENSE
            )

            if not user_txns.exists():
                continue

            categories = (
                user_txns
                .values_list("category_id", flat=True)
                .distinct()
            )

            for category_id in categories:
                recent_txns = user_txns.filter(
                    category_id=category_id,
                    date__gte=three_months_ago
                )

                qs = recent_txns if recent_txns.count() >= 5 else user_txns.filter(
                    category_id=category_id
                )

                amounts = list(qs.values_list("amount", flat=True))

                if len(amounts) < 5:
                    continue  # insufficient data

                mean = float(sum(amounts)) / len(amounts)
                variance = sum((float(x) - mean) ** 2 for x in amounts) / len(amounts)
                std = variance ** 0.5

                if std == 0:
                    continue

                stats[user_id][category_id] = {
                    "mean": float(mean),
                    "std": float(std),
                    "count": len(amounts),
                }

        model_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "ml",
            "models"
        )
        model_dir = os.path.abspath(model_dir)
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, "anomaly_stats.pkl")

        with open(model_path, "wb") as f:
            pickle.dump(dict(stats), f)

        self.stdout.write(
            self.style.SUCCESS(
                f"Anomaly stats computed and saved to {model_path}"
            )
        )

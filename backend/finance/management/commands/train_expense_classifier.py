import os
import pickle

from django.core.management.base import BaseCommand
from finance.models import Transaction
from finance.ml.inference import _clean_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class Command(BaseCommand):
    help = "Train global Naive Bayes model for expense category prediction"

    def handle(self, *args, **options):
        qs = (
            Transaction.objects
            .filter(type=Transaction.TransactionType.EXPENSE)
            .exclude(note__isnull=True)
            .exclude(note__exact="")
            .select_related("category")
        )

        if qs.count() < 10:
            self.stdout.write(
                self.style.WARNING(
                    "Not enough data to train model (need at least 10 samples)."
                )
            )
            return

        texts = []
        labels = []

        for tx in qs:
            cleaned = _clean_text(tx.note)
            if not cleaned:
                continue
            texts.append(cleaned)
            labels.append(tx.category_id)

        if len(set(labels)) < 2:
            self.stdout.write(
                self.style.WARNING(
                    "Need at least 2 categories to train classifier."
                )
            )
            return

        vectorizer = CountVectorizer(
            ngram_range=(1, 2),
            min_df=2
        )
        X = vectorizer.fit_transform(texts)

        clf = MultinomialNB()
        clf.fit(X, labels)

        model = (vectorizer, clf)

        model_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "ml",
            "models"
        )
        model_dir = os.path.abspath(model_dir)
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, "expense_nb.pkl")

        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        self.stdout.write(
            self.style.SUCCESS(
                f"Model trained and saved to {model_path}"
            )
        )

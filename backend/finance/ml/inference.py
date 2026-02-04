import os
import pickle
import re
from django.conf import settings

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "expense_nb.pkl"
)

_model = None


def _clean_text(text: str) -> str:
    """
    Minimal, deterministic text cleaning.
    Keep this stable for train/infer parity.
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_model():
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        return None

    with open(MODEL_PATH, "rb") as f:
        _model = pickle.load(f)

    return _model


def predict_category(note: str):
    model = load_model()
    if model is None:
        return None

    cleaned = _clean_text(note)
    if not cleaned:
        return None

    # model is expected to be a (vectorizer, classifier) tuple
    vectorizer, clf = model

    X = vectorizer.transform([cleaned])
    return clf.predict(X)[0]

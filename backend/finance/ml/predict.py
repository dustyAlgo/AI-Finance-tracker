import joblib
from django.conf import settings
from finance.models import Category

MODEL_PATH = settings.BASE_DIR / "finance" / "ml" / "expense_classifier.pkl"

_model = None
_vectorizer = None


def load_model():
    global _model, _vectorizer
    if _model is None:
        data = joblib.load(MODEL_PATH)
        _model = data["model"]
        _vectorizer = data["vectorizer"]
    return _model, _vectorizer


def predict_category_from_note(user, note):
    if not note:
        return None

    model, vectorizer = load_model()
    X = vectorizer.transform([note])
    predicted_name = model.predict(X)[0]

    return Category.objects.filter(
        user=user,
        name__iexact=predicted_name
    ).first()

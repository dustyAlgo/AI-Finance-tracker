import os
import pickle

ANOMALY_STATS = None


def load_anomaly_stats():
    global ANOMALY_STATS

    model_path = os.path.join(
        os.path.dirname(__file__),
        "models",
        "anomaly_stats.pkl"
    )

    if not os.path.exists(model_path):
        ANOMALY_STATS = {}
        return

    with open(model_path, "rb") as f:
        ANOMALY_STATS = pickle.load(f)


def get_category_stats(user_id, category_id):
    """
    Returns:
        dict: {"mean": float, "std": float, "count": int}
        or None if not available
    """
    if ANOMALY_STATS is None:
        load_anomaly_stats()

    user_data = ANOMALY_STATS.get(user_id)
    if not user_data:
        return None

    return user_data.get(category_id)

def compute_z_score(user_id, category_id, amount):
    """
    Returns z-score or None if stats unavailable.
    """
    stats = get_category_stats(user_id, category_id)

    if not stats:
        return None

    mean = stats.get("mean")
    std = stats.get("std")

    if std is None or std == 0:
        return None

    try:
        return (float(amount) - mean) / std
    except Exception:
        return None

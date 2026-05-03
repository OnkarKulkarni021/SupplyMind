from sqlalchemy.orm import Session
from app.db import models

def score_vendor(vendor):
    return (
        0.5 * vendor.price +
        0.3 * vendor.distance +
        0.2 * vendor.lead_time
    )


def select_best_vendor(db: Session):
    vendors = db.query(models.Vendor).all()

    scored = []
    for v in vendors:
        score = score_vendor(v)
        scored.append((v, score))

    # Lower score is better
    scored.sort(key=lambda x: x[1])

    best_vendor, best_score = scored[0]

    return {
        "vendor": best_vendor,
        "score": best_score
    }
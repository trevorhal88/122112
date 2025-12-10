from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import requests
from bluebook import get_bluebook_price   # your eBay API logic
from ai_autodescribe import detect_rc_model, generate_listing  # your AI helpers

router = APIRouter()

class DetectRequest(BaseModel):
    image_url: str | None = None
    text: str | None = None

@router.post("/api/rc-detect")
async def rc_detect(req: DetectRequest):
    # 1. AI MODEL DETECTION ----------------------
    detection = detect_rc_model(image_url=req.image_url, text=req.text)
    # detection returns: { brand, model, category, confidence }

    # 2. BLUEBOOK PRICING ------------------------
    blue = get_bluebook_price(
        brand=detection["brand"],
        model=detection["model"]
    )
    # blue returns: { average, currency, sample_count, time_window_days }

    # 3. AI LISTING GENERATOR -------------------
    listing = generate_listing(
        brand=detection["brand"],
        model=detection["model"],
        category=detection["category"],
        bluebook=blue,
        user_text=req.text
    )

    return {
        "brand": detection["brand"],
        "model": detection["model"],
        "category": detection["category"],
        "confidence": detection["confidence"],

        "bluebook": {
            "average_price": blue["average"],
            "currency": "USD",
            "sample_count": blue["sample_count"],
            "time_window_days": blue["time_window_days"]
        },

        "listing": {
            "title": listing["title"],
            "description": listing["description"],
            "recommended_price_low": listing["low"],
            "recommended_price_mid": listing["mid"],
            "recommended_price_high": listing["high"],
            "image_url": req.image_url
        }
    }

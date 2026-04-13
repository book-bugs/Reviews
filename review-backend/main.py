import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="BookBugs Review Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ── Models ───────────────────────────────────────────────────────────

class ReviewIn(BaseModel):
    book_code: str = Field(..., min_length=1)
    customer_email: EmailStr
    rating: float = Field(..., ge=1, le=5)
    review_text: Optional[str] = None


class ReviewOut(BaseModel):
    id: str
    book_code: str
    customer_email: str
    rating: float
    review_text: Optional[str]
    verified: bool
    created_at: str


# ── Routes ───────────────────────────────────────────────────────────

@app.get("/")
def health():
    return {"status": "ok", "service": "bookbugs-reviews"}


@app.post("/reviews", status_code=201)
def create_review(review: ReviewIn):
    """Submit a new review. One review per customer per book."""
    data = {
        "book_code": review.book_code.strip(),
        "customer_email": review.customer_email.strip().lower(),
        "rating": review.rating,
        "review_text": review.review_text.strip() if review.review_text else None,
        "verified": False,
    }

    try:
        result = supabase.table("reviews").insert(data).execute()
    except Exception as e:
        error_msg = str(e)
        # Supabase returns 23505 for unique-constraint violations
        if "23505" in error_msg or "duplicate" in error_msg.lower():
            raise HTTPException(
                status_code=409,
                detail="You have already reviewed this book.",
            )
        raise HTTPException(status_code=500, detail="Failed to save review.")

    return {"success": True, "review": result.data[0] if result.data else None}


@app.get("/reviews")
def get_reviews(
    book_code: str = Query(..., min_length=1, description="Product book_code"),
):
    """Return all reviews for a specific book, newest first."""
    result = (
        supabase.table("reviews")
        .select("*")
        .eq("book_code", book_code.strip())
        .order("created_at", desc=True)
        .execute()
    )
    reviews = result.data or []

    # Compute aggregate stats
    total = len(reviews)
    avg_rating = round(sum(r["rating"] for r in reviews) / total, 1) if total else 0

    return {
        "book_code": book_code.strip(),
        "total_reviews": total,
        "average_rating": avg_rating,
        "reviews": reviews,
    }

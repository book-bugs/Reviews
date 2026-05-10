# BookBugs Review System

A lightweight review microservice for **BookBugs** — a Shopify-based book rental store.  
Customers can rate and review books directly on product pages; reviews are stored in Supabase and displayed via a Shopify Liquid widget.

## 🏗️ Architecture

```
┌──────────────────────┐      POST /reviews       ┌──────────────────────┐
│  Shopify Storefront  │ ──────────────────────►   │   FastAPI Backend    │
│  (review-widget.liquid) │  GET /reviews?book_code= │   (main.py)          │
│                      │ ◄──────────────────────   │                      │
└──────────────────────┘                           └──────────┬───────────┘
                                                              │
                                                              ▼
                                                   ┌──────────────────────┐
                                                   │  Supabase (Postgres) │
                                                   │  reviews table       │
                                                   └──────────────────────┘
```

| Layer | Technology | File |
|-------|-----------|------|
| Backend API | Python 3.11 / FastAPI | `main.py` |
| Database | Supabase (PostgreSQL) | `supabase_setup.sql` |
| Frontend Widget | Shopify Liquid + Vanilla JS | `review-widget.liquid` |

## 📁 Project Structure

```
bookbugs review system/
├── main.py                 # FastAPI application — API endpoints
├── review-widget.liquid    # Shopify Liquid section — frontend widget
├── supabase_setup.sql      # Database schema (run once in Supabase SQL Editor)
├── manifest.json           # Project metadata for AI/assistant onboarding
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .python-version         # Python version (3.11.12)
└── readme.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project
- A Shopify store with theme editing access

### 1. Set Up the Database

Open the **Supabase SQL Editor** and run the contents of `supabase_setup.sql`.  
This creates the `reviews` table with:

- UUID primary key
- `book_code` + `customer_email` unique constraint (one review per customer per book)
- Row Level Security with public read/insert policies
- Index on `book_code` for fast lookups

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
ALLOWED_ORIGINS=https://your-store.myshopify.com
```

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Supabase anon (public) key |
| `ALLOWED_ORIGINS` | Comma-separated allowed CORS origins |

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 5. Install the Shopify Widget

1. In your Shopify Admin, go to **Online Store → Themes → Edit Code**
2. Create a new **Section** and paste the contents of `review-widget.liquid`
3. Update the `REVIEW_API_BASE` constant in the `<script>` block to point to your deployed API URL
4. Add the section to your product template

## 📚 API Reference

### Health Check

```
GET /
```

**Response:**
```json
{
  "status": "ok",
  "service": "bookbugs-reviews"
}
```

---

### Submit a Review

```
POST /reviews
Content-Type: application/json
```

**Request Body:**
```json
{
  "book_code": "T210",
  "customer_email": "reader@example.com",
  "rating": 4.5,
  "review_text": "Great book, loved every chapter!"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `book_code` | string | ✅ | Product identifier (from Shopify product tags) |
| `customer_email` | string (email) | ✅ | Must be a valid email |
| `rating` | float | ✅ | Between 1.0 and 5.0 (supports half-stars) |
| `review_text` | string | ❌ | Optional written review |

**Success (201):**
```json
{
  "success": true,
  "review": {
    "id": "uuid",
    "book_code": "T210",
    "customer_email": "reader@example.com",
    "rating": 4.5,
    "review_text": "Great book, loved every chapter!",
    "verified": false,
    "created_at": "2026-05-10T00:00:00+00:00"
  }
}
```

**Duplicate (409):**
```json
{
  "detail": "You have already reviewed this book."
}
```

---

### Get Reviews for a Book

```
GET /reviews?book_code=T210
```

**Response:**
```json
{
  "book_code": "T210",
  "total_reviews": 12,
  "average_rating": 4.3,
  "reviews": [
    {
      "id": "uuid",
      "book_code": "T210",
      "customer_email": "reader@example.com",
      "rating": 4.5,
      "review_text": "Great book!",
      "verified": false,
      "created_at": "2026-05-10T00:00:00+00:00"
    }
  ]
}
```

Reviews are sorted **newest first**.

## 🧩 Frontend Widget Details

The `review-widget.liquid` file is a self-contained Shopify section with HTML, CSS, and JavaScript:

- **Book identification:** Extracts `book_code` from Shopify product tags using the regex `/^[A-Za-z]+\d+$/` (e.g., `T210`, `B7`). Falls back to `product.handle`.
- **Auth check:** If the customer is not logged in (`{{ customer.email }}` is empty), the star input is hidden and replaced with a "Log in" message.
- **Half-star support:** Both the interactive input and display use SVG-based stars with half-star granularity.
- **Modal:** Clicking a star opens a review submission modal with adjustable stars and a textarea.
- **XSS protection:** Review text and usernames are sanitized before rendering.

## 🗄️ Database Schema

```sql
CREATE TABLE reviews (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    book_code       TEXT NOT NULL,
    customer_email  TEXT NOT NULL,
    rating          NUMERIC(2,1) NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text     TEXT,
    verified        BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ DEFAULT now(),
    UNIQUE (book_code, customer_email)
);
```

**Row Level Security** is enabled with public read and insert policies.

## 🚢 Deployment

The API is currently deployed on **Render** at:

```
https://reviews-system.onrender.com
```

### Deploy Your Own Instance

1. Push this repo to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Set the **Build Command** to `pip install -r requirements.txt`
4. Set the **Start Command** to `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add your environment variables (`SUPABASE_URL`, `SUPABASE_KEY`)
6. Deploy

## ⚠️ Known Limitations

- **No server-side auth:** The API accepts any email — authentication relies on the Shopify frontend passing `{{ customer.email }}`. Anyone with the API URL can submit reviews.
- **`verified` is always `false`:** There is no logic yet to cross-reference reviews with actual rental records.
- **Public RLS policies:** Both read and insert are open. Tighten insert policies once authentication is added.

## 📝 License

This project is licensed under the MIT License.

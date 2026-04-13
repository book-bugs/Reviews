-- ============================================================
-- BookBugs Review System — Supabase Table Setup
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor)
-- ============================================================

-- 1. Create the reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    book_code   TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    rating      NUMERIC(2,1) NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    verified    BOOLEAN DEFAULT false,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- 2. Prevent duplicate reviews (one review per customer per book)
ALTER TABLE reviews
    ADD CONSTRAINT unique_review_per_customer_per_book
    UNIQUE (book_code, customer_email);

-- 3. Index on book_code for fast per-product lookups
CREATE INDEX IF NOT EXISTS idx_reviews_book_code
    ON reviews (book_code);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- 5. Allow anyone to read reviews (public storefront)
CREATE POLICY "Public can read reviews"
    ON reviews FOR SELECT
    USING (true);

-- 6. Allow anyone to insert reviews (public submission)
--    (Tighten this later when auth is added)
CREATE POLICY "Public can insert reviews"
    ON reviews FOR INSERT
    WITH CHECK (true);

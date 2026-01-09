#!/bin/bash

# Script to run the scraper tool

echo "🚀 Starting App..."
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run app
echo ""
echo "▶️ Running app..."
echo ""
python sitemap_scraper.py

echo ""
echo "✅ Completed!"

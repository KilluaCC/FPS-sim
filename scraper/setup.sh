#!/bin/bash

echo "🚀 Setting up FPS Benchmark Scraper"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Test the scraper
echo "🧪 Testing scraper setup..."
python test_scraper.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "To use the scraper:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Run the scraper: python run_scraper.py"
    echo "3. Check results in the output/ directory"
    echo ""
    echo "To deactivate: deactivate"
else
    echo ""
    echo "⚠️  Setup completed with some issues. Check the test output above."
fi

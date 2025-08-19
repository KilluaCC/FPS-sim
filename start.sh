#!/bin/bash

echo "🚀 Starting FPS Estimator Application..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing dependencies..."

# Install backend dependencies
npm install

# Install frontend dependencies
cd client
npm install
cd ..

echo "✅ Dependencies installed successfully!"

echo "🌐 Starting development servers..."

# Start both backend and frontend
npm run dev

echo "🎮 Application is starting up!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "📊 Health Check: http://localhost:5000/api/health"

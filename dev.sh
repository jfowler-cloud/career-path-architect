#!/bin/bash

# Career Path Architect - Development Startup Script

echo "🚀 Starting Career Path Architect..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Install it with:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is not installed. Install it with:"
    echo "   npm install -g pnpm"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd apps/backend
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env file. Please configure AWS credentials."
fi
uv sync
echo "✅ Backend ready"
echo ""

# Frontend setup
echo "📦 Setting up frontend..."
cd ../web
if [ ! -f .env.local ]; then
    cp .env.local.example .env.local
fi
cd ../..
pnpm install
echo "✅ Frontend ready"
echo ""

# Start services
echo "🎯 Starting services..."
echo ""
echo "Backend will run on: http://localhost:8000"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Run both services
pnpm dev

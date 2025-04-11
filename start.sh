#!/bin/bash

# Check if required tools are installed
command -v conda >/dev/null 2>&1 || { echo "Conda is required but not found. Please install conda first"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required but not found. Please install Node.js and npm first"; exit 1; }

# Activate conda environment
echo "Activating conda environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate medagent || {
    echo "Conda environment 'medagent' not found, creating..."
    conda create --name medagent python=3.10 -y
    conda activate medagent
}

# Start backend service
echo "Starting backend service..."
cd backend
conda activate medagent
pip install -e . >/dev/null 2>&1
python -m uvicorn app.main:app --reload &
BACKEND_PID=$!

# Start frontend service
echo "Starting frontend service..."
cd ../frontend
npm install >/dev/null 2>&1
npm run dev &
FRONTEND_PID=$!

echo "Services started successfully:"
echo "Backend running at http://127.0.0.1:8000"
echo "Frontend running at http://localhost:3000"
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait

# Cleanup processes
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
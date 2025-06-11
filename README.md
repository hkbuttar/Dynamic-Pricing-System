# Dynamic-Pricing-System

## Overview
Full-stack system for real-time dynamic pricing using AI and business logic.

## Backend Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ml/train_model.py
python run.py
```

## Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Docker Setup
```bash
docker-compose up --build
```

## API
POST `/api/prices` with product data returns adjusted prices.

## Tests
```bash
pytest tests/
```
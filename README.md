# Restaurant Recommendation System

A full-stack web application for restaurant recommendations with filtering and search capabilities.

## Prerequisites
- Python 3.10 or higher
- Node.js 14 or higher
- MongoDB
- Git

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/PhaneeChowdary/RestaurantsRecommendation.git
cd RestaurantsRecommendation
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv db_env

# Activate virtual environment
# On Windows:
db_env\Scripts\activate
# On macOS/Linux:
source db_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your MongoDB configuration
echo "MONGODB_URI=mongodb://localhost:27017
DB_NAME=restaurants_db" > .env
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

## Running the Application

### 1. Start MongoDB
Ensure MongoDB is running on your system:
```bash
# On macOS/Linux
mongod

# On Windows
# Start MongoDB service through Windows Services
```

### 2. Start Backend Server
```bash
# In the backend directory with virtual environment activated
python app.py
```
The backend server will start on http://localhost:5001

### 3. Start Frontend Development Server
```bash
# In the frontend directory
npm start
```
The frontend will start on http://localhost:3000

## Features
- Restaurant search by city
- Price range filtering
- Advanced filters for categories and amenities
- Restaurant details including ratings and reviews
- CRUD operations for restaurants
- Responsive design

## API Endpoints

### GET Endpoints
- `GET /api/restaurants` - Get restaurants with filters
- `GET /api/categories` - Get all available categories

### POST Endpoints
- `POST /api/restaurants` - Create new restaurant

### PUT Endpoints
- `PUT /api/restaurants/<id>` - Update restaurant

### DELETE Endpoints
- `DELETE /api/restaurants/<id>` - Delete restaurant

## Technology Stack
- **Frontend**: React.js, Tailwind CSS
- **Backend**: Flask, Python
- **Database**: MongoDB
- **API**: RESTful API
- **State Management**: React Hooks

# Thank you
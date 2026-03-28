# FoodGenie AI Recommender 🍜

An SLM-powered food recommendation engine inspired by Swiggy and Uber Eats. The system uses semantic embeddings, vector search, contextual ranking, and reinforcement learning to deliver personalized food recommendations.

## 📋 Prerequisites

- **Python 3.8+** (required for backend)
- **Node.js 16+** and **npm** (required for frontend)
- **Git** (for cloning the repository)
- **Virtual Environment** (recommended for Python dependencies)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/foodgenie-ai-recommender.git
cd foodgenie-ai-recommender
```

### 2. Backend Setup

#### Step 1: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

#### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

#### Step 3: Run the Backend Server

```bash
# Make sure virtual environment is activated
cd backend/src
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: **http://localhost:8000**

- API Documentation: http://localhost:8000/docs
- API v1 Endpoint: http://localhost:8000/v1/

### 3. Frontend Setup

#### Step 1: Install Frontend Dependencies

Open a new terminal window and run:

```bash
cd frontend
npm install
```

#### Step 2: Run the Frontend Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173**

## 🎯 Running Both Servers

To run the complete application, you need **both servers running simultaneously**:

### Terminal 1 - Backend:
```bash
# From project root
source venv/bin/activate
cd backend/src
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend:
```bash
# From project root
cd frontend
npm run dev
```

## 📦 Project Structure

```
foodgenie-ai-recommender/
├── backend/                  # FastAPI backend
│   ├── src/
│   │   ├── api/             # API routes and schemas
│   │   │   ├── app.py       # Main FastAPI application
│   │   │   └── v1/          # API v1 routes
│   │   │       └── routes/  # Auth, recommend, feedback routes
│   │   ├── database/        # Database models and CRUD
│   │   ├── ml/              # Machine learning models
│   │   ├── recommender/     # Recommendation engine
│   │   ├── context/         # Context-aware features
│   │   ├── personalization/ # User personalization
│   │   └── reinforcement/   # Feedback loop
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React + TypeScript frontend
│   ├── src/
│   │   ├── api/            # API client functions
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── App.tsx         # Main app component
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
│
├── embeddings/             # Food embedding models
├── data/                   # Datasets and vector databases
├── notebooks/              # Jupyter notebooks
└── README.md              # This file
```

## 🔑 Key Features

- **User Authentication**: Register and login functionality
- **Personalized Recommendations**: AI-powered food suggestions
- **Contextual Ranking**: Time, weather, and preference-based recommendations
- **User Feedback**: Continuous learning from user interactions
- **Vector Search**: Fast similarity search using FAISS
- **Semantic Embeddings**: Advanced food understanding using sentence transformers

## 🛠️ API Endpoints

### Authentication
- `POST /v1/auth/register` - Register a new user
- `POST /v1/auth/login` - Login (form data)
- `POST /v1/auth/login-json` - Login (JSON body)
- `GET /v1/auth/me` - Get current user info

### Recommendations
- `POST /v1/recommend` - Get food recommendations

### Feedback
- `POST /v1/feedback` - Submit user feedback

## 🧪 Testing

### Test Backend Registration
```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

## 🐛 Troubleshooting

### Backend Won't Start

**Error: `ModuleNotFoundError`**
- Make sure you're running from the `backend/src` directory
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Error: `Address already in use`**
```bash
# Find and kill the process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Frontend Won't Start

**Error: `Cannot find module`**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 already in use**
- Vite will automatically use the next available port
- Or specify a different port in `vite.config.ts`

## 📝 Development Notes

- **CORS**: Backend is configured to allow all origins for development
- **Auto-reload**: Both servers support hot-reload during development
- **Database**: Currently using SQLite (located in backend/src)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using FastAPI, React, and Machine Learning**

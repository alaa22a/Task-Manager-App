# Task Management Application

A simple task management app with a Flask backend and React frontend.

## Tech Stack
- **Backend:** Python (Flask), SQLAlchemy, SQLite, Flask-JWT-Extended
- **Frontend:** React, Vite, TailwindCSS, Axios

## Prerequisites
- Python 3.8+
- Node.js 16+ and npm

## Setup Instructions

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
   The backend will start at `http://localhost:5000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will start at `http://localhost:5173` (or similar).

## API Endpoints

### Authentication
- `POST /api/auth/register`: Register a new user (`name`, `email`, `password`)
- `POST /api/auth/login`: Login (`email`, `password`) -> Returns `access_token`

### Tasks (Requires Bearer Token)
- `GET /api/tasks`: List all tasks for current user
- `POST /api/tasks`: Create a new task (`title`, `description` optional)
- `PUT /api/tasks/<id>`: Update a task (`title`, `description`, `status`)
- `DELETE /api/tasks/<id>`: Delete a task

## Assumptions
- SQLite is used for simplicity (no external DB setup required).
- Frontend assumes backend is running on port 5000.

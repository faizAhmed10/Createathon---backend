# Coding Challenge Platform

A web-based coding challenge platform where users can register, log in, attempt coding problems, and track their progress.

## Features
- JWT Authentication (Login & Registration)
- View available coding challenges
- Submit code and get results
- Track user progress

## Tech Stack
- **Frontend:** Next.js, React
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT

## Setup Instructions

### Backend
1. Clone the backend repository:  
   ```sh
   git clone <your-backend-repo-url>
   cd backend
   ```
2. Create a virtual environment and install dependencies:  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Run migrations and start the server:  
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```


## API Endpoints
- `POST /users/register/` - Register a new user
- `POST /users/login/` - Login and get JWT tokens
- `GET /challenges/` - View available coding challenges
- `POST /submit/` - Submit a solution to a challenge


## License
This project is open-source and available under the MIT license.
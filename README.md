
# TripWise – Smart Travel Planner & Budget Optimizer

TripWise is a full-stack web application designed to simplify travel planning. It helps users create personalized trips based on their destination, travel dates, budget, interests, and preferred optimization mode.

The application generates day-wise itineraries and helps users manage their travel budget efficiently.

## Features

- User registration and login.
- Browse popular travel destinations.
- Create and manage trips.
- Select travel dates, number of travelers, and budget.
- Choose interests such as beaches, adventure, nature, culture, food, and shopping.
- Generate personalized day-wise itineraries.
- Rank attractions based on ratings, interests, price, distance, and popularity.
- Optimize activity selection based on the available budget.
- Calculate travel distances and optimize routes.
- View planned activities and estimated expenses.
- Track total budget, planned expenses, and remaining budget.

## Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- HTML5
- CSS3
- Axios
- React Router

### Backend
- Python
- FastAPI
- SQLAlchemy
- REST APIs
- JWT Authentication
- Passlib

### Database
- MySQL

### Tools
- Visual Studio Code
- Git and GitHub
- Postman / Swagger UI

## Algorithms Used

### 1. Attraction Ranking Algorithm
Ranks attractions using multiple factors:
- Rating
- Interest matching
- Price
- Distance
- Popularity

### 2. Budget Optimization – 0/1 Knapsack
Uses Dynamic Programming to select activities within the available budget while maximizing the overall experience.

### 3. Dijkstra's Shortest Path Algorithm
Finds optimized routes between attractions based on travel distance, time, or cost.

### 4. Route Optimization
Uses attraction locations and travel information to arrange activities into an efficient itinerary.

## Project Structure

```text
Smart-Travel-Planner/
│
├── backend/
│   ├── app/
│   │   ├── algorithms/
│   │   │   ├── attraction_ranking.py
│   │   │   ├── budget_optimizer.py
│   │   │   ├── dijkstra.py
│   │   │   ├── graph.py
│   │   │   ├── itinerary_optimizer.py
│   │   │   └── route_optimizer.py
│   │   │
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.10 or above
- Node.js and npm
- MySQL Server
- Git

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL

cd Smart-Travel-Planner
```

### 2. Database Setup

Open MySQL and execute:

```sql
CREATE DATABASE smart_travel_db;
```

### 3. Backend Setup

Open a terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file inside the backend folder.

Add your own database credentials and secret key:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/smart_travel_db

SECRET_KEY=YOUR_SECRET_KEY
```

Replace the placeholder values with your actual local configuration.

**Note:** Never upload your `.env` file or actual credentials to GitHub. Use `.env.example` as a reference.

### 5. Run the Backend

From the backend directory:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

Make sure the frontend API configuration points to the running backend.

## Demo Login Credentials

The following are example credentials for testing.

| Field | Value |
|---|---|
| Name | Demo User |
| Email | user@example.com |
| Password | string |

**Important:** This is an example account, not a pre-created account.

Before logging in, create the account using the registration API:

1. Start the backend.
2. Open `http://127.0.0.1:8000/docs`.
3. Find `POST /auth/register`.
4. Register using:

```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "Demo@12345"
}
```

5. After successful registration, use these credentials to log in.

The frontend signup page may require completion before users can register directly through the website.

## 🔗 Main Backend API Modules

| Module | Purpose |
|---|---|
| Authentication | User registration and login |
| Destinations | Retrieve destination information |
| Attractions | Retrieve attraction information |
| Trips | Create and manage trips |
| Itinerary | Generate and retrieve itineraries |

For complete API details, visit:

`http://127.0.0.1:8000/docs`

## Security Notes

- Database credentials are stored in environment variables.
- JWT signing keys should be kept private.
- `.env` files must not be committed to GitHub.
- `.env.example` should contain placeholders only.
- Development-only endpoints should be removed or protected before deployment.

## Future Improvements

- Complete frontend signup functionality.
- Integrate interactive maps.
- Add weather API integration.
- Improve itinerary recommendations.
- Add more destinations and attractions.
- Deploy the application to a cloud platform.

## License

This project is available for educational and portfolio purposes. No formal open-source license has been added yet.

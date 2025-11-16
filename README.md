🚀 Mini Social Media App

FastAPI + PostgreSQL + JWT Auth + Streamlit Frontend

This project is a complete full-stack mini social media application where users can upload posts (images/videos), view feed, and delete posts, secured through JWT authentication.
The backend is built using FastAPI, data is stored in PostgreSQL, and the UI is created using Streamlit.

🔥 Features
🗂 Backend (FastAPI)

JWT Authentication

Upload API (image/video upload)

Fetch Feed API (view all posts)

Delete API (delete a specific post)

PostgreSQL Database Integration

Async architecture for high performance

Image/Video upload handled via ImageKit

🎨 Frontend (Streamlit)

Clean & simple UI

Upload posts

Display feed

Delete posts

Integrated with FastAPI endpoints

🏛 Tech Stack
Layer	Technology
Backend	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy Async
Auth	JWT (fastapi-users)
Storage	ImageKit
Frontend	Streamlit
Language	Python
📌 API Endpoints
🔐 Authentication
Method	Endpoint	Description
POST	/auth/jwt/login	Login with username/password
POST	/auth/register	Register new user
📤 Post Management
Method	Endpoint	Description
POST	/upload	Upload post (image/video)
GET	/view	View upload feed
DELETE	/posts/{post_id}	Delete post
🧪 Running the Project
1️⃣ Clone the repository
git clone <repo-url>
cd <project-folder>

2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start FastAPI server
uvicorn app:app --reload

5️⃣ Start Streamlit app
streamlit run frontend.py

🗂 Project Structure
├── app.py                 # FastAPI main application
├── users.py               # Auth, JWT, User manager
├── schema.py              # SQLAlchemy models
├── models.py              # Pydantic models
├── database.py            # Async DB connection
├── frontend.py            # Streamlit UI
├── requirements.txt       
└── README.md

🎥 Demo Video

(www.linkedin.com/in/
aryan-dwivedi-41b5a4370
)

⭐ Future Improvements

Like & comment system

Real-time feed using WebSockets

User profiles

Notifications

🤝 Contributing

Feel free to fork the repo and submit PRs!

📬 Contact

If you want help building something similar, feel free to message me! 🚀

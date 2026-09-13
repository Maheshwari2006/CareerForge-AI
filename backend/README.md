# CareerForge AI Backend

The Flask backend is ready in the project root. `app.py` is the application entry point and the backend code is organized into:

- `routes/` - authentication and resume/AI feature routes
- `services/` - ATS, career prediction, JD matching, roadmap, interview, analytics and PDF services
- `nlp/` - resume parsing and skills database
- `database/` - SQLAlchemy models and database setup
- `ml/` - career prediction model and training assets
- `uploads/` - uploaded resume storage

From the project root, run `run_backend.bat` on Windows or use the Python command shown in the main README.

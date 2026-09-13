import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from database.models import db
from database.models.user import User
from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(base_dir, "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access your CareerForge AI dashboard."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return render_template("home.html") if os.path.exists(os.path.join(app.template_folder, "home.html")) else render_template("login.html")

    @app.route("/dashboard")
    def dashboard():
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        from database.models.resume import Resume
        latest_resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.id.desc()).first()
        return render_template("dashboard.html", user=current_user, latest_resume=latest_resume)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("home.html") if os.path.exists(os.path.join(app.template_folder, "home.html")) else ("Page not found", 404)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

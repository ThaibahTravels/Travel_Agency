import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from flask_sqlalchemy import SQLAlchemy
from models import Package, Service, Testimonial, TeamMembers, db
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Fetch environment variables
FLASK_APP = os.getenv('FLASK_APP', 'app.py')  # Default to app.py if not set
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'default_username')  # Default is a fallback value
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'default_password')  # Default is a fallback value
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(24))  # Default to random secret key if not set

# Initialize the Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Secret Key for Flask app
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "db", "travel_agency.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'images')

# Initialize the database with the app
db.init_app(app)  # Link SQLAlchemy with the Flask app

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Define the User model for authentication (must be before login route)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        logging.error(f"Error loading user: {e}")
        return None

# Define custom admin views with authentication
class AuthenticatedAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        try:
            return super().index()
        except Exception as e:
            logging.error(f"Error accessing admin index: {e}")
            flash("Error accessing the admin dashboard. Please try again later.", "danger")
            return redirect(url_for('index'))

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class FileUploadModelView(AuthenticatedModelView):
    """Base class for models with file upload fields.""" 
    form_overrides = {
        'image': FileUploadField
    }
    form_args = {
        'image': {
            'base_path': app.config['UPLOAD_FOLDER'],
            'allow_overwrite': True
        }
    }
    column_formatters = {
        'image': lambda v, c, m, p: f'<img src="/static/images/{m.image}" width="100">' if m.image else ''
    }

# Initialize Flask Admin with authentication
admin = Admin(app, name='Travel Agency Dashboard', template_mode='bootstrap3', index_view=AuthenticatedAdminIndexView())
admin.add_view(FileUploadModelView(Package, db.session))
admin.add_view(FileUploadModelView(Service, db.session))
admin.add_view(FileUploadModelView(Testimonial, db.session))
admin.add_view(FileUploadModelView(TeamMembers, db.session))

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        app.logger.debug(f"Attempting to login with username: {username}")

        try:
            # Validate against environment variables
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                app.logger.debug("Admin login successful.")

                # Create user session (using Flask-Login)
                user = User.query.filter_by(username=username).first()
                if user:
                    login_user(user)
                else:
                    user = User(username=username)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)

                flash('Logged in successfully!', 'success')
                return redirect(url_for('admin.index'))
            else:
                flash('Invalid username or password.', 'danger')
                app.logger.warning("Invalid credentials entered.")
        except Exception as e:
            logging.error(f"Error during login: {e}")
            flash("An error occurred during login. Please try again.", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('Logged out successfully.', 'success')
    except Exception as e:
        logging.error(f"Error during logout: {e}")
        flash("Error occurred while logging out. Please try again.", "danger")
    return redirect(url_for('login'))

@app.context_processor
def inject_testimonials():
    try:
        testimonials = Testimonial.query.all()
        return {'testimonials': testimonials}
    except Exception as e:
        logging.error(f"Error fetching testimonials: {e}")
        return {'testimonials': []}

# Public routes
@app.route('/')
def index():
    try:
        packages = Package.query.all()
        services = Service.query.all()
        return render_template('index.html', packages=packages, services=services)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        flash("Error fetching data. Please try again later.", 'danger')
        return render_template('index.html')

@app.route('/packages')
def packages():
    try:
        national_packages = Package.query.filter_by(type='national').all()
        international_packages = Package.query.filter_by(type='international').all()
        return render_template("packages.html", national_packages=national_packages, international_packages=international_packages)
    except Exception as e:
        logging.error(f"Error fetching packages: {e}")
        flash("Error fetching packages. Please try again later.", 'danger')
        return render_template("packages.html")

@app.route('/services')
def services():
    try:
        services = Service.query.all()
        return render_template('services.html', services=services)
    except Exception as e:
        logging.error(f"Error fetching services: {e}")
        flash("Error fetching services. Please try again later.", 'danger')
        return render_template('services.html')

@app.route('/about')
def about():
    try:
        heads = TeamMembers.query.filter_by(is_head=True).all()
        members = TeamMembers.query.filter_by(is_head=False).all()
        return render_template("about.html", heads=heads, members=members)
    except Exception as e:
        logging.error(f"Error fetching team members: {e}")
        flash("Error fetching team members. Please try again later.", 'danger')
        return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

# Error handling for 404 and 500
@app.errorhandler(404)
def not_found_error(error):
    logging.error(f"404 Error: {error}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"500 Error: {e}")
    return render_template('500.html'), 500

# Ensure tables are created and create an admin user if not already present
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            if not User.query.filter_by(username=ADMIN_USERNAME).first():
                admin_user = User(username=ADMIN_USERNAME)
                admin_user.set_password(ADMIN_PASSWORD)
                db.session.add(admin_user)
                db.session.commit()
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
    app.run(debug=False)  # Set to False in production
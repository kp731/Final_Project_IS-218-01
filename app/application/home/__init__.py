"""Initialize Flask app."""
from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

mysql = MySQL(cursorclass=DictCursor)

def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from app import routes
        from app.routes import home_bp
        # Register Blueprints
        app.register_blueprint(app.home_bp)

        return app
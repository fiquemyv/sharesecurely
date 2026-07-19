from flask import Flask
import dotenv

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = dotenv.get_key(".env", "SECRET_KEY")

    from app.routes import main

    app.register_blueprint(main)

    return app
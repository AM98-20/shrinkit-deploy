from flask import Flask

from .routes import app

def create_app():
    main = Flask(__name__, static_folder='./build/static', template_folder="./build" )
    main.config['SECRET_KEY'] = 'xHdkwI98_hJkD'#W

    main.register_blueprint(app)

    return main
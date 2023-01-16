from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    main = Flask(__name__)

    main.config['SECRET_KEY'] = 'Tarik-Vinci-Diana-Alexandra'
    main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(main)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(main)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    #blueprint for expenses
    from expenses import expenses as expenses_blueprint
    main.register_blueprint(expenses_blueprint)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    main.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    main.register_blueprint(main_blueprint)


    with main.app_context():
        db.create_all()

    return main

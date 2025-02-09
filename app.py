from flask import Flask
from flask_login import LoginManager
from models.model import db, User

app = None
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = '23f3003203quizmaster'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.init_app(app)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

# with app.app_context():
#     db.drop_all()
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from controllers.user_controller import *
from controllers.admin_controller import *
from controllers.login_signup import *
from controllers.error_handler import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def db_init(app):
    db.init_app(app)

    # Creates the tables if the db doesnt already exist
    with app.app_context():
        db.create_all()
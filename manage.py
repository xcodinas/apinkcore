from sqlalchemy.exc import IntegrityError

from flask_script import Manager

from app import db, app
from app.models import User

manager = Manager(app)


@manager.command
def init_db():
    db.create_all()


@manager.command
def create_admin(
        email="admin@admin.com", username="admin", password="admin"):
    user = User(
        username=username,
        full_name=username,
        password=User.generate_hash(password),
        email=email,
        )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        print('That email is already in use.')
        return
    print('Admin user created correctly. \nEmail: %s' % email)


if __name__ == '__main__':
    manager.run()

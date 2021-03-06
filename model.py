"""Models for trail information."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///mapping', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

class Trail(db.Model):
    """A trail."""

    __tablename__ = 'trails'

    trail_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    desc = db.Column(db.Text)
    long = db.Column(db.Float, nullable = False)
    lat = db.Column(db.Float, nullable = False)
    gps = db.Column(db.String)
    length = db.Column(db.Float, nullable = False)
    ascent = db.Column(db.Integer)
    descent = db.Column(db.Integer)
    difficulty = db.Column(db.String)
    location = db.Column(db.String)
    url = db.Column(db.String)
    img = db.Column(db.String)

    # favorites = a list of Favorite objects

    def __repr__(self):
        return f'<Trail trail_id={self.trail_id} name={self.name}>'

class Suggestion(db.Model):
    """A suggested trail from a user."""

    __tablename__ = 'suggestions'
    
    suggestion_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String, nullable = False)
    desc = db.Column(db.Text)
    long = db.Column(db.Float, nullable = False)
    lat = db.Column(db.Float, nullable = False)
    gps = db.Column(db.String)
    length = db.Column(db.Float, nullable = False)
    ascent = db.Column(db.Integer)
    descent = db.Column(db.Integer)
    difficulty = db.Column(db.String)
    location = db.Column(db.String)
    url = db.Column(db.String)

    user = db.relationship('User', backref = 'suggestions')

    def __repr__(self):
        return f'<Suggestion suggestion_id={self.suggestion_id} name={self.name}>'


class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True,
                        )
    email = db.Column(db.String, unique = True, nullable = False)
    # password = db.Column(db.String, nullable = False)
    moderator = db.Column(db.Boolean, nullable = False)
    
    # favorites = a list of Favorite objects
    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'

class Favorite(db.Model):
    """A favorited trail."""

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.trail_id'), nullable = False)

    trail = db.relationship('Trail', backref = 'favorites')
    user = db.relationship('User', backref = 'favorites')

    def __repr__(self):
        return f'<Favorite favorite_id={self.favorite_id} id={self.id} trail_id={self.trail_id}>'


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)


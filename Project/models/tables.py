from app import db
from werkzeug.security import generate_password_hash


# Modelos
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    queries = db.relationship("HistoricalQuery", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

class HistoricalQuery(db.Model):
    __tablename__ = 'historical_queries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates="queries")
    results = db.relationship("HistoricalResult", back_populates="query")

class HistoricalResult(db.Model):
    __tablename__ = 'historical_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.DECIMAL(10, 2), nullable=False)
    reviews_num = db.Column(db.Integer, nullable=False)
    night_cost = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey('historical_queries.id'))

    query = db.relationship("HistoricalQuery", back_populates="results")
    screenshots = db.relationship("Screenshot", back_populates="result")

class Screenshot(db.Model):
    __tablename__ = 'screenshots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.LargeBinary, nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('historical_results.id'))

    result = db.relationship("HistoricalResult", back_populates="screenshots")


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import time

app = Flask(__name__)

# Get database URL from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple user model for demonstration
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Wait for MySQL to be ready
def wait_for_db():
    for _ in range(10):
        try:
            with app.app_context():
                db.session.execute("SELECT 1")
            print("✅ Database connected!")
            return
        except Exception as e:
            print("⏳ Waiting for database...")
            time.sleep(3)
    print("❌ Database connection failed.")
    exit(1)

@app.route('/')
def home():
    return jsonify({"message": "Auth microservice running!"})

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

if __name__ == '__main__':
    wait_for_db()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

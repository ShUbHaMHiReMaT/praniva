from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///praniva.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class PetProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    weight_kg = db.Column(db.Float)
    blood_group = db.Column(db.String(50))
    activity_level = db.Column(db.String(50))
    last_vaccination = db.Column(db.String(20))
    is_neutered = db.Column(db.String(20))
    allergies = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    owner_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    city = db.Column(db.String(50))
    preferred_vet = db.Column(db.String(100))
    discovery_source = db.Column(db.String(50))
    waitlist_id = db.Column(db.String(20), unique=True)

with app.app_context():
    db.drop_all()   # ← drops the old broken table
    db.create_all() # ← creates fresh table with all columns including dob

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    try:
        new_pet = PetProfile(
            pet_name=data.get('pet_name'),
            species=data.get('species'),
            breed=data.get('breed'),
            dob=data.get('dob'),
            weight_kg=data.get('weight_kg'),
            blood_group=data.get('blood_group'),
            activity_level=data.get('activity_level'),
            last_vaccination=data.get('last_vaccination'),
            is_neutered=data.get('is_neutered'),
            allergies=data.get('allergies'),
            medical_history=data.get('medical_history'),
            owner_name=data.get('owner_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            city=data.get('city'),
            preferred_vet=data.get('preferred_vet'),
            discovery_source=data.get('discovery_source'),
            waitlist_id=data.get('waitlist_id')
        )
        db.session.add(new_pet)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
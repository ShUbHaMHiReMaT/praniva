from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ── DATABASE CONFIG ──────────────────────────────────────────
# On Render: uses PostgreSQL via DATABASE_URL environment variable
# Locally: falls back to SQLite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///praniva.db')

# Render gives a postgres:// URL but SQLAlchemy needs postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── DATABASE MODEL ───────────────────────────────────────────
class PetProfile(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    pet_name         = db.Column(db.String(100), nullable=False)
    species          = db.Column(db.String(50),  nullable=False)
    breed            = db.Column(db.String(100))
    dob              = db.Column(db.String(20))
    weight_kg        = db.Column(db.Float)
    blood_group      = db.Column(db.String(50))
    activity_level   = db.Column(db.String(50))
    last_vaccination = db.Column(db.String(20))
    is_neutered      = db.Column(db.String(20))
    allergies        = db.Column(db.Text)
    medical_history  = db.Column(db.Text)
    owner_name       = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(100), nullable=False)
    phone            = db.Column(db.String(20))
    city             = db.Column(db.String(50))
    preferred_vet    = db.Column(db.String(100))
    discovery_source = db.Column(db.String(50))
    waitlist_id      = db.Column(db.String(20), unique=True)

with app.app_context():
    db.create_all()  # safe — only creates tables if they don't exist

# ── ROUTES ───────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    try:
        new_pet = PetProfile(
            pet_name         = data.get('pet_name'),
            species          = data.get('species'),
            breed            = data.get('breed'),
            dob              = data.get('dob'),
            weight_kg        = data.get('weight_kg'),
            blood_group      = data.get('blood_group'),
            activity_level   = data.get('activity_level'),
            last_vaccination = data.get('last_vaccination'),
            is_neutered      = data.get('is_neutered'),
            allergies        = data.get('allergies'),
            medical_history  = data.get('medical_history'),
            owner_name       = data.get('owner_name'),
            email            = data.get('email'),
            phone            = data.get('phone'),
            city             = data.get('city'),
            preferred_vet    = data.get('preferred_vet'),
            discovery_source = data.get('discovery_source'),
            waitlist_id      = data.get('waitlist_id')
        )
        db.session.add(new_pet)
        db.session.commit()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ── VIEW ALL SUBMISSIONS ─────────────────────────────────────
# Visit: https://your-app.onrender.com/admin/submissions?key=praniva2025
@app.route('/admin/submissions')
def view_submissions():
    secret = request.args.get('key')
    if secret != os.environ.get('ADMIN_KEY', 'praniva2025'):
        return jsonify({"error": "Unauthorized"}), 401
    pets = PetProfile.query.order_by(PetProfile.id.desc()).all()
    result = []
    for p in pets:
        result.append({
            "id":               p.id,
            "waitlist_id":      p.waitlist_id,
            "pet_name":         p.pet_name,
            "species":          p.species,
            "breed":            p.breed,
            "dob":              p.dob,
            "weight_kg":        p.weight_kg,
            "blood_group":      p.blood_group,
            "activity_level":   p.activity_level,
            "last_vaccination": p.last_vaccination,
            "is_neutered":      p.is_neutered,
            "allergies":        p.allergies,
            "medical_history":  p.medical_history,
            "owner_name":       p.owner_name,
            "email":            p.email,
            "phone":            p.phone,
            "city":             p.city,
            "preferred_vet":    p.preferred_vet,
            "discovery_source": p.discovery_source,
        })
    return jsonify({"total": len(result), "submissions": result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
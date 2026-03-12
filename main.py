from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
# IMPORTANT: This allows Render to send data to your laptop
CORS(app, resources={r"/*": {"origins": "*"}}) 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="praniva_db"
    )

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """INSERT INTO pet_profiles 
                 (pet_name, species, breed, dob, weight_kg, blood_group, 
                  activity_level, last_vaccination, is_neutered, allergies, 
                  medical_history, owner_name, email, phone, city, 
                  preferred_vet, discovery_source, waitlist_id) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            data.get('pet_name'), data.get('species'), data.get('breed'),
            data.get('dob') or None, data.get('weight_kg'), data.get('blood_group'),
            data.get('activity_level'), data.get('last_vaccination') or None,
            data.get('is_neutered'), data.get('allergies'), data.get('medical_history'),
            data.get('owner_name'), data.get('email'), data.get('phone'),
            data.get('city'), data.get('preferred_vet'), data.get('discovery_source'),
            data.get('waitlist_id')
        )
        
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it visible to your local network and Render
    app.run(host='0.0.0.0', port=5000, debug=True)
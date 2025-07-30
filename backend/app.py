from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import db

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ict_support.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import models after db initialization
from models.support_ticket import SupportTicket
from models.building import Building
from models.department import Department
from models.user import User
from models.floor import Floor

# Register blueprints
from routes.tickets import tickets_bp
from routes.ai import ai_bp
from routes.general import general_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.health import health_bp

app.register_blueprint(tickets_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(general_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(health_bp, url_prefix='/api')

# Serve frontend files
@app.route('/')
def serve_index():
    """Serve the main index.html"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/admin')
def serve_admin():
    """Serve the admin.html"""
    return send_from_directory('../frontend', 'admin.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from frontend directory"""
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
        print("✅ Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
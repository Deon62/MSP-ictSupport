from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import db

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ict_support.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import models after db initialization
from models.support_ticket import SupportTicket
from models.building import Building
from models.department import Department

# Register blueprints
from routes.tickets import tickets_bp
from routes.ai import ai_bp
from routes.general import general_bp

app.register_blueprint(tickets_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(general_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Initialize sample data
        from utils.sample_data import initialize_sample_data
        initialize_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
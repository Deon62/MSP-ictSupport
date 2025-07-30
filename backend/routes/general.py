from flask import Blueprint, request, jsonify
from datetime import datetime
from models.building import Building
from models.department import Department

general_bp = Blueprint('general', __name__)

@general_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'ICT Support System',
        'version': '1.0.0'
    })

@general_bp.route('/buildings', methods=['GET'])
def get_buildings():
    """Get all buildings"""
    try:
        buildings = Building.query.all()
        return jsonify({
            'buildings': [building.to_dict() for building in buildings]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@general_bp.route('/departments', methods=['GET'])
def get_departments():
    """Get all departments"""
    try:
        departments = Department.query.all()
        return jsonify({
            'departments': [dept.to_dict() for dept in departments]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@general_bp.route('/departments/<building>', methods=['GET'])
def get_departments_by_building(building):
    """Get departments by building"""
    try:
        departments = Department.query.filter_by(building=building).all()
        return jsonify({
            'departments': [dept.to_dict() for dept in departments],
            'building': building
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
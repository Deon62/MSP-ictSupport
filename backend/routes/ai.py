from flask import Blueprint, request, jsonify
from services.ai_agent import AIAgent
from datetime import datetime

ai_bp = Blueprint('ai', __name__)
ai_agent = AIAgent()

@ai_bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    """AI agent chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get AI response
        response = ai_agent.get_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'suggested_actions': ai_agent.get_quick_fixes(user_message.lower())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/quick-fixes/<issue_type>', methods=['GET'])
def get_quick_fixes(issue_type):
    """Get quick fixes for common issues"""
    try:
        fixes = ai_agent.get_quick_fixes(issue_type)
        return jsonify({
            'issue_type': issue_type,
            'quick_fixes': fixes
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
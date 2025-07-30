from flask import Blueprint, jsonify
from services.ai_agent import AIAgent
import os
import time
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health/ai', methods=['GET'])
def ai_health_check():
    """Health check for AI assistant"""
    try:
        # Check if API key is configured
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'status': 'failed',
                'model': 'gemini-1.5-flash',
                'latency_ms': 0,
                'error': 'GEMINI_API_KEY not configured',
                'timestamp': datetime.now().isoformat()
            }), 200
        
        # Initialize AI agent
        ai_agent = AIAgent()
        
        # Perform lightweight test
        start_time = time.time()
        test_prompt = "Hello, this is a health check. Please respond with 'OK'."
        
        try:
            response = ai_agent.model.generate_content(test_prompt)
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Check if response is valid
            if response and response.text:
                return jsonify({
                    'status': 'ok',
                    'model': 'gemini-1.5-flash',
                    'latency_ms': latency_ms,
                    'timestamp': datetime.now().isoformat()
                }), 200
            else:
                return jsonify({
                    'status': 'failed',
                    'model': 'gemini-1.5-flash',
                    'latency_ms': latency_ms,
                    'error': 'Empty response from model',
                    'timestamp': datetime.now().isoformat()
                }), 200
                
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            
            # Provide user-friendly error messages
            if 'PermissionDenied' in error_msg or 'InvalidArgument' in error_msg:
                user_error = 'API key configuration issue. Please check your Gemini API key and account settings.'
            elif 'ResourceExhausted' in error_msg:
                user_error = 'Rate limit exceeded. Please try again later.'
            elif 'safety' in error_msg.lower():
                user_error = 'Request blocked by safety filters. Please try rephrasing.'
            else:
                user_error = 'AI service temporarily unavailable. Please try again.'
            
            return jsonify({
                'status': 'failed',
                'model': 'gemini-1.5-flash',
                'latency_ms': latency_ms,
                'error': user_error,
                'technical_error': error_msg,
                'timestamp': datetime.now().isoformat()
            }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'model': 'gemini-1.5-flash',
            'latency_ms': 0,
            'error': f'Health check failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 200 
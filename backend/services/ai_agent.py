import os
import google.generativeai as genai
import logging
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not configured - AI will use fallback responses")
            self.model = None
            self.api_configured = False
        else:
            try:
                genai.configure(api_key=api_key)
                # Use gemini-1.5-flash for faster responses
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.api_configured = True
                logger.info("AI Agent initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI Agent: {str(e)}")
                self.model = None
                self.api_configured = False
        
        # Simplified ICT Support prompt template
        self.ict_prompt = """You are GPO, the ICT Support Assistant for Teleposta GPO (Ministry of Public Service).

Personality: Warm, helpful, and professional. Keep responses concise and practical.

Scope: WiFi, printers, projectors, computers, software, network, email, general IT support.

Guidelines:
- Provide clear, numbered steps
- If physical access needed, guide to create a support ticket
- Keep responses under 150 words
- Use simple language, avoid technical jargon
- Be encouraging and solution-focused

Example responses:
Q: "WiFi keeps dropping"
A: "Let's fix your WiFi connection:
1. Toggle WiFi off/on and reconnect to 'Teleposta_Guest'
2. Forget the network, then reconnect with credentials
3. Restart your device
4. Move closer to the access point if signal is weak
5. If still having issues, I can help you create a support ticket."

Q: "What's your name?"
A: "Hi! I'm GPO, your friendly ICT helper. How can I assist you today?"""
        
        # Fallback responses for common issues when API is unavailable
        self.fallback_responses = {
            'wifi': "For WiFi issues, try these steps:\n1. Restart your device\n2. Forget and reconnect to 'Teleposta_Guest'\n3. Move closer to the access point\n4. Contact ICT team if issues persist",
            'printer': "For printer problems:\n1. Check if printer is powered on\n2. Ensure paper is loaded\n3. Restart the printer\n4. Contact ICT team for driver issues",
            'projector': "For projector setup:\n1. Connect VGA/HDMI cable to laptop\n2. Press Windows + P to extend display\n3. Check projector power and input source\n4. Contact ICT team for assistance",
            'computer': "For computer issues:\n1. Restart the computer\n2. Check all cables are connected\n3. Try a different power outlet\n4. Contact ICT team for hardware issues",
            'email': "For email problems:\n1. Check your internet connection\n2. Clear browser cache and cookies\n3. Try a different browser\n4. Contact ICT team for account issues",
            'software': "For software issues:\n1. Restart the application\n2. Check for updates\n3. Restart your computer\n4. Contact ICT team for installation help"
        }
    
    def get_fallback_response(self, user_message):
        """Get a fallback response when API is unavailable"""
        message_lower = user_message.lower()
        
        # Check for keywords to provide relevant fallback
        if any(word in message_lower for word in ['wifi', 'internet', 'connection', 'network']):
            return self.fallback_responses['wifi']
        elif any(word in message_lower for word in ['printer', 'print', 'printing']):
            return self.fallback_responses['printer']
        elif any(word in message_lower for word in ['projector', 'display', 'screen', 'presentation']):
            return self.fallback_responses['projector']
        elif any(word in message_lower for word in ['computer', 'pc', 'laptop', 'desktop']):
            return self.fallback_responses['computer']
        elif any(word in message_lower for word in ['email', 'mail', 'outlook']):
            return self.fallback_responses['email']
        elif any(word in message_lower for word in ['software', 'program', 'application', 'app']):
            return self.fallback_responses['software']
        elif any(word in message_lower for word in ['name', 'who are you', 'hello', 'hi']):
            return "Hi! I'm GPO, your friendly ICT helper. How can I assist you today?"
        else:
            return "I'm here to help with your ICT issues! Please provide more details about your problem, or contact the ICT team directly for immediate assistance."
    
    def clean_response(self, text):
        """Clean response text by removing markdown formatting and extra whitespace"""
        if not text:
            return text
        
        # Remove markdown formattin
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove *italic*
        text = re.sub(r'`(.*?)`', r'\1', text)        # Remove `code`
        text = re.sub(r'#+\s*', '', text)             # Remove headers
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Remove links
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove extra line breaks
        text = text.strip()
        
        return text
    
    def get_response(self, user_message):
        """Get AI response for user message - always returns a response"""
        if not self.api_configured:
            # Use fallback response when API is not configured
            logger.info("Using fallback response - API not configured")
            return self.get_fallback_response(user_message)
        
        try:
            # Create a concise prompt for faster responses
            prompt = f"{self.ict_prompt}\n\nUser: {user_message}\n\nGPO:"
            
            logger.info(f"Generating response for user message: {user_message[:50]}...")
            
            # Set generation config for faster responses
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 300,  # Limit response length
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                # Clean the response to remove markdown formatting
                cleaned_response = self.clean_response(response.text)
                logger.info("AI response generated successfully")
                return cleaned_response
            else:
                logger.warning("Empty response from AI model, using fallback")
                return self.get_fallback_response(user_message)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"AI response error: {error_msg}")
            
            # Always return a helpful response instead of error message
            logger.info("Using fallback response due to API error")
            return self.get_fallback_response(user_message)
    
    def get_quick_fixes(self, issue_type):
        """Get quick fixes for common issues"""
        quick_fixes = {
            'wifi': [
                "1. Check if WiFi is enabled on your device",
                "2. Try connecting to 'Teleposta_Guest' network",
                "3. Restart your device",
                "4. Contact ICT team if issues persist"
            ],
            'printer': [
                "1. Check if printer is powered on",
                "2. Ensure paper is loaded",
                "3. Check for paper jams",
                "4. Restart the printer",
                "5. Contact ICT team for driver issues"
            ],
            'projector': [
                "1. Connect VGA/HDMI cable to laptop",
                "2. Press Windows + P to extend display",
                "3. Check projector power and input source",
                "4. Contact ICT team for setup assistance"
            ],
            'computer': [
                "1. Restart the computer",
                "2. Check all cables are connected",
                "3. Try a different power outlet",
                "4. Contact ICT team for hardware issues"
            ]
        }
        
        return quick_fixes.get(issue_type.lower(), ["Please contact the ICT team for assistance."])

import os
import re
import logging
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        # Initialize API keys
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        # Initialize clients
        self.deepseek_client = None
        self.openai_client = None
        self.gemini_model = None
        
        # ICT Support prompt
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

        # Fallback responses
        self.fallback_responses = {
            'wifi': "For WiFi issues, try these steps:\n1. Restart your device\n2. Forget and reconnect to 'Teleposta_Guest'\n3. Move closer to the access point\n4. Contact ICT team if issues persist",
            'printer': "For printer problems:\n1. Check if printer is powered on\n2. Ensure paper is loaded\n3. Restart the printer\n4. Contact ICT team for driver issues",
            'projector': "For projector setup:\n1. Connect VGA/HDMI cable to laptop\n2. Press Windows + P to extend display\n3. Check projector power and input source\n4. Contact ICT team for assistance",
            'computer': "For computer issues:\n1. Restart the computer\n2. Check all cables are connected\n3. Try a different power outlet\n4. Contact ICT team for hardware issues",
            'email': "For email problems:\n1. Check your internet connection\n2. Clear browser cache and cookies\n3. Try a different browser\n4. Contact ICT team for account issues",
            'software': "For software issues:\n1. Restart the application\n2. Check for updates\n3. Restart your computer\n4. Contact ICT team for installation help"
        }
        
        # Initialize providers
        self._init_providers()
    
    def _init_providers(self):
        """Initialize AI providers in order of preference"""
        
        # 1. DeepSeek (Primary)
        if self.deepseek_key:
            try:
                from openai import OpenAI
                self.deepseek_client = OpenAI(
                    api_key=self.deepseek_key,
                    base_url="https://api.deepseek.com/v1"
                )
                logger.info("DeepSeek client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize DeepSeek: {e}")
                self.deepseek_client = None
        
        # 2. OpenAI (Secondary - using free model)
        if self.openai_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.openai_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI: {e}")
                self.openai_client = None
        
        # 3. Gemini (Tertiary)
        if self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.gemini_model = None
        
        # Log available providers
        available_providers = []
        if self.deepseek_client: available_providers.append("DeepSeek")
        if self.openai_client: available_providers.append("OpenAI")
        if self.gemini_model: available_providers.append("Gemini")
        
        if available_providers:
            logger.info(f"Available AI providers: {', '.join(available_providers)}")
        else:
            logger.warning("No AI providers available - will use fallback responses")
    
    def clean_response(self, text):
        """Clean response text by removing markdown formatting"""
        if not text:
            return text
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove *italic*
        text = re.sub(r'`(.*?)`', r'\1', text)        # Remove `code`
        text = re.sub(r'#+\s*', '', text)             # Remove headers
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Remove links
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def get_fallback_response(self, user_message):
        """Get a fallback response based on keywords"""
        message_lower = user_message.lower()
        
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
    
    def _try_deepseek(self, user_message):
        """Try DeepSeek API"""
        if not self.deepseek_client:
            return None
        
        try:
            start_time = time.time()
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.ict_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=300,
                timeout=15
            )
            
            if time.time() - start_time > 15:
                logger.warning("DeepSeek request timed out")
                return None
            
            content = response.choices[0].message.content
            if content:
                logger.info("DeepSeek response successful")
                return self.clean_response(content)
            
        except Exception as e:
            logger.warning(f"DeepSeek failed: {str(e)}")
        
        return None
    
    def _try_openai(self, user_message):
        """Try OpenAI API (using free model)"""
        if not self.openai_client:
            return None
        
        try:
            start_time = time.time()
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Free model
                messages=[
                    {"role": "system", "content": self.ict_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=300,
                timeout=15
            )
            
            if time.time() - start_time > 15:
                logger.warning("OpenAI request timed out")
                return None
            
            content = response.choices[0].message.content
            if content:
                logger.info("OpenAI response successful")
                return self.clean_response(content)
            
        except Exception as e:
            logger.warning(f"OpenAI failed: {str(e)}")
        
        return None
    
    def _try_gemini(self, user_message):
        """Try Gemini API"""
        if not self.gemini_model:
            return None
        
        try:
            start_time = time.time()
            response = self.gemini_model.generate_content(
                f"{self.ict_prompt}\n\nUser: {user_message}\n\nGPO:",
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 300,
                }
            )
            
            if time.time() - start_time > 15:
                logger.warning("Gemini request timed out")
                return None
            
            if response and response.text:
                logger.info("Gemini response successful")
                return self.clean_response(response.text)
            
        except Exception as e:
            logger.warning(f"Gemini failed: {str(e)}")
        
        return None
    
    def get_response(self, user_message):
        """Get AI response with fallback chain"""
        logger.info(f"Processing user message: {user_message[:50]}...")
        
        # Try DeepSeek first (Primary)
        response = self._try_deepseek(user_message)
        if response:
            return response
        
        # Try OpenAI second (Secondary)
        response = self._try_openai(user_message)
        if response:
            return response
        
        # Try Gemini third (Tertiary)
        response = self._try_gemini(user_message)
        if response:
            return response
        
        # Use fallback response
        logger.info("All AI providers failed, using fallback response")
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

import os
import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not configured - AI features will be limited")
            self.model = None
            self.api_configured = False
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.api_configured = True
                logger.info("AI Agent initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI Agent: {str(e)}")
                self.model = None
                self.api_configured = False
        
        # Simple ICT Support prompt template
        self.ict_prompt ="""
            You are called GPO, the friendly ICT Support Assistant for **Teleposta GPO (Ministry of Public Service).

            Personality & tone:
            - Warm, polite, and empathetic. Add light humor when appropriate. Be helpful, never sarcastic.


            How to respond:
            - Thank the user for reaching out and restate their goal in one short sentence.
            - Provide clear, numbered steps with concise actions. Bold the most important actions.
            - Ask one clarifying question if needed before giving a long set of steps.
            - Keep responses practical and brief; avoid long paragraphs.
            - Use at most one emoji per response (optional) to keep things professional and friendly.

            Scope you cover:
            - WiFi connectivity problems
            - Printer setup & troubleshooting
            - Projector/boardroom setup
            - Computer hardware issues
            - Software installation & updates
            - Network connectivity issues
            - Email configuration
            - General IT support queries

            Ticketing & escalation:
            - If physical assistance or privileged access is required, politely guide the user to create a support ticket.
            - Ask for: Issue, Location/Room, Device, Extension/Phone, Best time to visit**.
            - Offer to fill the ticket for them if they provide details.

            Safety & good practice:
            - Encourage saving work before restarts/updates.
            - Avoid sharing sensitive info; remind users not to post passwords.

            Examples:

            Q: "What's your name?"
            A: "hey there I'm GPO your friendly ICT helper. How can I make your tech behave today? 😄"

            Q: "My WiFi keeps dropping."
            A: "Thanks for reaching out. Let's stabilize your connection:
            1) Toggle WiFi off/on and reconnect to 'Teleposta_Guest'.
            2) Forget the network, then reconnect and re‑enter credentials.
            3) Restart the device to refresh the adapter.
            4) If near a wall or far from the AP, move closer and test again.
            5) Still flaky? I can open a ticket—share your location and extension."

            Be consistently kind, concise, and action‑oriented. Sign off as GPO when it helps clarity.
            """
    
    def get_response(self, user_message):
        """Get AI response for user message with robust error handling"""
        if not self.api_configured:
            return "I'm currently in offline mode. Please contact the ICT team directly for immediate assistance, or try again later when the AI service is available."
        
        try:
            # Create a simple prompt for ICT support
            prompt = f"{self.ict_prompt}\n\nUser Question: {user_message}\n\nPlease provide a helpful response:"
            
            logger.info(f"Generating response for user message: {user_message[:50]}...")
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                logger.info("AI response generated successfully")
                return response.text
            else:
                logger.warning("Empty response from AI model")
                return "I apologize, but I received an empty response. Please try rephrasing your question."
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"AI response error: {error_msg}")
            
            # Provide user-friendly error messages based on error type
            if 'PermissionDenied' in error_msg or 'InvalidArgument' in error_msg:
                user_message = "I'm experiencing a configuration issue with the AI service. Please contact the ICT team for immediate assistance."
            elif 'ResourceExhausted' in error_msg:
                user_message = "I've hit the rate limit for AI requests. Please try again in a few minutes or contact the ICT team directly."
            elif 'safety' in error_msg.lower():
                user_message = "I couldn't complete your request due to safety filters. Please try rephrasing your question or contact the ICT team."
            else:
                user_message = "I encountered an error while processing your request. Please contact the ICT team directly for immediate assistance."
            
            return user_message
    
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
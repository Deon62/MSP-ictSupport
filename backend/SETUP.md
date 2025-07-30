# ICT Support System - Backend Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
1. Copy the example environment file:
   ```bash
   cp env_example.txt .env
   ```

2. Edit `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   ```

   **To get a free Gemini API key:**
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key and paste it in your `.env` file

### 3. Run the Backend
```bash
python run.py
```

The server will start on `http://localhost:5000`

### 4. Test the API
```bash
python test_app.py
```

## What's Included

### ✅ Core Features
- **Support Ticket System**: Create and manage IT support tickets
- **Multi-Building Support**: 4 buildings including the 27-floor Teleposta Tower
- **Department Management**: 8 departments across different buildings
- **AI Assistant**: Simple AI chat for common IT issues
- **RESTful API**: Complete API for frontend integration

### 🏢 Sample Data
- **Buildings**: Teleposta Tower (27 floors), Annex A (8 floors), Annex B (12 floors), Regional Office (5 floors)
- **Departments**: ICT, HR, Finance, Customer Service, Operations, Legal, Marketing, R&D
- **Sample Tickets**: 5 realistic support tickets for testing

### 🤖 AI Features
- **Simple AI Chat**: Uses Gemini 1.5 Flash (free tier)
- **ICT-Specific Responses**: Tailored for IT support queries
- **Common Issue Help**: WiFi, printer, projector, computer issues

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/tickets` | POST | Create support ticket |
| `/api/tickets` | GET | Get all tickets |
| `/api/tickets/<id>` | GET | Get specific ticket |
| `/api/tickets/<id>/status` | PUT | Update ticket status |
| `/api/ai/chat` | POST | AI assistant chat |
| `/api/buildings` | GET | Get all buildings |
| `/api/departments` | GET | Get all departments |

## Example Usage

### Create a Support Ticket
```bash
curl -X POST http://localhost:5000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "building": "Teleposta Tower",
    "floor": "15",
    "department": "ICT Department",
    "issue_type": "WiFi Connectivity",
    "description": "WiFi is very slow on the 15th floor",
    "contact_person": "John Doe",
    "phone_number": "+254-700-123-456",
    "priority": "high"
  }'
```

### Chat with AI Assistant
```bash
curl -X POST http://localhost:5000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I connect to the WiFi?"
  }'
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run: `pip install -r requirements.txt`

2. **"GEMINI_API_KEY not found"**
   - Make sure you have a `.env` file with your API key

3. **Database errors**
   - Delete `ict_support.db` and restart the server

4. **Port already in use**
   - Change the port in `run.py` or kill the existing process

### Getting Help
- Check the logs in the terminal
- Run `python test_app.py` to test all endpoints
- Make sure all files are in the correct directories

## Next Steps

After the backend is running:
1. ✅ Backend API is ready
2. 🔄 Create the frontend (HTML/CSS/JavaScript)
3. 🔄 Connect frontend to backend API
4. 🔄 Test the complete system

The backend is designed to be simple but functional. It provides all the essential features needed for the ICT support system without unnecessary complexity. 
# ICT Support System - Backend

This is the backend API for the Teleposta GPO Ministry of Public Service ICT Support System.

## Features

- **Support Ticket Management**: Create, view, and update support tickets
- **Building & Department Management**: Manage buildings and departments
- **AI Assistant**: Gemini-powered AI agent for common IT support queries
- **Web Search Integration**: LangChain integration for real-time information
- **RESTful API**: Complete REST API for frontend integration

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `env_example.txt` to `.env` and configure your environment variables:
```bash
cp env_example.txt .env
```

Edit `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your-actual-gemini-api-key
```

### 3. Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Health check endpoint

### Support Tickets
- `POST /api/tickets` - Create a new support ticket
- `GET /api/tickets` - Get all tickets (with optional filters)
- `GET /api/tickets/<id>` - Get specific ticket
- `PUT /api/tickets/<id>/status` - Update ticket status

### AI Assistant
- `POST /api/ai/chat` - Chat with AI assistant

### Buildings & Departments
- `GET /api/buildings` - Get all buildings
- `GET /api/departments` - Get all departments

## Database Schema

### Support Tickets
- Building, floor, department
- Issue type and description
- Contact information
- Priority and status tracking
- Timestamps for creation and updates

### Buildings
- Name, address, number of floors
- Contact person and phone number

### Departments
- Name, building, floor
- Contact person and phone number

## Sample Data

The system comes with sample data including:
- 4 buildings (including the 27-floor Teleposta Tower)
- 8 departments across different buildings
- 5 sample support tickets

## AI Assistant Features

The AI assistant can help with:
- WiFi connectivity issues
- Printer troubleshooting
- Projector setup
- Computer hardware problems
- Software installation
- General IT support queries

## Development

### Project Structure
```
backend/
├── app.py              # Main Flask application
├── models/             # Database models
│   ├── support_ticket.py
│   ├── building.py
│   └── department.py
├── services/           # Business logic
│   └── ai_agent.py
├── utils/              # Utilities
│   └── sample_data.py
└── requirements.txt    # Python dependencies
```

### Adding New Features
1. Create new models in `models/` directory
2. Add routes in `app.py`
3. Create services in `services/` directory
4. Update sample data in `utils/sample_data.py` 
# ICT Support Ticketing System - Backend

A comprehensive ticketing system with AI-powered support assistant and role-based admin management.

## Features

### Core Features
- **Support Ticket Management**: Create, track, and manage support tickets
- **AI Assistant**: Powered by Google Gemini for intelligent support responses
- **Role-Based Access Control**: ADMIN, AGENT, and VIEWER roles
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Admin Dashboard**: Comprehensive admin interface for system management

### Admin Features
- **User Management**: Create, edit, and manage team members
- **Department Management**: CRUD operations for departments
- **Building & Floor Management**: Manage buildings and their floors
- **Ticket Management**: View all tickets, filter, sort, and update status
- **AI Health Monitoring**: Real-time AI assistant health checks

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ict/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

   The server will start on `http://localhost:5000`

### Default Admin Account

The system creates a default admin account during initialization:

- **Username**: `ict_support`
- **Password**: `Ict@support`
- **Role**: ADMIN
- **Must Change Password**: Yes (enforced on first login)

⚠️ **Important**: Change the default password immediately after first login!

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user info

### Admin Endpoints (Require ADMIN role)
- `GET /api/admin/tickets` - Get all tickets with filtering
- `PATCH /api/admin/tickets/{id}/status` - Update ticket status
- `GET/POST/PATCH/DELETE /api/admin/departments` - Department management
- `GET/POST/PATCH/DELETE /api/admin/buildings` - Building management
- `GET/POST/PATCH/DELETE /api/admin/floors` - Floor management
- `GET/POST/PATCH/DELETE /api/admin/users` - User management

### Health & Monitoring
- `GET /api/health/ai` - AI assistant health check

### Public Endpoints
- `POST /api/tickets` - Create support ticket
- `GET /api/tickets` - Get tickets (filtered)
- `GET /api/tickets/{id}` - Get specific ticket
- `PUT /api/tickets/{id}/status` - Update ticket status
- `GET /api/dashboard` - Dashboard statistics

## Database Schema

### Users Table
```sql
users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'VIEWER',
    department_id INTEGER REFERENCES departments(id),
    active BOOLEAN DEFAULT TRUE,
    must_change_password BOOLEAN DEFAULT FALSE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
)
```

### Support Tickets Table
```sql
support_tickets (
    id INTEGER PRIMARY KEY,
    building_id INTEGER NOT NULL REFERENCES buildings(id),
    floor_id INTEGER NOT NULL REFERENCES floors(id),
    department_id INTEGER NOT NULL REFERENCES departments(id),
    issue_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    contact_person VARCHAR(100),
    phone_number VARCHAR(20),
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    assigned_to_id INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    notes TEXT
)
```

## Role-Based Access Control

### ADMIN Role
- Full system access
- User management
- Department/Building/Floor management
- All ticket operations
- System configuration

### AGENT Role
- View and update tickets
- View departments
- Limited admin functions

### VIEWER Role
- View tickets only
- No modification permissions

## Security Features

- **Password Hashing**: bcrypt with 12 rounds
- **Rate Limiting**: 5 login attempts per minute
- **Account Locking**: 5-minute lock after failed attempts
- **JWT Tokens**: Secure token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Validation**: Comprehensive request validation

## AI Assistant

The system includes an AI-powered support assistant using Google's Gemini model:

### Features
- **Intelligent Responses**: Context-aware support responses
- **Quick Fixes**: Pre-defined solutions for common issues
- **Health Monitoring**: Real-time status checking
- **Error Handling**: Graceful error handling with user-friendly messages

### Health Check
The `/api/health/ai` endpoint provides:
- API key validation
- Model availability check
- Response latency monitoring
- Detailed error reporting

## Seed Data

The system automatically creates:

### Buildings
- Uchumi House
- KICC
- Harambee House
- Teleposta

### Floors
- Numbers 1-27
- Background Floor
- Ground Floor

### Departments
- Human Resource
- Internal Audit
- Guidance and Counselling
- Accounts
- Library
- Treasury

## Testing

Run the test suite to verify functionality:

```bash
python test_admin.py
```

This will test:
- Authentication
- Admin endpoints
- AI health check
- Password management

## Development

### Database Migrations
For schema changes, use the migration script:

```bash
python -c "from utils.migrate_data import migrate_ticket_data; migrate_ticket_data()"
```

### Adding New Features
1. Create models in `models/` directory
2. Add routes in `routes/` directory
3. Update `app.py` to register new blueprints
4. Add tests in `test_admin.py`

## Troubleshooting

### Common Issues

1. **AI Assistant Not Working**
   - Check `GEMINI_API_KEY` in `.env`
   - Verify API key is valid and has quota
   - Check `/api/health/ai` endpoint

2. **Authentication Issues**
   - Ensure JWT_SECRET_KEY is set
   - Check token expiration
   - Verify user account is active

3. **Database Issues**
   - Delete `instance/ict_support.db` to reset
   - Run `python app.py` to recreate database
   - Check database file permissions

### Logs
The application logs to console. Check for:
- Authentication attempts
- AI request errors
- Database connection issues

## Production Deployment

### Environment Variables
```bash
GEMINI_API_KEY=your_production_api_key
JWT_SECRET_KEY=your_secure_jwt_secret
FLASK_ENV=production
```

### Security Checklist
- [ ] Change default admin password
- [ ] Set secure JWT secret key
- [ ] Configure HTTPS
- [ ] Set up proper CORS origins
- [ ] Enable rate limiting
- [ ] Configure logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 
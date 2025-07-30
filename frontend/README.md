# ICT Support System - Frontend

A beautiful, modern web interface for the Teleposta GPO ICT Support System.

## Features

### 🎨 Modern Design
- **Clean & Professional**: Modern gradient design with glassmorphism effects
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **User-Friendly**: Intuitive navigation and smooth animations
- **Brand Integration**: Features your Teleposta GPO logo

### 📊 Dashboard
- **Real-time Statistics**: Live ticket counts and status overview
- **Quick Actions**: Easy access to common tasks
- **Recent Tickets**: View latest support requests
- **Visual Cards**: Beautiful stat cards with icons

### 🎫 Ticket Management
- **Create Tickets**: Easy form with building/department selection
- **View All Tickets**: Complete ticket listing with filters
- **Search & Filter**: Find tickets by status, building, or keywords
- **Status Tracking**: Real-time status updates with notifications

### 🤖 AI Assistant
- **Smart Chat**: Interactive AI assistant for common issues
- **Quick Questions**: Pre-defined questions for instant help
- **ICT-Specific**: Tailored responses for IT support queries
- **Real-time**: Instant responses from Gemini AI

### 📱 Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Touch-Friendly**: Easy navigation on touch devices
- **Fast Loading**: Optimized performance

## Setup Instructions

### 1. Prerequisites
Make sure the backend server is running:
```bash
cd backend
python run.py
```

### 2. Open the Frontend
Simply open `index.html` in your web browser:
- Double-click the `index.html` file
- Or drag and drop it into your browser
- Or use a local server (recommended)

### 3. Using a Local Server (Recommended)
For the best experience, serve the frontend using a local server:

**Using Python:**
```bash
cd frontend
python -m http.server 8000
```
Then open: http://localhost:8000

**Using Node.js:**
```bash
cd frontend
npx serve .
```

## File Structure

```
frontend/
├── index.html          # Main HTML file
├── styles.css          # Modern CSS styles
├── script.js           # JavaScript functionality
├── assets/
│   └── image.png       # Your Teleposta GPO logo
└── README.md           # This file
```

## Features in Detail

### Dashboard
- **Statistics Cards**: Total, pending, in-progress, and resolved tickets
- **Quick Actions**: Buttons to create tickets, ask AI, and refresh
- **Recent Tickets**: Latest support requests with status indicators

### Ticket Creation
- **Smart Forms**: Auto-populated building and department dropdowns
- **Validation**: Required field validation with helpful messages
- **Priority Selection**: Low, medium, high, urgent options
- **Contact Information**: Optional contact person and phone number

### Ticket Viewing
- **Advanced Filtering**: Filter by status, building, and search terms
- **Status Indicators**: Color-coded status badges
- **Notification System**: Real-time status change notifications
- **Responsive Cards**: Beautiful ticket cards with all details

### AI Assistant
- **Interactive Chat**: Real-time conversation with AI
- **Quick Questions**: Pre-defined buttons for common issues
- **Contextual Responses**: AI understands ICT-specific queries
- **Visual Design**: User and AI messages with distinct styling

## Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## API Integration

The frontend connects to the backend API at `http://localhost:5000/api` and includes:

- **Health Checks**: Automatic API connectivity verification
- **Error Handling**: Graceful error messages and retry logic
- **Real-time Updates**: Live data refresh and notifications
- **CORS Support**: Cross-origin requests handled properly

## Customization

### Colors
The design uses a beautiful gradient theme that can be easily customized in `styles.css`:
- Primary gradient: `#667eea` to `#764ba2`
- Success colors: Green gradients
- Warning colors: Orange/red gradients
- Error colors: Red gradients

### Logo
Replace `assets/image.png` with your own logo. The system automatically scales and displays it in the navigation.

### Styling
All styles are in `styles.css` and use modern CSS features:
- CSS Grid and Flexbox for layouts
- CSS Custom Properties for theming
- Smooth animations and transitions
- Glassmorphism effects

## Troubleshooting

### Common Issues

1. **API Connection Error**
   - Make sure the backend server is running on port 5000
   - Check that CORS is enabled in the backend
   - Verify the API_BASE_URL in script.js

2. **Logo Not Displaying**
   - Ensure the logo file is in the assets folder
   - Check the file path in index.html
   - Verify the image format is supported

3. **Styling Issues**
   - Clear browser cache
   - Check that styles.css is in the same directory as index.html
   - Verify all CSS is loading properly

4. **JavaScript Errors**
   - Open browser developer tools (F12)
   - Check the Console tab for error messages
   - Ensure all required files are present

## Performance

The frontend is optimized for:
- **Fast Loading**: Minimal dependencies, optimized assets
- **Smooth Animations**: CSS-based animations for better performance
- **Efficient API Calls**: Smart caching and request management
- **Mobile Performance**: Optimized for mobile devices

## Security

- **No Sensitive Data**: All data is handled by the backend
- **CORS Protection**: Proper cross-origin request handling
- **Input Validation**: Client-side and server-side validation
- **XSS Protection**: Proper content escaping and sanitization

## Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the backend server is running
3. Test API endpoints directly
4. Check network connectivity

The frontend is designed to be simple, beautiful, and functional - perfect for the ICT team and users at Teleposta GPO! 
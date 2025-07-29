# Agent Conversation System - Frontend

A clean, modern web interface for interacting with the multi-agent conversation system. Built with HTML, CSS, and JavaScript, featuring a sleek black, white, and grey design.

## 🎨 Design Features

- **Clean Minimalist Design**: Black, white, and grey color scheme
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Modern Typography**: Inter font family for excellent readability
- **Smooth Animations**: Subtle transitions and loading states
- **Professional UI**: Workplace-appropriate interface design

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML page
├── styles.css          # CSS styling and animations
├── script.js           # JavaScript functionality
├── server.py           # Flask backend server
└── README.md           # This file
```

## 🚀 Quick Start

### Option 1: Simple HTML Server (Demo Mode)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start a simple HTTP server:**
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Or with Python 2
   python -m SimpleHTTPServer 8000
   ```

3. **Open your browser:**
   ```
   http://localhost:8000
   ```

### Option 2: Full Backend Integration

1. **Install Flask (if not already installed):**
   ```bash
   pip install flask
   ```

2. **Start the Flask server:**
   ```bash
   cd frontend
   python server.py
   ```

3. **Open your browser:**
   ```
   http://localhost:5000
   ```

## 🎯 Features

### Agent Configuration
- **Customizable Roles**: Set different roles for Employee1 and Employee2
- **Expertise Areas**: Define specific expertise for each agent
- **Real-time Updates**: Changes apply immediately

### Conversation Management
- **Topic Setting**: Define the main conversation topic
- **Context Provision**: Add optional context for better understanding
- **Exchange Control**: Set maximum exchanges (3-6)
- **Progress Tracking**: Visual progress bar and exchange counter

### Demo Scenarios
- **Project Timeline Discussion**: Project Manager vs Developer
- **Feature Design Discussion**: Product Manager vs UX Designer
- **Marketing Campaign Strategy**: Marketing Manager vs Data Analyst
- **HR System Implementation**: HR Manager vs IT Manager

### Conversation Display
- **Real-time Messages**: See conversation as it happens
- **Agent Identification**: Color-coded messages for each agent
- **Timestamps**: Track when each message was sent
- **Broker Analysis**: See the broker's insights and guidance

### System Status
- **API Connection**: Monitor connection to the agent system
- **Agent Status**: Check if agents are ready
- **Conversation Status**: Track current conversation state

## 🎨 UI Components

### Header Section
- **Gradient Background**: Black to dark grey gradient
- **Title**: "Agent Conversation System"
- **Subtitle**: System description

### Configuration Panel
- **Grid Layout**: Responsive grid for agent configuration
- **Form Controls**: Input fields for roles and expertise
- **Validation**: Real-time input validation

### Conversation Setup
- **Topic Input**: Main conversation topic
- **Context Textarea**: Optional additional context
- **Exchange Selector**: Choose maximum exchanges
- **Start Button**: Begin conversation

### Conversation Display
- **Progress Bar**: Visual progress indicator
- **Message Container**: Scrollable conversation area
- **Message Styling**: Different styles for each agent
- **Control Buttons**: Next, Run Full, Reset

### Demo Section
- **Scenario Buttons**: Quick access to predefined scenarios
- **Active States**: Visual feedback for selected scenarios
- **Responsive Layout**: Adapts to screen size

### Status Section
- **Status Grid**: System status indicators
- **Color Coding**: Green (success), Red (error), Yellow (warning)
- **Real-time Updates**: Status changes reflected immediately

## 🔧 Technical Details

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript (ES6+)**: Modern JavaScript with async/await
- **Responsive Design**: Mobile-first approach

### Backend Integration
- **Flask**: Python web framework
- **RESTful API**: JSON-based communication
- **Error Handling**: Comprehensive error management
- **Status Monitoring**: Real-time system status

### Browser Compatibility
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Mobile Support**: iOS Safari, Chrome Mobile
- **Progressive Enhancement**: Works without JavaScript (basic functionality)

## 🎮 Usage Guide

### Starting a Conversation

1. **Configure Agents:**
   - Set Employee1 role and expertise
   - Set Employee2 role and expertise

2. **Set Conversation Parameters:**
   - Enter the main topic
   - Add optional context
   - Choose maximum exchanges

3. **Start Conversation:**
   - Click "Start Conversation"
   - Watch initial perspectives appear

### Using Demo Scenarios

1. **Select a Scenario:**
   - Click any demo button
   - Configuration auto-fills
   - Topic and context are set

2. **Customize (Optional):**
   - Modify roles or expertise
   - Adjust topic or context
   - Change exchange count

3. **Start Conversation:**
   - Use "Start Conversation" button
   - Or try "Run Full Conversation"

### Conversation Controls

- **Next Exchange**: Process one exchange at a time
- **Run Full Conversation**: Complete all exchanges automatically
- **Reset**: Clear conversation and start over

## 🎨 Design System

### Color Palette
- **Primary Black**: #000000
- **Secondary Grey**: #1a1a1a
- **Light Grey**: #6c757d
- **Background Grey**: #f8f9fa
- **Border Grey**: #e9ecef
- **Text Dark**: #212529
- **Text Medium**: #495057

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Sizes**: 0.8rem to 2.5rem
- **Line Height**: 1.6

### Spacing
- **Container Padding**: 20px
- **Section Margin**: 30px
- **Element Gap**: 10px-20px
- **Border Radius**: 8px-12px

### Animations
- **Transition Duration**: 0.2s-0.3s
- **Hover Effects**: Transform and shadow
- **Loading Spinner**: 1s rotation
- **Message Slide-in**: 0.3s ease-out

## 🔧 Customization

### Styling Customization
Edit `styles.css` to modify:
- Color scheme
- Typography
- Spacing
- Animations
- Layout

### Functionality Customization
Edit `script.js` to modify:
- Demo scenarios
- API endpoints
- Error handling
- UI behavior

### Backend Customization
Edit `server.py` to modify:
- API routes
- Agent integration
- Error responses
- Server configuration

## 🚀 Deployment

### Static Hosting
The frontend can be deployed to any static hosting service:
- **GitHub Pages**
- **Netlify**
- **Vercel**
- **AWS S3**

### Full Stack Deployment
For full backend integration:
- **Heroku**
- **DigitalOcean**
- **AWS EC2**
- **Google Cloud Platform**

## 🐛 Troubleshooting

### Common Issues

1. **Agents Not Available**
   - Check if agent system is running
   - Verify XAI API token is set
   - Check Python environment

2. **Frontend Not Loading**
   - Verify server is running
   - Check browser console for errors
   - Ensure all files are present

3. **API Connection Issues**
   - Check network connectivity
   - Verify API endpoints
   - Check CORS settings

### Debug Mode
Enable debug mode in `server.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📱 Mobile Experience

The frontend is fully responsive and optimized for mobile devices:
- **Touch-friendly buttons**
- **Responsive grid layouts**
- **Optimized typography**
- **Mobile-first design**

## 🔒 Security Considerations

- **Input Validation**: All user inputs are validated
- **XSS Prevention**: Content is properly escaped
- **CORS Configuration**: Configured for local development
- **Error Handling**: Sensitive information is not exposed

## 🎯 Future Enhancements

Potential improvements for the frontend:
- **Real-time WebSocket communication**
- **Conversation history and saving**
- **Export functionality (PDF, JSON)**
- **Advanced analytics and insights**
- **Multi-language support**
- **Dark/light theme toggle**
- **Accessibility improvements**

## 📄 License

This frontend is part of the Agent Conversation System and follows the same license terms as the main project. 
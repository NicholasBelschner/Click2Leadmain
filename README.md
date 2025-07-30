# Click2Lead - Dynamic Agent Conversation System

A sophisticated multi-agent conversation platform that allows users to create unlimited specialized agents for dynamic team discussions and problem-solving.

## 🚀 **Quick Start**

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd Click2Lead
   ```

2. **Set up environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your XAI API token
   ```

4. **Start the system**
   ```bash
   cd frontend
   python server.py
   ```

5. **Access the interface**
   - Open http://localhost:5001 in your browser
   - Start creating dynamic agents and conversations!

## 🎯 **Key Features**

- **🤖 Dynamic Agent Creation**: Create any number of specialized agents on-demand
- **💬 Multi-Agent Conversations**: Coordinate discussions between unlimited agents
- **🎨 Real-time Visualization**: See agents and conversations in real-time
- **🛡️ Guardian NLP System**: Intelligent text classification and processing
- **⚡ Responsive Interface**: Beautiful, minimal UI optimized for productivity

## 📁 **Project Structure**

```
Click2Lead/
├── agents/           # Dynamic agent system
│   ├── dynamic_agent_manager.py
│   ├── dynamic_broker.py
│   ├── dynamic_orchestrator.py
│   └── README.md
├── frontend/         # Web interface
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   ├── server.py
│   └── README.md
├── gaurdian/         # NLP classification system
│   ├── nlp_classifier.py
│   ├── database_integration.py
│   ├── train_model.py
│   └── README.md
├── docs/            # 📚 Comprehensive documentation
│   ├── README.md
│   ├── DEVELOPMENT_REPORTS.md
│   ├── session-001-dynamic-agent-system.md
│   └── templates/
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## 📚 **Documentation**

### **Development Reports** 📋
- **[Development Reports Index](docs/DEVELOPMENT_REPORTS.md)** - Overview of all development sessions
- **[Session 1 Report](docs/session-001-dynamic-agent-system.md)** - Complete dynamic agent system implementation
- **[Documentation Guide](docs/README.md)** - How to use and contribute to documentation

### **System Documentation**
- **[Agent System](agents/README.md)** - Dynamic agent creation and management
- **[Frontend Interface](frontend/README.md)** - Web interface and user experience
- **[Guardian NLP](gaurdian/README.md)** - Natural language processing system

## 🎯 **Example Usage**

### **Creating a Fitness Team**
```
"I would like to create a team of agents working for me to make sure my human body is running at its optimal performance. I would like 3 employees working for me. I would like one to be in charge of my workouts and then another to be in charge of my nutrition I am eating/drinking, and then another to make sure that the workouts align with my nutrients and my nutrients aligns with my workouts please"
```

**System Response:**
- ✅ Creates 3 specialized agents: Workout Specialist, Nutrition Specialist, Fitness Coordinator
- ✅ Assigns appropriate expertise and personalities
- ✅ Displays agents in real-time UI
- ✅ Enables multi-agent conversations

### **Business Team Creation**
```
"Create 4 agents: Product Manager, Developer, Designer, and Marketing Manager for a new product launch"
```

## 🔧 **Technology Stack**

- **Backend**: Python, Flask, XAI API
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI/ML**: TensorFlow, NLP Classification
- **Architecture**: Dynamic Agent System, Broker Pattern

## 🚀 **Current Status**

- ✅ **Dynamic Agent System**: Fully operational
- ✅ **Real-time UI**: Complete with agent visualization
- ✅ **Multi-agent Conversations**: Working with unlimited agents
- ✅ **Error Handling**: Robust fallback systems
- ✅ **Documentation**: Comprehensive development tracking

**Ready for production use and further development!**

## 🤝 **Contributing**

1. Read the [development reports](docs/DEVELOPMENT_REPORTS.md) to understand the project history
2. Check the [documentation guide](docs/README.md) for contribution standards
3. Use the [session report template](docs/templates/session-report-template.md) for new features
4. Follow the established patterns in existing code

## 📞 **Support**

- **Documentation**: [docs/README.md](docs/README.md)
- **Development History**: [docs/DEVELOPMENT_REPORTS.md](docs/DEVELOPMENT_REPORTS.md)
- **System Status**: Check individual component README files

---

*Last Updated: July 30, 2025*  
*System Status: Production Ready* 🚀 
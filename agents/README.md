# Multi-Agent Conversation System

A sophisticated multi-agent system featuring a broker agent that coordinates efficient conversations between Employee1 and Employee2, ensuring productive communication within 3-6 exchanges maximum.

## 🎯 Overview

This system uses three AI agents powered by the XAI API to simulate realistic workplace conversations:

- **Broker Agent**: The communication coordinator that ensures efficient, goal-oriented conversations
- **Employee1 Agent**: First participant with customizable role and expertise
- **Employee2 Agent**: Second participant with customizable role and expertise

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Employee1     │    │     Broker      │    │   Employee2     │
│                 │◄──►│                 │◄──►│                 │
│ • Role-based    │    │ • Coordinates    │    │ • Role-based    │
│ • XAI-powered   │    │ • Analyzes       │    │ • XAI-powered   │
│ • Context-aware │    │ • Guides         │    │ • Context-aware │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 File Structure

```
agents/
├── README.md              # This documentation
├── broker.py              # Broker agent - conversation coordinator
├── employee1.py           # Employee1 agent - first participant
├── employee2.py           # Employee2 agent - second participant
├── agent_orchestrator.py  # Main orchestrator - coordinates all agents
├── demo_agents.py         # Demo script with multiple scenarios
└── conversation_logs/     # Generated conversation logs
```

## 🚀 Quick Start

### 1. Setup Environment

Ensure your `.env` file contains your XAI API token:
```bash
XAI_API_TOKEN=xai-your-token-here
```

### 2. Run Demo

```bash
cd agents
python demo_agents.py
```

### 3. Basic Usage

```python
from agent_orchestrator import AgentOrchestrator

# Create orchestrator with custom roles
orchestrator = AgentOrchestrator(
    employee1_role="Project Manager",
    employee1_expertise="Project planning and coordination",
    employee2_role="Senior Developer",
    employee2_expertise="Technical implementation"
)

# Conduct a conversation
result = orchestrator.conduct_full_conversation(
    topic="Project timeline adjustment",
    context="Need to discuss timeline changes for the authentication module",
    max_exchanges=4
)
```

## 🤖 Agent Details

### Broker Agent (`broker.py`)

**Role**: Communication coordinator and facilitator

**Key Features**:
- Manages conversation flow and progress
- Analyzes exchanges using XAI API
- Ensures conversations stay focused and productive
- Tracks conversation goals and completion
- Provides guidance and intervention when needed

**Methods**:
- `start_conversation()` - Initialize new conversation
- `coordinate_exchange()` - Analyze and guide exchanges
- `get_conversation_summary()` - Get conversation status
- `reset_conversation()` - Reset conversation state

### Employee1 Agent (`employee1.py`)

**Role**: First conversation participant

**Key Features**:
- Customizable role and expertise
- XAI-powered intelligent responses
- Context-aware communication
- Professional communication style
- Goal-oriented responses

**Methods**:
- `generate_response()` - Respond to Employee2
- `provide_initial_perspective()` - Share initial thoughts
- `update_context()` - Update conversation context
- `get_agent_info()` - Get agent information

### Employee2 Agent (`employee2.py`)

**Role**: Second conversation participant

**Key Features**:
- Customizable role and expertise
- XAI-powered intelligent responses
- Technical but accessible communication
- Solution-focused approach
- Collaborative mindset

**Methods**:
- `generate_response()` - Respond to Employee1
- `provide_initial_perspective()` - Share initial thoughts
- `update_context()` - Update conversation context
- `get_agent_info()` - Get agent information

### Agent Orchestrator (`agent_orchestrator.py`)

**Role**: Main coordinator for all agents

**Key Features**:
- Manages complete conversation flow
- Coordinates all three agents
- Provides conversation logging
- Handles conversation state management
- Generates comprehensive reports

**Methods**:
- `start_conversation()` - Begin new conversation
- `conduct_exchange()` - Conduct single exchange
- `conduct_full_conversation()` - Run complete conversation
- `save_conversation_log()` - Save conversation to file
- `get_conversation_status()` - Get current status

## 🎬 Demo Scenarios

The demo script includes four realistic workplace scenarios:

1. **Project Timeline Discussion**: Project Manager vs Developer
2. **Feature Design Discussion**: Product Manager vs UX Designer
3. **Marketing Campaign Strategy**: Marketing Manager vs Data Analyst
4. **HR System Implementation**: HR Manager vs IT Manager

## 📊 Conversation Flow

```
1. Start Conversation
   ├── Broker initializes conversation
   ├── Employee1 provides initial perspective
   └── Employee2 provides initial perspective

2. Exchange Loop (3-6 times max)
   ├── Employee1 generates response
   ├── Employee2 generates response
   ├── Broker analyzes exchange
   └── Broker provides guidance

3. Conclusion
   ├── Broker determines completion
   ├── Generate final summary
   └── Save conversation log
```

## ⚙️ Configuration

### Customizing Agent Roles

```python
orchestrator = AgentOrchestrator(
    employee1_role="Sales Manager",
    employee1_expertise="Sales strategy and customer relations",
    employee2_role="Marketing Specialist",
    employee2_expertise="Digital marketing and campaign optimization"
)
```

### Adjusting Conversation Parameters

```python
result = orchestrator.conduct_full_conversation(
    topic="Your topic here",
    context="Additional context",
    max_exchanges=5  # Customize max exchanges
)
```

## 📈 Performance Features

- **Efficient Communication**: Conversations complete within 3-6 exchanges
- **Goal-Oriented**: Each conversation has specific objectives
- **Context-Aware**: Agents remember conversation history
- **Intelligent Analysis**: Broker provides real-time guidance
- **Comprehensive Logging**: All conversations are saved and analyzed

## 🔧 API Integration

The system uses the XAI API for:
- Intelligent response generation
- Conversation analysis
- Context understanding
- Goal tracking

## 📝 Output Formats

### Conversation Logs

All conversations are saved as JSON files containing:
- Complete conversation history
- Agent responses and analysis
- Progress tracking
- Final summaries
- Metadata and timestamps

### Real-time Output

During conversations, you'll see:
- Exchange-by-exchange progress
- Agent responses
- Broker guidance
- Progress percentages
- Completion status

## 🛠️ Troubleshooting

### Common Issues

1. **XAI API Token Missing**
   ```
   ❌ XAI_API_TOKEN not found in environment variables
   ```
   **Solution**: Add your token to the `.env` file

2. **API Rate Limits**
   ```
   ❌ XAI API error: 429 - Rate limit exceeded
   ```
   **Solution**: Wait and retry, or implement rate limiting

3. **Network Issues**
   ```
   ❌ XAI API error: Connection timeout
   ```
   **Solution**: Check internet connection and retry

### Debug Mode

Enable detailed logging by modifying the API calls to include error handling and retry logic.

## 🎯 Use Cases

- **Workplace Communication Training**
- **Conflict Resolution Simulation**
- **Project Planning Discussions**
- **Cross-Departmental Collaboration**
- **Decision-Making Processes**
- **Team Building Exercises**

## 📚 Examples

See `demo_agents.py` for comprehensive examples of different conversation scenarios and agent configurations.

## 🤝 Contributing

To extend the system:
1. Add new agent types by extending the base classes
2. Implement new conversation scenarios
3. Add additional analysis features to the broker
4. Create custom conversation templates

## 📄 License

This project is part of the Click2Lead system and follows the same licensing terms. 
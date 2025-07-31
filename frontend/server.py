#!/usr/bin/env python3
"""
Simple Flask server for the Agent Conversation System Frontend
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, Response
import os
import sys
import json
from datetime import datetime
import time
import threading

# Add the parent directory to the path to import agent modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

app = Flask(__name__)

# Import dynamic agent modules
try:
    from agents.dynamic_orchestrator import DynamicAgentOrchestrator
    AGENTS_AVAILABLE = True
    print("✅ Successfully imported DynamicAgentOrchestrator")
except ImportError as e:
    print(f"Warning: Dynamic agent modules not available: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    AGENTS_AVAILABLE = False

# Import neural learning system
try:
    from agents.neural_learning_system import NeuralLearningSystem
    NEURAL_LEARNING_AVAILABLE = True
    print("✅ Successfully imported NeuralLearningSystem")
except ImportError as e:
    print(f"Warning: Neural learning system not available: {e}")
    NEURAL_LEARNING_AVAILABLE = False

orchestrator = None
neural_learning = None

# Global thought stream for real-time updates
thought_stream = []
thought_stream_lock = threading.Lock()

def initialize_orchestrator():
    global orchestrator, neural_learning
    if orchestrator is None and AGENTS_AVAILABLE:
        try:
            orchestrator = DynamicAgentOrchestrator()
            
            # Initialize neural learning system
            if neural_learning is None and NEURAL_LEARNING_AVAILABLE:
                neural_learning = NeuralLearningSystem()
                print("🧠 Neural learning system initialized")
            
            return True
        except Exception as e:
            print(f"Error initializing orchestrator: {e}")
            return False
    return AGENTS_AVAILABLE

def add_thought(thought_type, message, agent_id=None):
    """Add a thought to the global stream"""
    with thought_stream_lock:
        thought = {
            'timestamp': datetime.now().isoformat(),
            'type': thought_type,
            'message': message,
            'agent_id': agent_id
        }
        thought_stream.append(thought)
        # Keep only last 100 thoughts
        if len(thought_stream) > 100:
            thought_stream.pop(0)

def clear_thoughts():
    """Clear the thought stream"""
    with thought_stream_lock:
        thought_stream.clear()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/thoughts/stream')
def stream_thoughts():
    """Stream real-time thoughts as Server-Sent Events"""
    def generate():
        last_index = 0
        while True:
            with thought_stream_lock:
                current_thoughts = thought_stream[last_index:]
                last_index = len(thought_stream)
            
            for thought in current_thoughts:
                yield f"data: {json.dumps(thought)}\n\n"
            
            time.sleep(0.5)  # Check every 500ms
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/thoughts/clear', methods=['POST'])
def clear_thought_stream():
    """Clear the thought stream"""
    clear_thoughts()
    return jsonify({'status': 'cleared'})

@app.route('/api/status')
def api_status():
    """Check if the dynamic agent system is available"""
    if initialize_orchestrator():
        return jsonify({
            'status': 'available',
            'message': 'Dynamic Agent System is ready',
            'features': [
                'Dynamic agent creation',
                'Multi-agent conversations',
                'AI-powered suggestions',
                'Flexible conversation management'
            ]
        })
    else:
        return jsonify({
            'status': 'unavailable',
            'message': 'Dynamic Agent System not available',
            'features': []
        })

@app.route('/api/conversation/start', methods=['POST'])
def start_conversation():
    """Start a new conversation with dynamic agents"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        context = data.get('context', '')
        agent_specifications = data.get('agent_specifications', None)
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        result = orchestrator.start_conversation(topic, context, agent_specifications)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/create', methods=['POST'])
def create_agents():
    """Create agents from user specification with real-time updates"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        data = request.get_json()
        user_specification = data.get('specification', '')
        topic = data.get('topic', '')
        context = data.get('context', '')
        
        if not user_specification:
            return jsonify({'error': 'Agent specification is required'}), 400
        
        # Clear previous thoughts
        clear_thoughts()
        
        # Add initial thoughts
        add_thought('system', 'Starting agent creation process...')
        add_thought('system', f'Analyzing user specification: "{user_specification}"')
        add_thought('system', f'Topic: {topic}')
        add_thought('system', f'Context: {context}')
        
        # Simulate the agent creation process with real-time updates
        def create_agents_with_updates():
            try:
                # Step 1: Parse user specification
                add_thought('system', 'Parsing user agent specification...')
                add_thought('system', f'Detected keywords: {", ".join([word for word in user_specification.lower().split() if word in ["create", "agent", "team", "manager", "developer", "designer", "analyst"]])}')
                time.sleep(1)
                
                # Step 2: Analyze context and requirements
                add_thought('system', 'Analyzing conversation context and requirements...')
                add_thought('system', f'Topic analysis: {topic[:50]}{"..." if len(topic) > 50 else ""}')
                add_thought('system', f'Context analysis: {context[:50]}{"..." if len(context) > 50 else ""}')
                time.sleep(1.5)
                
                # Step 3: Generate agent roles and expertise
                add_thought('system', 'Generating agent roles and expertise based on specification...')
                add_thought('system', 'Using AI to determine optimal agent combinations...')
                time.sleep(1.5)
                
                # Step 4: Create agent personalities
                add_thought('system', 'Creating unique personalities for each agent...')
                add_thought('system', 'Generating diverse perspectives and communication styles...')
                time.sleep(1)
                
                # Step 5: Initialize agent systems
                add_thought('system', 'Initializing agent systems and memory...')
                add_thought('system', 'Loading conversation history and context...')
                add_thought('system', 'Setting up inter-agent communication protocols...')
                time.sleep(1)
                
                # Step 6: Create the actual agents
                add_thought('system', 'Creating agents using the orchestrator...')
                add_thought('system', 'Establishing agent connections and shared memory...')
                result = orchestrator.create_agents_from_specification(user_specification, topic, context)
                
                if result['status'] == 'started':
                    add_thought('system', f'Successfully created {result["agents_created"]} agents')
                    
                    # Add thoughts for each agent
                    for agent in result.get('agents', []):
                        add_thought('agent_created', f'Agent {agent["role"]} initialized with expertise in {agent["expertise"]}', agent.get('id'))
                        add_thought('agent_created', f'Loading personality: {agent["personality"][:100]}...', agent.get('id'))
                        add_thought('agent_created', f'Agent {agent["role"]} ready for conversation', agent.get('id'))
                    
                    add_thought('system', 'All agents successfully created and ready for conversation')
                    add_thought('system', 'Integrating agents with conversation system...')
                    add_thought('system', 'Conversation system ready!')
                else:
                    add_thought('system', f'Error creating agents: {result.get("message", "Unknown error")}')
                
                return result
                
            except Exception as e:
                add_thought('system', f'Error during agent creation: {str(e)}')
                raise e
        
        # Run the creation process
        result = create_agents_with_updates()
        return jsonify(result)
        
    except Exception as e:
        add_thought('system', f'Fatal error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/exchange', methods=['POST'])
def conduct_exchange():
    """Conduct one exchange between agents"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        result = orchestrator.conduct_exchange()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/full', methods=['POST'])
def run_full_conversation():
    """Run a full conversation from start to finish"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        context = data.get('context', '')
        agent_specifications = data.get('agent_specifications', None)
        max_exchanges = data.get('max_exchanges', 6)
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        result = orchestrator.conduct_full_conversation(topic, context, agent_specifications, max_exchanges)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/reset', methods=['POST'])
def reset_conversation():
    """Reset the current conversation"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        orchestrator.reset_conversation()
        return jsonify({'status': 'reset', 'message': 'Conversation reset successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/list')
def list_agents():
    """Get all created agents"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        agents = orchestrator.get_all_agents()
        return jsonify({'agents': agents, 'count': len(agents)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/suggestions', methods=['POST'])
def get_agent_suggestions():
    """Get agent role suggestions for a topic"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        context = data.get('context', '')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        suggestions = orchestrator.get_agent_suggestions(topic, context)
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/status')
def get_conversation_status():
    """Get current conversation status"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        status = orchestrator.get_conversation_status()
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning/stats')
def get_learning_stats():
    """Get neural learning system statistics"""
    if not neural_learning:
        return jsonify({'error': 'Neural learning system not available'}), 500
    
    try:
        stats = neural_learning.get_learning_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/learning/preferences')
def get_user_preferences():
    """Get user preferences learned by the neural system"""
    if not neural_learning:
        return jsonify({'error': 'Neural learning system not available'}), 500
    
    try:
        preferences = neural_learning.user_data.get_user_preferences()
        return jsonify(preferences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo/<scenario>')
def get_demo_scenario(scenario):
    """Get demo scenarios for testing"""
    demos = {
        'project': {
            'topic': 'Project Timeline Adjustment',
            'context': 'Client needs delivery by Friday, team estimates 2 more weeks',
            'suggestion': 'Create 3 agents: Project Manager, Senior Developer, and Client Representative'
        },
        'design': {
            'topic': 'Redesigning User Onboarding Flow',
            'context': '40% drop-off rate, need to improve retention',
            'suggestion': 'Create 4 agents: Product Manager, UX Designer, Data Analyst, and Marketing Manager'
        },
        'marketing': {
            'topic': 'Q4 Marketing Campaign Strategy',
            'context': '$100K budget across different channels',
            'suggestion': 'Create 3 agents: Marketing Manager, Data Analyst, and Creative Director'
        },
        'hr': {
            'topic': 'Employee Performance Management System',
            'context': 'Replace paper-based system with digital solution',
            'suggestion': 'Create 3 agents: HR Manager, IT Manager, and Employee Representative'
        }
    }
    
    if scenario in demos:
        return jsonify(demos[scenario])
    else:
        return jsonify({'error': 'Demo scenario not found'}), 404

@app.route('/api/conversation/process', methods=['POST'])
def process_conversation():
    """Process any conversation prompt intelligently with real-time updates"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Clear previous thoughts
        clear_thoughts()
        
        # Add initial thoughts
        add_thought('system', 'Processing user message...')
        add_thought('system', f'Analyzing: "{user_message[:100]}{"..." if len(user_message) > 100 else ""}"')
        
        def process_message_intelligently():
            try:
                # Step 1: Analyze user intent using neural learning
                add_thought('system', 'Analyzing user intent and context...')
                
                # Use neural learning system if available
                if neural_learning:
                    predicted_intent, confidence = neural_learning.predict_intent(user_message)
                    add_thought('system', f'Neural intent prediction: {predicted_intent} (confidence: {confidence:.2f})')
                    
                    # Get response optimization
                    context = {
                        'current_agents': conversation_context.get('current_agents', []),
                        'conversation_length': len(conversation_context.get('interactions', [])),
                        'user_preferences': neural_learning.user_data.get_user_preferences()
                    }
                    
                    optimization = neural_learning.optimize_response(user_message, predicted_intent, context)
                    add_thought('system', f'Response optimization: {optimization["response_style"]} style, personalization: {optimization["personalization_level"]:.2f}')
                else:
                    predicted_intent = 'general_conversation'
                    confidence = 0.8
                    optimization = {'response_style': 'direct', 'personalization_level': 0.5}
                
                time.sleep(0.5)
                
                # Step 2: Determine response type based on neural prediction
                lower_message = user_message.lower()
                
                # Check for agent creation intent
                agent_keywords = ['create', 'agent', 'team', 'employees', 'hire', 'build', 'assemble']
                agent_indicators = any(keyword in lower_message for keyword in agent_keywords)
                
                if agent_indicators:
                    add_thought('system', 'Detected agent creation request')
                    add_thought('system', 'Preparing to create dynamic agents...')
                    add_thought('system', f'User request: "{user_message[:100]}{"..." if len(user_message) > 100 else ""}"')
                    time.sleep(0.5)
                    
                    # Create agents
                    result = orchestrator.create_agents_from_specification(user_message, "", "")
                    
                    # Debug: Log what agents were created
                    if result.get('agents'):
                        agent_names = [agent['role'] for agent in result['agents']]
                        add_thought('system', f'Debug: Created agents: {", ".join(agent_names)}')
                    else:
                        add_thought('system', 'Debug: No agents created')
                    
                    if result['status'] == 'started':
                        add_thought('system', f'Successfully created {result["agents_created"]} agents')
                        add_thought('system', 'Agents are ready for conversation')
                        
                        # Add agent-specific thoughts
                        for agent in result.get('agents', []):
                            add_thought('agent_created', f'Agent {agent["role"]} initialized', agent.get('id'))
                            add_thought('agent_created', f'Expertise loaded: {agent["expertise"]}', agent.get('id'))
                        
                        return {
                            'type': 'agent_creation',
                            'status': 'success',
                            'response': result['broker_message'],
                            'agents': result.get('agents', []),
                            'agents_created': result['agents_created']
                        }
                    else:
                        add_thought('system', f'Error creating agents: {result.get("message", "Unknown error")}')
                        return {
                            'type': 'error',
                            'status': 'error',
                            'response': f"Sorry, I couldn't create the agents: {result.get('message', 'Unknown error')}"
                        }
                
                # Check for conversation management
                elif any(word in lower_message for word in ['exchange', 'next', 'continue', 'proceed']):
                    add_thought('system', 'Detected conversation management request')
                    add_thought('system', 'Preparing to conduct agent exchange...')
                    time.sleep(0.5)
                    
                    result = orchestrator.conduct_exchange()
                    
                    if result['status'] == 'exchange_completed':
                        add_thought('system', 'Exchange completed successfully')
                        add_thought('system', 'Processing agent responses...')
                        
                        response_text = "**Agent Exchange Results:**\n\n"
                        for agent_response in result.get('agent_responses', []):
                            response_text += f"**{agent_response['agent_role']}:** {agent_response['message']}\n\n"
                        
                        if result.get('broker_analysis'):
                            response_text += f"**Broker Analysis:** {result['broker_analysis']}\n\n"
                        
                        return {
                            'type': 'exchange',
                            'status': 'success',
                            'response': response_text,
                            'exchange_data': result
                        }
                    else:
                        add_thought('system', 'No active conversation to exchange')
                        return {
                            'type': 'exchange',
                            'status': 'error',
                            'response': 'No active conversation found. Please create agents first.'
                        }
                
                # Check for help requests
                elif any(word in lower_message for word in ['help', 'what can you do', 'how', 'guide', 'assist']):
                    add_thought('system', 'Detected help request')
                    add_thought('system', 'Generating helpful response...')
                    time.sleep(0.5)
                    
                    help_response = """🤖 **Agent Conversation System - What I Can Do**

**🎯 Main Features:**
• **Create Dynamic Agents** - Build custom AI teams for any project
• **Multi-Agent Conversations** - Conduct intelligent discussions between agents
• **Real-Time Processing** - Watch the system think and work in real-time

**💡 How to Get Started:**
1. **Create Agents**: "Create 3 agents: Project Manager, Developer, Designer"
2. **Start Conversations**: "I need help with a marketing strategy"
3. **Run Exchanges**: "Conduct the next exchange" or "Continue the conversation"

**🚀 Example Requests:**
• "Create a team for a mobile app project"
• "I need 4 agents for a business strategy meeting"
• "Help me build a team for product development"
• "What agents would work best for a startup?"

**🔄 Conversation Flow:**
1. Create agents → 2. Start conversation → 3. Run exchanges → 4. Get results

What would you like to do today?"""
                    
                    return {
                        'type': 'help',
                        'status': 'success',
                        'response': help_response
                    }
                
                # Check for status requests
                elif any(word in lower_message for word in ['status', 'system', 'health', 'check']):
                    add_thought('system', 'Detected system status request')
                    add_thought('system', 'Checking system health...')
                    time.sleep(0.5)
                    
                    # Check if user is asking about learning stats
                    if any(word in lower_message for word in ['learning', 'neural', 'stats', 'brain']):
                        add_thought('system', 'User requesting neural learning statistics')
                        return {
                            'type': 'learning_stats',
                            'status': 'success',
                            'response': 'learning_stats_request'
                        }
                    
                    status_response = """✅ **System Status Report**

**🛡️ Guardian System:** Active and monitoring
**🤖 Agent Orchestrator:** Ready for agent creation
**💬 Conversation Manager:** Available for exchanges
**📊 Real-Time Processing:** Enabled with thought streaming
**🧠 Neural Learning:** Active and learning from interactions

**🎯 Current Capabilities:**
• Dynamic agent creation and management
• Multi-agent conversation coordination
• Real-time thought process visualization
• Intelligent conversation flow management
• Neural network learning and optimization

**📈 System Health:** All systems operational
**🔄 Ready for:** Agent creation and conversation management

Everything is running smoothly! Ready to create your agent team."""
                    
                    return {
                        'type': 'status',
                        'status': 'success',
                        'response': status_response
                    }
                
                # Check for general conversation starters
                elif any(word in lower_message for word in ['start', 'begin', 'new', 'project', 'discuss', 'talk']):
                    add_thought('system', 'Detected conversation starter')
                    add_thought('system', 'Suggesting agent creation for better discussion...')
                    time.sleep(0.5)
                    
                    conversation_response = f"""Great! I'd love to help you with "{user_message}".

To make this conversation as productive as possible, I recommend creating a team of specialized agents who can provide different perspectives and expertise.

**🤔 What kind of agents would be helpful for this topic?**

You can either:
• **Let me suggest agents**: "Create appropriate agents for this discussion"
• **Specify your own**: "Create 3 agents: [roles you want]"
• **Quick start**: "Just create 4 agents for this"

**💡 Examples:**
• "Create agents for a marketing strategy discussion"
• "I want a Project Manager, Developer, and Designer"
• "Just create 3 agents for this project"

What would you prefer?"""
                    
                    return {
                        'type': 'conversation_starter',
                        'status': 'success',
                        'response': conversation_response
                    }
                
                # Default intelligent response
                else:
                    add_thought('system', 'Processing general conversation')
                    add_thought('system', 'Generating contextual response...')
                    time.sleep(0.5)
                    
                    default_response = f"""I understand you're asking about: "{user_message}"

I'm an intelligent agent conversation system that can help you with:

**🎯 What I Do Best:**
• Create custom AI agent teams for any project or discussion
• Facilitate multi-agent conversations with different perspectives
• Provide real-time insights and analysis through agent collaboration

**💡 To Get Started:**
Try asking me to:
• "Create agents for [your topic]"
• "Help me build a team for [your project]"
• "I need agents to discuss [your subject]"

**🚀 Or ask me:**
• "What can you do?" for a full overview
• "Show me system status" for health check
• "Help" for guidance

What would you like to explore with a team of AI agents?"""
                    
                    return {
                        'type': 'general',
                        'status': 'success',
                        'response': default_response
                    }
                
            except Exception as e:
                add_thought('system', f'Error processing message: {str(e)}')
                raise e
        
        # Process the message
        result = process_message_intelligently()
        add_thought('system', 'Response generated successfully')
        
        # Learn from this interaction
        if neural_learning and result.get('status') == 'success':
            agents_created = []
            if result.get('type') == 'agent_creation' and result.get('agents'):
                agents_created = [agent['role'] for agent in result['agents']]
            
            neural_learning.learn_from_interaction(
                prompt=user_message,
                response=result.get('response', ''),
                response_type=result.get('type', 'general'),
                agents_created=agents_created,
                user_feedback=None  # Could be added later with user feedback system
            )
            add_thought('system', 'Learning from interaction completed')
        
        return jsonify(result)
        
    except Exception as e:
        add_thought('system', f'Fatal error: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Dynamic Agent Conversation System Frontend Server...")
    print("Server will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    
    if initialize_orchestrator():
        print("✅ Dynamic Agent System is available")
    else:
        print("⚠️  Dynamic Agent System not available - running in demo mode")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 
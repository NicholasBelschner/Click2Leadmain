#!/usr/bin/env python3
"""
Simple Flask server for the Agent Conversation System Frontend
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import json
from datetime import datetime

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

orchestrator = None

def initialize_orchestrator():
    global orchestrator
    if orchestrator is None and AGENTS_AVAILABLE:
        try:
            orchestrator = DynamicAgentOrchestrator()
            return True
        except Exception as e:
            print(f"Error initializing orchestrator: {e}")
            return False
    return AGENTS_AVAILABLE

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

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
    """Create agents from user specification"""
    if not initialize_orchestrator():
        return jsonify({'error': 'Agent system not available'}), 500
    
    try:
        data = request.get_json()
        user_specification = data.get('specification', '')
        topic = data.get('topic', '')
        context = data.get('context', '')
        
        if not user_specification:
            return jsonify({'error': 'Agent specification is required'}), 400
        
        result = orchestrator.create_agents_from_specification(user_specification, topic, context)
        return jsonify(result)
        
    except Exception as e:
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

if __name__ == '__main__':
    print("Starting Dynamic Agent Conversation System Frontend Server...")
    print("Server will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    
    if initialize_orchestrator():
        print("✅ Dynamic Agent System is available")
    else:
        print("⚠️  Dynamic Agent System not available - running in demo mode")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 
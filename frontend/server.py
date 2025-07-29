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
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__)

# Import agent modules
try:
    from agents.agent_orchestrator import AgentOrchestrator
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Agent modules not available: {e}")
    AGENTS_AVAILABLE = False

# Global orchestrator instance
orchestrator = None

def initialize_orchestrator():
    """Initialize the agent orchestrator"""
    global orchestrator
    if AGENTS_AVAILABLE and orchestrator is None:
        try:
            orchestrator = AgentOrchestrator()
            return True
        except Exception as e:
            print(f"Error initializing orchestrator: {e}")
            return False
    return AGENTS_AVAILABLE

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/status')
def api_status():
    """Check system status"""
    try:
        if initialize_orchestrator():
            return jsonify({
                'status': 'connected',
                'agents': 'ready',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'demo_mode',
                'agents': 'not_available',
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/conversation/start', methods=['POST'])
def start_conversation():
    """Start a new conversation"""
    try:
        data = request.get_json()
        
        if not initialize_orchestrator():
            return jsonify({
                'error': 'Agent system not available'
            }), 503
        
        # Extract parameters
        topic = data.get('topic', '')
        context = data.get('context', '')
        employee1_role = data.get('employee1_role', 'Project Manager')
        employee1_expertise = data.get('employee1_expertise', 'Project planning and coordination')
        employee2_role = data.get('employee2_role', 'Senior Developer')
        employee2_expertise = data.get('employee2_expertise', 'Technical implementation')
        max_exchanges = data.get('max_exchanges', 4)
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Start conversation
        result = orchestrator.start_conversation(topic, context)
        
        return jsonify({
            'success': True,
            'conversation_id': result.get('conversation_id'),
            'initial_perspectives': {
                'employee1': result.get('employee1_perspective'),
                'employee2': result.get('employee2_perspective'),
                'broker_analysis': result.get('broker_analysis')
            },
            'max_exchanges': max_exchanges
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error starting conversation: {str(e)}'
        }), 500

@app.route('/api/conversation/exchange', methods=['POST'])
def conduct_exchange():
    """Conduct the next exchange in the conversation"""
    try:
        if not initialize_orchestrator():
            return jsonify({
                'error': 'Agent system not available'
            }), 503
        
        # Conduct exchange
        result = orchestrator.conduct_exchange()
        
        return jsonify({
            'success': True,
            'exchange': result.get('exchange'),
            'broker_analysis': result.get('broker_analysis'),
            'progress': result.get('progress'),
            'is_complete': result.get('is_complete', False)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error conducting exchange: {str(e)}'
        }), 500

@app.route('/api/conversation/full', methods=['POST'])
def run_full_conversation():
    """Run the complete conversation"""
    try:
        data = request.get_json()
        
        if not initialize_orchestrator():
            return jsonify({
                'error': 'Agent system not available'
            }), 503
        
        # Extract parameters
        topic = data.get('topic', '')
        context = data.get('context', '')
        max_exchanges = data.get('max_exchanges', 4)
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Run full conversation
        result = orchestrator.conduct_full_conversation(topic, context, max_exchanges)
        
        return jsonify({
            'success': True,
            'conversation': result.get('conversation'),
            'summary': result.get('summary'),
            'exchanges': result.get('exchanges', []),
            'final_status': result.get('final_status')
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error running full conversation: {str(e)}'
        }), 500

@app.route('/api/conversation/reset', methods=['POST'])
def reset_conversation():
    """Reset the current conversation"""
    try:
        if not initialize_orchestrator():
            return jsonify({
                'error': 'Agent system not available'
            }), 503
        
        orchestrator.reset_conversation()
        
        return jsonify({
            'success': True,
            'message': 'Conversation reset successfully'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error resetting conversation: {str(e)}'
        }), 500

@app.route('/api/demo/<scenario>')
def get_demo_scenario(scenario):
    """Get demo scenario configuration"""
    scenarios = {
        'project': {
            'topic': 'Project Timeline Adjustment for Authentication Module',
            'context': 'Client needs delivery by Friday, team estimates 2 more weeks',
            'employee1_role': 'Project Manager',
            'employee1_expertise': 'Project planning and coordination',
            'employee2_role': 'Senior Developer',
            'employee2_expertise': 'Technical implementation and system architecture'
        },
        'design': {
            'topic': 'Redesigning User Onboarding Flow',
            'context': '40% drop-off rate, need to improve retention',
            'employee1_role': 'Product Manager',
            'employee1_expertise': 'Product strategy and user experience',
            'employee2_role': 'UX Designer',
            'employee2_expertise': 'User interface design and user research'
        },
        'marketing': {
            'topic': 'Q4 Marketing Campaign Budget Allocation',
            'context': '$100K budget across different channels',
            'employee1_role': 'Marketing Manager',
            'employee1_expertise': 'Marketing strategy and campaign management',
            'employee2_role': 'Data Analyst',
            'employee2_expertise': 'Data analysis and performance optimization'
        },
        'hr': {
            'topic': 'Employee Performance Management System Implementation',
            'context': 'Replace paper-based system with digital solution',
            'employee1_role': 'HR Manager',
            'employee1_expertise': 'Human resources and employee relations',
            'employee2_role': 'IT Manager',
            'employee2_expertise': 'Information technology and system implementation'
        }
    }
    
    if scenario in scenarios:
        return jsonify(scenarios[scenario])
    else:
        return jsonify({'error': 'Scenario not found'}), 404

if __name__ == '__main__':
    print("Starting Agent Conversation System Frontend Server...")
    print("Server will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    
    # Check if agents are available
    if AGENTS_AVAILABLE:
        print("✅ Agent system is available")
    else:
        print("⚠️  Agent system not available - running in demo mode")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 
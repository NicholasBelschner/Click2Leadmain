#!/usr/bin/env python3
"""
Production Flask application for Click2Lead deployment
"""

import os
import sys
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')

# Global variables for thought streaming
thought_stream = []
thought_stream_lock = None

def add_thought(thought_type, message, agent_id=None):
    """Add a thought to the stream"""
    global thought_stream
    thought = {
        'type': thought_type,
        'message': message,
        'agent_id': agent_id,
        'timestamp': time.time()
    }
    thought_stream.append(thought)
    if len(thought_stream) > 100:
        thought_stream.pop(0)

def clear_thoughts():
    """Clear the thought stream"""
    global thought_stream
    thought_stream.clear()

# Initialize core systems
try:
    from agents.dynamic_orchestrator import DynamicAgentOrchestrator
    from agents.neural_learning_system import NeuralLearningSystem
    
    orchestrator = DynamicAgentOrchestrator()
    neural_learning = NeuralLearningSystem()
    print("✅ Systems initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: {e}")
    orchestrator = None
    neural_learning = None

# Import all routes from the frontend server
try:
    from frontend.server import *
    print("✅ Routes imported successfully")
except Exception as e:
    print(f"⚠️ Warning importing routes: {e}")

# Health check endpoint
@app.route('/api/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'orchestrator_available': orchestrator is not None,
        'neural_learning_available': neural_learning is not None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 
#!/usr/bin/env python3
"""
Dynamic Agent Orchestrator
Orchestrates conversations with any number of dynamically created agents
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

from .dynamic_broker import DynamicBrokerAgent
from .dynamic_agent_manager import DynamicAgentManager

load_dotenv()

class DynamicAgentOrchestrator:
    def __init__(self):
        self.broker = DynamicBrokerAgent()
        self.agent_manager = DynamicAgentManager()
        self.current_conversation = None
        self.conversation_log = []
        
    def start_conversation(self, topic: str, context: str = "", agent_specifications: List[Dict] = None) -> Dict:
        """
        Start a new conversation with specified or dynamically created agents
        """
        try:
            result = self.broker.start_conversation(topic, context, agent_specifications)
            
            if result['status'] == 'needs_agents':
                # User needs to specify agents
                return {
                    'status': 'needs_agents',
                    'message': result['message'],
                    'suggestions': result['suggestions'],
                    'topic': result['topic'],
                    'context': result['context']
                }
            elif result['status'] == 'started':
                # Conversation started successfully
                self.current_conversation = result
                return {
                    'status': 'started',
                    'conversation_id': result['conversation_id'],
                    'agents_created': result['agents_created'],
                    'broker_message': result['broker_message'],
                    'agents': result['agents']
                }
            else:
                return result
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error starting conversation: {str(e)}"
            }
    
    def create_agents_from_specification(self, user_specification: str, topic: str, context: str) -> Dict:
        """
        Create agents based on user's specification and start conversation
        """
        try:
            result = self.broker.create_agents_from_user_specification(user_specification, topic, context)
            
            if result['status'] == 'started':
                self.current_conversation = result
                
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error creating agents: {str(e)}"
            }
    
    def conduct_exchange(self) -> Dict:
        """
        Conduct one exchange between all active agents
        """
        if not self.current_conversation:
            return {
                'status': 'error',
                'message': 'No active conversation. Please start a conversation first.'
            }
        
        try:
            result = self.broker.conduct_exchange()
            
            # Log the exchange
            if result['status'] == 'exchange_completed':
                self.conversation_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'exchange_number': result['exchange_number'],
                    'agent_responses': result['agent_responses'],
                    'broker_analysis': result['broker_analysis']
                })
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error conducting exchange: {str(e)}"
            }
    
    def conduct_full_conversation(self, topic: str, context: str = "", 
                                agent_specifications: List[Dict] = None, 
                                max_exchanges: int = 6) -> Dict:
        """
        Conduct a full conversation from start to finish
        """
        try:
            # Start conversation
            start_result = self.start_conversation(topic, context, agent_specifications)
            
            if start_result['status'] == 'needs_agents':
                return start_result
            
            if start_result['status'] != 'started':
                return start_result
            
            # Set max exchanges
            self.broker.max_exchanges = max_exchanges
            
            # Conduct exchanges
            exchanges = []
            for i in range(max_exchanges):
                print(f"Conducting exchange {i+1}/{max_exchanges}...")
                
                exchange_result = self.conduct_exchange()
                
                if exchange_result['status'] == 'concluded':
                    exchanges.append(exchange_result)
                    break
                elif exchange_result['status'] == 'exchange_completed':
                    exchanges.append(exchange_result)
                else:
                    return exchange_result
            
            # Save conversation log
            self.save_conversation_log()
            
            return {
                'status': 'completed',
                'topic': topic,
                'context': context,
                'total_exchanges': len(exchanges),
                'exchanges': exchanges,
                'agents': self.broker.active_agents
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error conducting full conversation: {str(e)}"
            }
    
    def get_conversation_status(self) -> Dict:
        """
        Get current conversation status
        """
        if not self.current_conversation:
            return {'status': 'no_conversation'}
        
        return self.broker.get_conversation_summary()
    
    def get_all_agents(self) -> List[Dict]:
        """
        Get all created agents
        """
        return self.agent_manager.get_all_agents()
    
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """
        Get specific agent by ID
        """
        return self.agent_manager.get_agent(agent_id)
    
    def update_agent(self, agent_id: str, updates: Dict) -> bool:
        """
        Update agent properties
        """
        return self.agent_manager.update_agent(agent_id, updates)
    
    def delete_agent(self, agent_id: str) -> bool:
        """
        Delete an agent
        """
        return self.agent_manager.delete_agent(agent_id)
    
    def save_conversation_log(self, filename: str = None) -> str:
        """
        Save conversation log to file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_log_{timestamp}.json"
        
        data = {
            'conversation_log': self.conversation_log,
            'current_conversation': self.current_conversation,
            'all_agents': self.agent_manager.get_all_agents(),
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def reset_conversation(self):
        """
        Reset conversation state
        """
        self.broker.reset_conversation()
        self.current_conversation = None
        self.conversation_log = []
    
    def get_agent_suggestions(self, topic: str, context: str) -> List[Dict]:
        """
        Get suggestions for agent roles based on topic
        """
        try:
            return self.broker.helper.suggest_agent_roles(topic, context)
        except Exception as e:
            return []
    
    def validate_agent_specification(self, role: str, expertise: str) -> Dict:
        """
        Validate and enhance agent specification
        """
        try:
            return self.broker.helper.validate_agent_specification(role, expertise)
        except Exception as e:
            return {
                'is_valid': True,
                'suggestions': 'Unable to validate due to error',
                'enhanced_role': role,
                'enhanced_expertise': expertise,
                'personality_traits': ['Professional', 'Collaborative']
            }

# Example usage and testing
if __name__ == "__main__":
    try:
        orchestrator = DynamicAgentOrchestrator()
        print("✅ Dynamic Agent Orchestrator initialized successfully!")
        
        # Test 1: Start conversation without agents (should prompt for agents)
        print("\n🧪 Test 1: Starting conversation without agents...")
        result1 = orchestrator.start_conversation(
            topic="Redesigning the user onboarding flow",
            context="Current drop-off rate is 40%, need to improve user retention"
        )
        
        print(f"Result: {result1['status']}")
        if result1['status'] == 'needs_agents':
            print(f"Suggestions: {len(result1['suggestions'])} agent roles")
        
        # Test 2: Create agents from specification
        print("\n🧪 Test 2: Creating agents from specification...")
        result2 = orchestrator.create_agents_from_specification(
            "Create 3 agents: Product Manager, UX Designer, and Developer",
            "Redesigning the user onboarding flow",
            "Current drop-off rate is 40%, need to improve user retention"
        )
        
        print(f"Result: {result2['status']}")
        if result2['status'] == 'started':
            print(f"Agents created: {result2['agents_created']}")
        
        # Test 3: Conduct an exchange
        if result2['status'] == 'started':
            print("\n🧪 Test 3: Conducting exchange...")
            result3 = orchestrator.conduct_exchange()
            print(f"Exchange result: {result3['status']}")
        
        # Test 4: Get all agents
        print("\n🧪 Test 4: Getting all agents...")
        agents = orchestrator.get_all_agents()
        print(f"Total agents: {len(agents)}")
        for agent in agents:
            print(f"  - {agent['role']} (ID: {agent['id']})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure XAI_API_TOKEN is set in your .env file") 
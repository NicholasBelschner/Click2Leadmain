#!/usr/bin/env python3
"""
Agent Orchestrator - Coordinates the broker, employee1, and employee2 agents.
Manages the complete conversation flow and ensures efficient communication.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

from broker import BrokerAgent
from employee1 import Employee1Agent
from employee2 import Employee2Agent

# Load environment variables
load_dotenv()

class AgentOrchestrator:
    """
    Main orchestrator that coordinates all three agents for efficient conversations.
    """
    
    def __init__(self, employee1_role: str = "Project Manager", 
                 employee1_expertise: str = "Project planning and coordination",
                 employee2_role: str = "Senior Developer",
                 employee2_expertise: str = "Technical implementation and system architecture"):
        
        # Initialize all agents
        self.broker = BrokerAgent()
        self.employee1 = Employee1Agent(role=employee1_role, expertise=employee1_expertise)
        self.employee2 = Employee2Agent(role=employee2_role, expertise=employee2_expertise)
        
        # Conversation state
        self.current_conversation = None
        self.conversation_log = []
        
    def start_conversation(self, topic: str, context: str = "") -> Dict:
        """
        Start a new conversation between Employee1 and Employee2.
        
        Args:
            topic: The main topic to discuss
            context: Additional context about the situation
        
        Returns:
            Dict containing conversation setup and initial messages
        """
        # Start broker conversation
        broker_result = self.broker.start_conversation(
            topic=topic,
            employee1_context=f"{self.employee1.role} - {self.employee1.expertise}",
            employee2_context=f"{self.employee2.role} - {self.employee2.expertise}"
        )
        
        self.current_conversation = broker_result
        
        # Get initial perspectives from both employees
        employee1_perspective = self.employee1.provide_initial_perspective(topic, context)
        employee2_perspective = self.employee2.provide_initial_perspective(topic, context)
        
        # Log the conversation start
        self.conversation_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'conversation_started',
            'topic': topic,
            'context': context,
            'broker_setup': broker_result,
            'employee1_perspective': employee1_perspective,
            'employee2_perspective': employee2_perspective
        })
        
        return {
            'conversation_id': broker_result['conversation_id'],
            'topic': topic,
            'broker_message': broker_result['initial_message'],
            'employee1_perspective': employee1_perspective,
            'employee2_perspective': employee2_perspective,
            'status': 'started'
        }
    
    def conduct_exchange(self) -> Dict:
        """
        Conduct one exchange between Employee1 and Employee2.
        
        Returns:
            Dict containing the exchange results and broker analysis
        """
        if not self.current_conversation:
            raise ValueError("No active conversation. Start a conversation first.")
        
        # Get conversation history for context
        conversation_history = self.broker.conversation_history
        
        # Generate responses from both employees
        employee1_response = self.employee1.generate_response(
            topic=self.current_conversation['topic'],
            employee2_message=self.employee2.provide_initial_perspective(
                self.current_conversation['topic'], 
                "Responding to Employee1's perspective"
            ),
            conversation_history=conversation_history
        )
        
        employee2_response = self.employee2.generate_response(
            topic=self.current_conversation['topic'],
            employee1_message=employee1_response,
            conversation_history=conversation_history
        )
        
        # Coordinate the exchange through the broker
        broker_result = self.broker.coordinate_exchange(employee1_response, employee2_response)
        
        # Log the exchange
        self.conversation_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'exchange_conducted',
            'exchange_number': broker_result['exchange_number'],
            'employee1_response': employee1_response,
            'employee2_response': employee2_response,
            'broker_analysis': broker_result['analysis'],
            'progress': broker_result['progress']
        })
        
        return {
            'exchange_number': broker_result['exchange_number'],
            'employee1_response': employee1_response,
            'employee2_response': employee2_response,
            'broker_analysis': broker_result['analysis'],
            'progress': broker_result['progress'],
            'remaining_exchanges': broker_result['remaining_exchanges'],
            'should_continue': broker_result['should_continue']
        }
    
    def conduct_full_conversation(self, topic: str, context: str = "", max_exchanges: int = 6) -> Dict:
        """
        Conduct a full conversation from start to finish.
        
        Args:
            topic: The main topic to discuss
            context: Additional context about the situation
            max_exchanges: Maximum number of exchanges (default 6)
        
        Returns:
            Dict containing the complete conversation results
        """
        # Start the conversation
        start_result = self.start_conversation(topic, context)
        
        exchanges = []
        should_continue = True
        exchange_count = 0
        
        print(f"🎯 Starting conversation: {topic}")
        print(f"📋 Context: {context}")
        print(f"👥 Participants: {self.employee1.role} & {self.employee2.role}")
        print("=" * 60)
        
        # Conduct exchanges until completion or max reached
        while should_continue and exchange_count < max_exchanges:
            exchange_count += 1
            print(f"\n🔄 Exchange #{exchange_count}")
            print("-" * 40)
            
            exchange_result = self.conduct_exchange()
            exchanges.append(exchange_result)
            
            print(f"👤 {self.employee1.role}: {exchange_result['employee1_response']}")
            print(f"👤 {self.employee2.role}: {exchange_result['employee2_response']}")
            print(f"🤝 Broker: {exchange_result['broker_analysis']['broker_guidance']}")
            print(f"📊 Progress: {exchange_result['progress']['overall']:.1f}%")
            
            should_continue = exchange_result['should_continue']
            
            if should_continue:
                print(f"⏭️  Continuing... ({exchange_result['remaining_exchanges']} exchanges remaining)")
            else:
                print("✅ Conversation concluded")
        
        # Get final summary
        final_summary = self.broker.get_conversation_summary()
        
        print("\n" + "=" * 60)
        print("📋 CONVERSATION SUMMARY")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Total Exchanges: {len(exchanges)}")
        print(f"Final Progress: {final_summary['progress']['overall']:.1f}%")
        print(f"Status: {'Completed' if not should_continue else 'Max exchanges reached'}")
        
        return {
            'conversation_id': start_result['conversation_id'],
            'topic': topic,
            'context': context,
            'start_result': start_result,
            'exchanges': exchanges,
            'final_summary': final_summary,
            'total_exchanges': len(exchanges),
            'max_exchanges': max_exchanges,
            'completed': not should_continue,
            'conversation_log': self.conversation_log
        }
    
    def get_conversation_status(self) -> Dict:
        """
        Get the current status of the conversation.
        """
        if not self.current_conversation:
            return {'status': 'no_active_conversation'}
        
        broker_summary = self.broker.get_conversation_summary()
        
        return {
            'conversation_id': self.current_conversation['conversation_id'],
            'topic': self.current_conversation['topic'],
            'total_exchanges': broker_summary['total_exchanges'],
            'max_exchanges': broker_summary['max_exchanges'],
            'progress': broker_summary['progress'],
            'remaining_exchanges': broker_summary['max_exchanges'] - broker_summary['total_exchanges'],
            'status': 'active'
        }
    
    def reset_conversation(self):
        """
        Reset the conversation state.
        """
        self.broker.reset_conversation()
        self.current_conversation = None
        self.conversation_log = []
    
    def save_conversation_log(self, filename: str = None) -> str:
        """
        Save the conversation log to a JSON file.
        
        Args:
            filename: Optional filename, defaults to timestamp-based name
        
        Returns:
            The filename where the log was saved
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_log_{timestamp}.json"
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'conversation_log': self.conversation_log,
            'employee1_info': self.employee1.get_agent_info(),
            'employee2_info': self.employee2.get_agent_info()
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return filename
    
    def get_agent_info(self) -> Dict:
        """
        Get information about all agents.
        """
        return {
            'broker': {
                'name': 'Broker',
                'role': 'Communication Coordinator',
                'conversation_count': len(self.broker.conversation_history)
            },
            'employee1': self.employee1.get_agent_info(),
            'employee2': self.employee2.get_agent_info()
        }

# Example usage
if __name__ == "__main__":
    # Create orchestrator with custom roles
    orchestrator = AgentOrchestrator(
        employee1_role="Product Manager",
        employee1_expertise="Product strategy and user experience",
        employee2_role="UX Designer",
        employee2_expertise="User interface design and user research"
    )
    
    # Conduct a full conversation
    result = orchestrator.conduct_full_conversation(
        topic="Redesigning the user onboarding flow",
        context="Users are dropping off during the first 3 steps of onboarding",
        max_exchanges=4
    )
    
    # Save the conversation log
    log_file = orchestrator.save_conversation_log()
    print(f"\n💾 Conversation log saved to: {log_file}")
    
    # Get agent information
    agent_info = orchestrator.get_agent_info()
    print(f"\n👥 Agent Information:")
    for agent_name, info in agent_info.items():
        print(f"  {agent_name}: {info['role']}") 
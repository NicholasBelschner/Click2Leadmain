#!/usr/bin/env python3
"""
Broker Agent - The middleman that coordinates communication between Employee1 and Employee2.
Ensures efficient and systematic conversations within 3-6 exchanges maximum.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BrokerAgent:
    """
    Broker agent that manages communication between Employee1 and Employee2.
    Ensures conversations are efficient and systematic, completing within 3-6 exchanges.
    """
    
    def __init__(self):
        self.xai_api_token = os.getenv('XAI_API_TOKEN')
        if not self.xai_api_token:
            raise ValueError("XAI_API_TOKEN not found in environment variables")
        
        self.base_url = "https://api.x.ai/v1"
        self.conversation_history = []
        self.current_conversation_id = None
        self.exchange_count = 0
        self.max_exchanges = 6
        self.conversation_goals = []
        
        # Initialize the broker's personality and role
        self.broker_personality = """
        You are an efficient communication broker and coordinator. Your role is to:
        1. Facilitate clear communication between Employee1 and Employee2
        2. Ensure conversations stay focused and productive
        3. Monitor conversation progress and guide towards resolution
        4. Intervene when conversations become inefficient or off-track
        5. Summarize key points and ensure mutual understanding
        6. Track conversation goals and ensure they are met within 3-6 exchanges
        
        You are systematic, clear, and goal-oriented. You help both employees understand
        each other's perspectives and work towards common solutions efficiently.
        """
    
    def start_conversation(self, topic: str, employee1_context: str, employee2_context: str) -> Dict:
        """
        Start a new conversation between Employee1 and Employee2.
        
        Args:
            topic: The main topic or issue to discuss
            employee1_context: Context about Employee1's role and perspective
            employee2_context: Context about Employee2's role and perspective
        
        Returns:
            Dict containing conversation ID and initial setup
        """
        self.current_conversation_id = f"conv_{int(time.time())}"
        self.exchange_count = 0
        self.conversation_goals = []
        
        # Create conversation goals
        goals = [
            f"Clarify the main issue: {topic}",
            "Establish mutual understanding of perspectives",
            "Identify key requirements and constraints",
            "Develop actionable solutions or agreements",
            "Confirm next steps and responsibilities"
        ]
        self.conversation_goals = goals
        
        # Initialize conversation
        initial_message = f"""
        🎯 NEW CONVERSATION INITIATED
        
        Topic: {topic}
        Employee1 Context: {employee1_context}
        Employee2 Context: {employee2_context}
        
        Conversation Goals:
        {chr(10).join([f"• {goal}" for goal in goals])}
        
        Maximum Exchanges: {self.max_exchanges}
        Current Exchange: {self.exchange_count + 1}
        
        Let's begin with Employee1's initial perspective on this topic.
        """
        
        self.conversation_history.append({
            'exchange': self.exchange_count + 1,
            'timestamp': datetime.now().isoformat(),
            'role': 'broker',
            'message': initial_message,
            'type': 'conversation_start'
        })
        
        return {
            'conversation_id': self.current_conversation_id,
            'topic': topic,
            'goals': goals,
            'initial_message': initial_message,
            'status': 'started'
        }
    
    def coordinate_exchange(self, employee1_message: str, employee2_message: str) -> Dict:
        """
        Coordinate an exchange between Employee1 and Employee2.
        
        Args:
            employee1_message: Message from Employee1
            employee2_message: Message from Employee2
        
        Returns:
            Dict containing broker's analysis and guidance
        """
        self.exchange_count += 1
        
        if self.exchange_count > self.max_exchanges:
            return self._force_conclusion("Maximum exchanges reached")
        
        # Add messages to history
        self.conversation_history.append({
            'exchange': self.exchange_count,
            'timestamp': datetime.now().isoformat(),
            'role': 'employee1',
            'message': employee1_message,
            'type': 'input'
        })
        
        self.conversation_history.append({
            'exchange': self.exchange_count,
            'timestamp': datetime.now().isoformat(),
            'role': 'employee2',
            'message': employee2_message,
            'type': 'input'
        })
        
        # Analyze the exchange using XAI
        analysis = self._analyze_exchange(employee1_message, employee2_message)
        
        # Add broker's analysis to history
        self.conversation_history.append({
            'exchange': self.exchange_count,
            'timestamp': datetime.now().isoformat(),
            'role': 'broker',
            'message': analysis['broker_guidance'],
            'type': 'coordination'
        })
        
        return {
            'exchange_number': self.exchange_count,
            'analysis': analysis,
            'progress': self._calculate_progress(),
            'remaining_exchanges': self.max_exchanges - self.exchange_count,
            'should_continue': analysis['should_continue']
        }
    
    def _analyze_exchange(self, employee1_message: str, employee2_message: str) -> Dict:
        """
        Analyze the exchange between employees using XAI API.
        """
        prompt = f"""
        {self.broker_personality}
        
        CONVERSATION ANALYSIS REQUEST
        
        Exchange #{self.exchange_count} of {self.max_exchanges}
        
        Employee1 Message: "{employee1_message}"
        Employee2 Message: "{employee2_message}"
        
        Conversation Goals:
        {chr(10).join([f"• {goal}" for goal in self.conversation_goals])}
        
        Previous Exchanges: {self.exchange_count - 1}
        
        Please analyze this exchange and provide:
        1. Key points from each employee
        2. Areas of agreement/disagreement
        3. Progress towards goals
        4. Broker guidance for next steps
        5. Whether conversation should continue or conclude
        
        Respond in JSON format:
        {{
            "key_points": {{
                "employee1": ["point1", "point2"],
                "employee2": ["point1", "point2"]
            }},
            "agreement_areas": ["area1", "area2"],
            "disagreement_areas": ["area1", "area2"],
            "goal_progress": {{
                "goal1": "progress_status",
                "goal2": "progress_status"
            }},
            "broker_guidance": "Clear guidance for next steps",
            "should_continue": true/false,
            "conclusion_reason": "reason if should_continue is false"
        }}
        """
        
        try:
            response = self._call_xai_api(prompt)
            analysis = json.loads(response)
            return analysis
        except Exception as e:
            # Fallback analysis if XAI fails
            return {
                "key_points": {
                    "employee1": ["Message received"],
                    "employee2": ["Message received"]
                },
                "agreement_areas": [],
                "disagreement_areas": [],
                "goal_progress": {},
                "broker_guidance": f"Exchange {self.exchange_count} completed. Continue discussion.",
                "should_continue": True,
                "conclusion_reason": None
            }
    
    def _call_xai_api(self, prompt: str) -> str:
        """
        Make a call to the XAI API.
        """
        headers = {
            "Authorization": f"Bearer {self.xai_api_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "x-1",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"XAI API error: {response.status_code} - {response.text}")
    
    def _calculate_progress(self) -> Dict:
        """
        Calculate progress towards conversation goals.
        """
        if self.exchange_count == 0:
            return {"overall": 0, "goals": {}}
        
        # Simple progress calculation based on exchanges
        overall_progress = min((self.exchange_count / self.max_exchanges) * 100, 100)
        
        goal_progress = {}
        for i, goal in enumerate(self.conversation_goals):
            # Estimate progress based on exchange number
            goal_progress[goal] = min((self.exchange_count / len(self.conversation_goals)) * 100, 100)
        
        return {
            "overall": overall_progress,
            "goals": goal_progress
        }
    
    def _force_conclusion(self, reason: str) -> Dict:
        """
        Force conclusion of conversation when max exchanges reached.
        """
        conclusion_message = f"""
        🔚 CONVERSATION CONCLUDED
        
        Reason: {reason}
        Total Exchanges: {self.exchange_count}
        
        Final Summary:
        - Conversation has reached maximum allowed exchanges
        - Key points have been exchanged
        - Next steps should be determined based on current progress
        
        Recommendation: Schedule follow-up if needed or proceed with current agreements.
        """
        
        self.conversation_history.append({
            'exchange': self.exchange_count,
            'timestamp': datetime.now().isoformat(),
            'role': 'broker',
            'message': conclusion_message,
            'type': 'conclusion'
        })
        
        return {
            'exchange_number': self.exchange_count,
            'analysis': {
                'broker_guidance': conclusion_message,
                'should_continue': False,
                'conclusion_reason': reason
            },
            'progress': self._calculate_progress(),
            'remaining_exchanges': 0,
            'should_continue': False
        }
    
    def get_conversation_summary(self) -> Dict:
        """
        Get a summary of the current conversation.
        """
        return {
            'conversation_id': self.current_conversation_id,
            'total_exchanges': self.exchange_count,
            'max_exchanges': self.max_exchanges,
            'progress': self._calculate_progress(),
            'goals': self.conversation_goals,
            'history': self.conversation_history
        }
    
    def reset_conversation(self):
        """
        Reset the conversation state.
        """
        self.conversation_history = []
        self.current_conversation_id = None
        self.exchange_count = 0
        self.conversation_goals = []

# Example usage
if __name__ == "__main__":
    broker = BrokerAgent()
    
    # Start a conversation
    result = broker.start_conversation(
        topic="Project timeline adjustment",
        employee1_context="Project manager concerned about delays",
        employee2_context="Developer explaining technical constraints"
    )
    
    print("Conversation started:", result['conversation_id'])
    print("Initial message:", result['initial_message']) 
#!/usr/bin/env python3
"""
Employee1 Agent - Communicates with Employee2 through the broker.
Uses XAI API for intelligent, context-aware responses.
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

class Employee1Agent:
    """
    Employee1 agent that communicates with Employee2 through the broker.
    Provides intelligent, context-aware responses using XAI API.
    """
    
    def __init__(self, role: str = "Project Manager", expertise: str = "Project planning and coordination"):
        self.xai_api_token = os.getenv('XAI_API_TOKEN')
        if not self.xai_api_token:
            raise ValueError("XAI_API_TOKEN not found in environment variables")
        
        self.base_url = "https://api.x.ai/v1"
        self.role = role
        self.expertise = expertise
        self.conversation_context = []
        self.personality = self._create_personality()
        
    def _create_personality(self) -> str:
        """
        Create Employee1's personality and communication style.
        """
        return f"""
        You are Employee1, a {self.role} with expertise in {self.expertise}.
        
        Your communication style:
        - Professional and clear
        - Focused on goals and objectives
        - Collaborative and solution-oriented
        - Respectful of others' perspectives
        - Efficient in communication
        
        Your responsibilities:
        - Represent your role and expertise effectively
        - Provide clear, actionable input
        - Listen to and consider Employee2's perspective
        - Work towards mutual understanding and solutions
        - Stay focused on the conversation topic
        
        When responding:
        1. Be concise but comprehensive
        2. Address the specific points raised
        3. Share your perspective based on your role
        4. Ask clarifying questions when needed
        5. Propose solutions or next steps
        6. Acknowledge Employee2's input
        """
    
    def generate_response(self, topic: str, employee2_message: str, conversation_history: List[Dict], 
                         broker_guidance: str = None) -> str:
        """
        Generate a response to Employee2's message using XAI API.
        
        Args:
            topic: The conversation topic
            employee2_message: Message from Employee2
            conversation_history: Previous conversation exchanges
            broker_guidance: Guidance from the broker (optional)
        
        Returns:
            Generated response message
        """
        # Build context from conversation history
        context = self._build_context(conversation_history)
        
        prompt = f"""
        {self.personality}
        
        CONVERSATION CONTEXT:
        Topic: {topic}
        Your Role: {self.role}
        Your Expertise: {self.expertise}
        
        CONVERSATION HISTORY:
        {context}
        
        EMPLOYEE2'S MESSAGE:
        "{employee2_message}"
        
        BROKER GUIDANCE:
        {broker_guidance if broker_guidance else "No specific guidance provided"}
        
        TASK:
        Generate a thoughtful, professional response to Employee2's message. Your response should:
        1. Acknowledge Employee2's points
        2. Share your perspective based on your role
        3. Address any concerns or questions
        4. Propose solutions or next steps
        5. Keep the conversation moving forward efficiently
        
        Respond naturally as Employee1, maintaining your professional communication style.
        Keep your response concise but comprehensive (2-4 sentences).
        """
        
        try:
            response = self._call_xai_api(prompt)
            return response.strip()
        except Exception as e:
            # Fallback response if XAI fails
            return f"I understand your perspective on {topic}. From my role as {self.role}, I'd like to discuss this further and find a solution that works for both of us."
    
    def _build_context(self, conversation_history: List[Dict]) -> str:
        """
        Build context string from conversation history.
        """
        if not conversation_history:
            return "This is the beginning of the conversation."
        
        context_parts = []
        for entry in conversation_history[-6:]:  # Last 6 entries for context
            if entry['role'] in ['employee1', 'employee2']:
                role_name = "You" if entry['role'] == 'employee1' else "Employee2"
                context_parts.append(f"{role_name}: {entry['message']}")
        
        return "\n".join(context_parts) if context_parts else "No previous exchanges."
    
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
            "max_tokens": 500,
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
    
    def provide_initial_perspective(self, topic: str, context: str) -> str:
        """
        Provide initial perspective on a topic.
        
        Args:
            topic: The conversation topic
            context: Additional context about the situation
        
        Returns:
            Initial perspective message
        """
        prompt = f"""
        {self.personality}
        
        INITIAL PERSPECTIVE REQUEST:
        Topic: {topic}
        Context: {context}
        Your Role: {self.role}
        
        Provide your initial perspective on this topic. Consider:
        1. How this topic relates to your role and expertise
        2. Your initial thoughts and concerns
        3. What you hope to achieve from this conversation
        4. Questions you have for Employee2
        
        Keep your response professional and focused (3-5 sentences).
        """
        
        try:
            response = self._call_xai_api(prompt)
            return response.strip()
        except Exception as e:
            return f"As {self.role}, I'd like to discuss {topic} and understand how we can work together effectively on this matter."
    
    def update_context(self, new_context: Dict):
        """
        Update the agent's conversation context.
        """
        self.conversation_context.append({
            'timestamp': datetime.now().isoformat(),
            'context': new_context
        })
    
    def get_agent_info(self) -> Dict:
        """
        Get information about the agent.
        """
        return {
            'name': 'Employee1',
            'role': self.role,
            'expertise': self.expertise,
            'personality': self.personality,
            'conversation_context_count': len(self.conversation_context)
        }

# Example usage
if __name__ == "__main__":
    # Create Employee1 as a Project Manager
    employee1 = Employee1Agent(
        role="Project Manager",
        expertise="Project planning, timeline management, and stakeholder coordination"
    )
    
    # Provide initial perspective
    initial_perspective = employee1.provide_initial_perspective(
        topic="Project timeline adjustment",
        context="The development team needs more time for a critical feature"
    )
    
    print("Employee1 Initial Perspective:")
    print(initial_perspective)
    
    # Generate response to Employee2
    response = employee1.generate_response(
        topic="Project timeline adjustment",
        employee2_message="We need an additional 2 weeks for the authentication module due to security requirements.",
        conversation_history=[],
        broker_guidance="Focus on understanding the technical constraints and finding a solution."
    )
    
    print("\nEmployee1 Response:")
    print(response) 
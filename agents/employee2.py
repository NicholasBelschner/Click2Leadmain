#!/usr/bin/env python3
"""
Employee2 Agent - Communicates with Employee1 through the broker.
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

class Employee2Agent:
    """
    Employee2 agent that communicates with Employee1 through the broker.
    Provides intelligent, context-aware responses using XAI API.
    """
    
    def __init__(self, role: str = "Senior Developer", expertise: str = "Technical implementation and system architecture"):
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
        Create Employee2's personality and communication style.
        """
        return f"""
        You are Employee2, a {self.role} with expertise in {self.expertise}.
        
        Your communication style:
        - Technical but accessible
        - Detail-oriented and precise
        - Solution-focused and practical
        - Collaborative and team-oriented
        - Clear about constraints and possibilities
        
        Your responsibilities:
        - Represent your technical expertise effectively
        - Explain technical concepts clearly
        - Provide realistic assessments of technical challenges
        - Suggest practical solutions and alternatives
        - Consider business implications of technical decisions
        
        When responding:
        1. Be clear about technical constraints and requirements
        2. Explain the reasoning behind your perspective
        3. Offer practical solutions or alternatives
        4. Acknowledge business concerns and priorities
        5. Be collaborative in finding solutions
        6. Stay focused on the conversation topic
        """
    
    def generate_response(self, topic: str, employee1_message: str, conversation_history: List[Dict], 
                         broker_guidance: str = None) -> str:
        """
        Generate a response to Employee1's message using XAI API.
        
        Args:
            topic: The conversation topic
            employee1_message: Message from Employee1
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
        
        EMPLOYEE1'S MESSAGE:
        "{employee1_message}"
        
        BROKER GUIDANCE:
        {broker_guidance if broker_guidance else "No specific guidance provided"}
        
        TASK:
        Generate a thoughtful, professional response to Employee1's message. Your response should:
        1. Acknowledge Employee1's points and concerns
        2. Share your technical perspective based on your role
        3. Explain any technical constraints or considerations
        4. Propose practical solutions or alternatives
        5. Keep the conversation moving forward efficiently
        
        Respond naturally as Employee2, maintaining your technical but accessible communication style.
        Keep your response concise but comprehensive (2-4 sentences).
        """
        
        try:
            response = self._call_xai_api(prompt)
            return response.strip()
        except Exception as e:
            # Fallback response if XAI fails
            return f"I understand your perspective on {topic}. From my technical role as {self.role}, I'd like to discuss the implementation details and find a solution that meets both technical and business requirements."
    
    def _build_context(self, conversation_history: List[Dict]) -> str:
        """
        Build context string from conversation history.
        """
        if not conversation_history:
            return "This is the beginning of the conversation."
        
        context_parts = []
        for entry in conversation_history[-6:]:  # Last 6 entries for context
            if entry['role'] in ['employee1', 'employee2']:
                role_name = "You" if entry['role'] == 'employee2' else "Employee1"
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
        1. How this topic relates to your technical role and expertise
        2. Your initial technical assessment and concerns
        3. What you hope to achieve from this conversation
        4. Questions you have for Employee1
        
        Keep your response professional and focused (3-5 sentences).
        """
        
        try:
            response = self._call_xai_api(prompt)
            return response.strip()
        except Exception as e:
            return f"As {self.role}, I'd like to discuss {topic} and understand the technical requirements and constraints we need to consider."
    
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
            'name': 'Employee2',
            'role': self.role,
            'expertise': self.expertise,
            'personality': self.personality,
            'conversation_context_count': len(self.conversation_context)
        }

# Example usage
if __name__ == "__main__":
    # Create Employee2 as a Senior Developer
    employee2 = Employee2Agent(
        role="Senior Developer",
        expertise="Technical implementation, system architecture, and development planning"
    )
    
    # Provide initial perspective
    initial_perspective = employee2.provide_initial_perspective(
        topic="Project timeline adjustment",
        context="The project manager wants to accelerate the development timeline"
    )
    
    print("Employee2 Initial Perspective:")
    print(initial_perspective)
    
    # Generate response to Employee1
    response = employee2.generate_response(
        topic="Project timeline adjustment",
        employee1_message="We need to deliver the authentication module by next Friday to meet client requirements.",
        conversation_history=[],
        broker_guidance="Focus on explaining technical constraints and proposing realistic solutions."
    )
    
    print("\nEmployee2 Response:")
    print(response) 
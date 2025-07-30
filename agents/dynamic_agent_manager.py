#!/usr/bin/env python3
"""
Dynamic Agent Manager
Creates and manages agents dynamically based on user specifications
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv

load_dotenv()

class DynamicAgentManager:
    def __init__(self):
        self.xai_api_token = os.getenv('XAI_API_TOKEN')
        if not self.xai_api_token:
            raise ValueError("XAI_API_TOKEN not found in environment variables")
        self.base_url = "https://api.x.ai/v1"
        self.agents = {}  # Store created agents
        self.agent_counter = 0
        
    def create_agent(self, role: str, expertise: str, personality_traits: List[str] = None) -> Dict:
        """
        Create a new agent with specified role, expertise, and personality traits
        """
        agent_id = f"agent_{self.agent_counter}"
        self.agent_counter += 1
        
        # Create agent personality
        personality = self._create_agent_personality(role, expertise, personality_traits)
        
        # Create agent instance
        agent = {
            'id': agent_id,
            'role': role,
            'expertise': expertise,
            'personality': personality,
            'conversation_context': [],
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.agents[agent_id] = agent
        return agent
    
    def _create_agent_personality(self, role: str, expertise: str, personality_traits: List[str] = None) -> str:
        """
        Generate a personality for the agent using XAI API
        """
        if personality_traits is None:
            personality_traits = []
        
        prompt = f"""Create a professional personality for an AI agent with the following specifications:

Role: {role}
Expertise: {expertise}
Personality Traits: {', '.join(personality_traits) if personality_traits else 'Professional, collaborative, knowledgeable'}

Please create a detailed personality description that includes:
1. Professional background and experience
2. Communication style and approach
3. Key strengths and areas of expertise
4. How they typically approach problems and collaboration
5. Their role in team discussions and decision-making

Make it realistic, professional, and suitable for workplace conversations. Keep it concise but comprehensive."""

        try:
            response = self._call_xai_api(prompt)
            return response.strip()
        except Exception as e:
            # Enhanced fallback personality if API call fails
            fallback_personalities = {
                'Product Manager': f"A seasoned Product Manager with expertise in {expertise}. Known for strategic thinking, excellent communication skills, and ability to bridge technical and business requirements. Collaborative leader who focuses on user needs and market opportunities.",
                'Developer': f"A skilled Developer specializing in {expertise}. Technical problem-solver with attention to detail and passion for clean, efficient code. Values collaboration and enjoys explaining complex technical concepts in accessible terms.",
                'Designer': f"A creative Designer with expertise in {expertise}. User-centered approach with strong visual and interaction design skills. Collaborative team player who advocates for user experience and design consistency.",
                'Marketing Manager': f"A strategic Marketing Manager with expertise in {expertise}. Data-driven decision maker with strong analytical skills and creative thinking. Excellent communicator who understands both customer needs and business objectives.",
                'Data Analyst': f"A detail-oriented Data Analyst specializing in {expertise}. Strong analytical and statistical skills with ability to translate complex data into actionable insights. Collaborative team member who helps drive data-informed decisions.",
                'Project Manager': f"An experienced Project Manager with expertise in {expertise}. Organized and methodical approach with strong leadership and communication skills. Focuses on delivering results while maintaining team collaboration and stakeholder satisfaction."
            }
            
            # Try to find a matching personality
            for key, personality in fallback_personalities.items():
                if key.lower() in role.lower():
                    return personality
            
            # Generic fallback
            return f"A professional {role} with expertise in {expertise}. Collaborative, knowledgeable, and focused on achieving results through effective communication and problem-solving. Brings valuable perspective to team discussions and decision-making processes."
    
    def create_multiple_agents(self, agent_specifications: List[Dict]) -> List[Dict]:
        """
        Create multiple agents based on specifications
        """
        created_agents = []
        for spec in agent_specifications:
            agent = self.create_agent(
                role=spec.get('role', 'Team Member'),
                expertise=spec.get('expertise', 'General'),
                personality_traits=spec.get('personality_traits', [])
            )
            created_agents.append(agent)
        
        return created_agents
    
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """
        Get agent by ID
        """
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[Dict]:
        """
        Get all created agents
        """
        return list(self.agents.values())
    
    def update_agent(self, agent_id: str, updates: Dict) -> bool:
        """
        Update agent properties
        """
        if agent_id in self.agents:
            self.agents[agent_id].update(updates)
            return True
        return False
    
    def delete_agent(self, agent_id: str) -> bool:
        """
        Delete an agent
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False
    
    def generate_agent_response(self, agent_id: str, topic: str, context: str, 
                               other_agents_messages: List[str] = None) -> str:
        """
        Generate a response from a specific agent
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return "Agent not found."
        
        # Build context for the agent
        context_parts = [
            f"You are {agent['role']} with expertise in {agent['expertise']}.",
            f"Your personality: {agent['personality']}",
            f"Current topic: {topic}",
            f"Context: {context}"
        ]
        
        if other_agents_messages:
            context_parts.append("Recent messages from other team members:")
            for i, msg in enumerate(other_agents_messages[-3:], 1):  # Last 3 messages
                context_parts.append(f"{i}. {msg}")
        
        context_parts.append("\nPlease provide your professional perspective on this topic, considering your role and expertise.")
        
        prompt = "\n".join(context_parts)
        
        try:
            response = self._call_xai_api(prompt)
            return response.strip()
        except Exception as e:
            # Enhanced fallback responses based on agent role
            role = agent['role'].lower()
            expertise = agent['expertise'].lower()
            
            if 'product' in role or 'manager' in role:
                return f"As a {agent['role']}, I believe we should approach this {topic} systematically. From my expertise in {expertise}, I see several key considerations we need to address. We should focus on user needs, market opportunities, and ensuring our solution aligns with business objectives. What are your thoughts on the technical feasibility and timeline?"
            
            elif 'developer' in role or 'technical' in role or 'engineer' in role:
                return f"From a technical perspective on {topic}, I can see both opportunities and challenges. My expertise in {expertise} suggests we need to consider implementation complexity, scalability, and maintainability. I'd recommend we start with a proof of concept to validate our approach. How does this align with your strategic vision?"
            
            elif 'designer' in role or 'ux' in role or 'creative' in role:
                return f"As a {agent['role']}, I'm excited about the {topic} opportunity. My expertise in {expertise} tells me we need to prioritize user experience and design consistency. I suggest we conduct user research to understand pain points and create intuitive solutions. How can we balance user needs with technical constraints?"
            
            elif 'marketing' in role or 'analyst' in role or 'data' in role:
                return f"Looking at {topic} through the lens of {expertise}, I see several data points we should consider. We need to understand our target audience, measure performance metrics, and optimize based on results. I recommend we establish clear KPIs and track progress systematically. What are your thoughts on the strategic direction?"
            
            else:
                return f"As a {agent['role']} with expertise in {expertise}, I have some valuable insights on {topic}. I believe we should consider multiple perspectives and ensure our approach is well-rounded. Collaboration will be key to success here. What aspects should we prioritize first?"
    
    def _call_xai_api(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Make API call to XAI
        """
        headers = {
            "Authorization": f"Bearer {self.xai_api_token}",
            "Content-Type": "application/json"
        }
        
        # Try different model names
        models_to_try = ["x-1", "x-2", "x-3", "grok-beta"]
        
        for model in models_to_try:
            try:
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
                
                response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
                
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                elif response.status_code == 404:
                    # Model not found, try next one
                    continue
                else:
                    raise Exception(f"XAI API error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                if "404" in str(e) and "model" in str(e).lower():
                    continue
                else:
                    raise e
        
        # If all models fail, raise an exception to trigger fallback responses
        raise Exception("XAI API not available - using fallback responses")
    
    def save_agents_to_file(self, filename: str = None) -> str:
        """
        Save all agents to a JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agents_backup_{timestamp}.json"
        
        data = {
            'agents': self.agents,
            'agent_counter': self.agent_counter,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def load_agents_from_file(self, filename: str) -> bool:
        """
        Load agents from a JSON file
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.agents = data.get('agents', {})
            self.agent_counter = data.get('agent_counter', 0)
            return True
        except Exception as e:
            print(f"Error loading agents: {e}")
            return False

class AgentSpecificationHelper:
    """
    Helper class to assist users in specifying agents
    """
    
    def __init__(self, xai_api_token: str):
        self.xai_api_token = xai_api_token
        self.base_url = "https://api.x.ai/v1"
    
    def suggest_agent_roles(self, topic: str, context: str) -> List[Dict]:
        """
        Suggest appropriate agent roles for a given topic
        """
        prompt = f"""Given the following topic and context, suggest 3-5 appropriate agent roles that would be valuable for this discussion:

Topic: {topic}
Context: {context}

For each role, provide:
1. Role title
2. Key expertise areas
3. Why this role is important for this topic

Format your response as a JSON array of objects with 'role', 'expertise', and 'reasoning' fields."""

        try:
            response = self._call_xai_api(prompt, max_tokens=800)
            # Try to parse JSON response
            try:
                suggestions = json.loads(response)
                return suggestions
            except json.JSONDecodeError:
                # If JSON parsing fails, return a default suggestion
                return [
                    {
                        'role': 'Project Manager',
                        'expertise': 'Project planning and coordination',
                        'reasoning': 'To oversee the overall discussion and ensure objectives are met'
                    },
                    {
                        'role': 'Technical Specialist',
                        'expertise': 'Technical implementation and feasibility',
                        'reasoning': 'To provide technical insights and address implementation concerns'
                    }
                ]
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            return []
    
    def validate_agent_specification(self, role: str, expertise: str) -> Dict:
        """
        Validate and enhance agent specification
        """
        prompt = f"""Please validate and enhance this agent specification:

Role: {role}
Expertise: {expertise}

Provide feedback on:
1. Is this role clear and specific enough?
2. Are there any missing expertise areas?
3. What personality traits would work well for this role?
4. Any suggestions for improvement?

Format as JSON with 'is_valid', 'suggestions', 'enhanced_role', 'enhanced_expertise', and 'personality_traits' fields."""

        try:
            response = self._call_xai_api(prompt, max_tokens=600)
            try:
                validation = json.loads(response)
                return validation
            except json.JSONDecodeError:
                return {
                    'is_valid': True,
                    'suggestions': 'Specification looks good',
                    'enhanced_role': role,
                    'enhanced_expertise': expertise,
                    'personality_traits': ['Professional', 'Collaborative']
                }
        except Exception as e:
            return {
                'is_valid': True,
                'suggestions': 'Unable to validate due to API error',
                'enhanced_role': role,
                'enhanced_expertise': expertise,
                'personality_traits': ['Professional', 'Collaborative']
            }
    
    def _call_xai_api(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Make API call to XAI
        """
        headers = {
            "Authorization": f"Bearer {self.xai_api_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "x-1",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"XAI API error: {response.status_code} - {response.text}")

# Example usage and testing
if __name__ == "__main__":
    try:
        # Initialize the dynamic agent manager
        manager = DynamicAgentManager()
        helper = AgentSpecificationHelper(manager.xai_api_token)
        
        print("✅ Dynamic Agent Manager initialized successfully!")
        print(f"XAI API Token: {'*' * 20}{manager.xai_api_token[-4:]}")
        
        # Example: Create a few agents
        agents = manager.create_multiple_agents([
            {'role': 'Product Manager', 'expertise': 'Product strategy and user experience'},
            {'role': 'Senior Developer', 'expertise': 'Technical architecture and implementation'},
            {'role': 'UX Designer', 'expertise': 'User interface design and user research'}
        ])
        
        print(f"\n✅ Created {len(agents)} agents:")
        for agent in agents:
            print(f"  - {agent['role']} (ID: {agent['id']})")
        
        # Example: Get suggestions for a topic
        suggestions = helper.suggest_agent_roles(
            "Redesigning the user onboarding flow",
            "Current drop-off rate is 40%, need to improve user retention"
        )
        
        print(f"\n📋 Suggested roles for onboarding redesign:")
        for suggestion in suggestions:
            print(f"  - {suggestion['role']}: {suggestion['expertise']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure XAI_API_TOKEN is set in your .env file") 
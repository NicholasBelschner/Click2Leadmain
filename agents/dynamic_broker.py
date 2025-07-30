#!/usr/bin/env python3
"""
Dynamic Broker Agent
Handles conversations with any number of dynamically created agents
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv

from .dynamic_agent_manager import DynamicAgentManager, AgentSpecificationHelper

load_dotenv()

class DynamicBrokerAgent:
    def __init__(self):
        self.xai_api_token = os.getenv('XAI_API_TOKEN')
        if not self.xai_api_token:
            raise ValueError("XAI_API_TOKEN not found in environment variables")
        self.base_url = "https://api.x.ai/v1"
        
        # Initialize dynamic agent manager
        self.agent_manager = DynamicAgentManager()
        self.helper = AgentSpecificationHelper(self.xai_api_token)
        
        # Conversation state
        self.conversation_history = []
        self.current_conversation_id = None
        self.exchange_count = 0
        self.max_exchanges = 6
        self.conversation_goals = []
        self.active_agents = []
        
        # Broker personality
        self.broker_personality = """You are an intelligent conversation broker and facilitator. Your role is to:

1. **Coordinate Multi-Agent Conversations**: Manage discussions between any number of agents, ensuring everyone has a chance to contribute meaningfully.

2. **Agent Creation and Management**: When users want to start a conversation but haven't specified agents, help them create appropriate agents by:
   - Asking clarifying questions about the topic and context
   - Suggesting relevant agent roles and expertise
   - Creating agents dynamically using AI
   - Ensuring the right mix of perspectives for the discussion

3. **Conversation Facilitation**: 
   - Keep discussions focused and productive
   - Ensure balanced participation from all agents
   - Summarize key points and progress
   - Guide conversations toward actionable conclusions

4. **Problem Solving**: Help users identify what types of agents they need for their specific use case and create them accordingly.

You are professional, helpful, and focused on creating valuable multi-agent conversations."""
    
    def start_conversation(self, topic: str, context: str = "", agent_specifications: List[Dict] = None) -> Dict:
        """
        Start a new conversation with specified or dynamically created agents
        """
        conversation_id = f"conv_{int(time.time())}"
        self.current_conversation_id = conversation_id
        self.exchange_count = 0
        
        # Set conversation goals
        self.conversation_goals = [
            f"Discuss and analyze: {topic}",
            "Ensure all agents contribute meaningfully",
            "Reach actionable conclusions",
            "Maintain productive dialogue"
        ]
        
        # Handle agent creation
        if agent_specifications:
            # Create agents from specifications
            created_agents = self.agent_manager.create_multiple_agents(agent_specifications)
            self.active_agents = created_agents
            agent_creation_message = f"Created {len(created_agents)} agents for this conversation."
        else:
            # No agents specified - need to create them dynamically
            return self._handle_agent_creation_request(topic, context)
        
        # Initialize conversation
        conversation_data = {
            'conversation_id': conversation_id,
            'topic': topic,
            'context': context,
            'agents': self.active_agents,
            'start_time': datetime.now().isoformat(),
            'goals': self.conversation_goals,
            'status': 'active'
        }
        
        self.conversation_history.append(conversation_data)
        
        # Generate initial broker message
        initial_message = self._generate_initial_message(topic, context, self.active_agents)
        
        return {
            'conversation_id': conversation_id,
            'status': 'started',
            'agents_created': len(self.active_agents),
            'broker_message': initial_message,
            'agents': self.active_agents
        }
    
    def _handle_agent_creation_request(self, topic: str, context: str) -> Dict:
        """
        Handle the case where no agents are specified - prompt user for agent creation
        """
        # Get suggestions for appropriate agents
        suggestions = self.helper.suggest_agent_roles(topic, context)
        
        # Create a detailed prompt for the user
        prompt = f"""I'd be happy to help you start a conversation about "{topic}". 

To create the most effective discussion, I need to know what types of agents would be most valuable for this topic.

**Topic**: {topic}
**Context**: {context}

**Suggested Agent Roles** (based on your topic):
"""
        
        for i, suggestion in enumerate(suggestions, 1):
            prompt += f"""
{i}. **{suggestion['role']}**
   - Expertise: {suggestion['expertise']}
   - Why needed: {suggestion['reasoning']}
"""
        
        prompt += f"""

**Please specify how many agents you'd like and their roles:**

You can either:
1. **Use my suggestions**: Tell me which of the above roles you want (e.g., "Create agents 1, 3, and 5")
2. **Custom roles**: Specify your own roles and expertise (e.g., "Create a Marketing Manager and Data Analyst")
3. **Quick start**: Just tell me how many agents you want and I'll create appropriate ones

**Examples:**
- "Create 3 agents: Product Manager, Developer, and Designer"
- "I want 2 agents: one for strategy and one for technical implementation"
- "Just create 4 agents for this discussion"

What would you prefer?"""
        
        return {
            'conversation_id': None,
            'status': 'needs_agents',
            'message': prompt,
            'suggestions': suggestions,
            'topic': topic,
            'context': context
        }
    
    def create_agents_from_user_specification(self, user_specification: str, topic: str, context: str) -> Dict:
        """
        Create agents based on user's specification
        """
        try:
            # Parse user specification using AI
            agent_specs = self._parse_user_agent_specification(user_specification, topic, context)
            
            # Create the agents
            created_agents = self.agent_manager.create_multiple_agents(agent_specs)
            self.active_agents = created_agents
            
            # Now start the actual conversation
            return self.start_conversation(topic, context, agent_specs)
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error creating agents: {str(e)}. Please try again with a clearer specification."
            }
    
    def _parse_user_agent_specification(self, user_spec: str, topic: str, context: str) -> List[Dict]:
        """
        Parse user specification to extract agent roles and expertise
        """
        prompt = f"""Parse the following user specification to extract agent roles and expertise. Return a JSON array of agent specifications.

User specification: "{user_spec}"
Topic: {topic}
Context: {context}

Examples:

User: "Create 3 agents: Product Manager, Developer, and Designer"
Output: [
    {{"role": "Product Manager", "expertise": "Product strategy and project management"}},
    {{"role": "Developer", "expertise": "Technical implementation and coding"}},
    {{"role": "Designer", "expertise": "User interface and user experience design"}}
]

User: "I want a Marketing Manager and Data Analyst"
Output: [
    {{"role": "Marketing Manager", "expertise": "Marketing strategy and campaign management"}},
    {{"role": "Data Analyst", "expertise": "Data analysis and insights"}}
]

User: "Just create 2 agents for strategy and technical"
Output: [
    {{"role": "Strategy Specialist", "expertise": "Strategic planning and business analysis"}},
    {{"role": "Technical Specialist", "expertise": "Technical implementation and feasibility"}}
]

User: "I would like 3 employees working for me. I would like one to be in charge of my workouts and then another to be in charge of my nutrition I am eating/drinking, and then another to make sure that the workouts align with my nutrients and my nutrients aligns with my workouts"
Output: [
    {{"role": "Workout Specialist", "expertise": "Fitness training and exercise program design"}},
    {{"role": "Nutrition Specialist", "expertise": "Nutrition planning and dietary optimization"}},
    {{"role": "Fitness Coordinator", "expertise": "Integration of workouts and nutrition for optimal performance"}}
]

Please parse the user specification and return only the JSON array."""

        try:
            response = self._call_xai_api(prompt, max_tokens=800)
            # Try to parse JSON response
            try:
                agent_specs = json.loads(response)
                return agent_specs
            except json.JSONDecodeError:
                # Fallback: try to extract number of agents from user spec
                return self._extract_agents_from_fallback(user_spec, topic, context)
        except Exception as e:
            # Fallback: try to extract number of agents from user spec
            return self._extract_agents_from_fallback(user_spec, topic, context)
    
    def _extract_agents_from_fallback(self, user_spec: str, topic: str, context: str) -> List[Dict]:
        """
        Fallback method to extract agent specifications when XAI API fails
        """
        user_spec_lower = user_spec.lower()
        
        # Try to extract number of agents
        agent_count = 2  # default
        if "3 employees" in user_spec_lower or "3 agents" in user_spec_lower:
            agent_count = 3
        elif "4 employees" in user_spec_lower or "4 agents" in user_spec_lower:
            agent_count = 4
        elif "5 employees" in user_spec_lower or "5 agents" in user_spec_lower:
            agent_count = 5
        
        # Try to extract specific roles from the text
        agents = []
        
        # Check for fitness/nutrition related roles
        if "workout" in user_spec_lower or "fitness" in user_spec_lower:
            agents.append({"role": "Workout Specialist", "expertise": "Fitness training and exercise program design"})
        
        if "nutrition" in user_spec_lower or "eating" in user_spec_lower or "drinking" in user_spec_lower:
            agents.append({"role": "Nutrition Specialist", "expertise": "Nutrition planning and dietary optimization"})
        
        if "align" in user_spec_lower or "coordinate" in user_spec_lower or "coordination" in user_spec_lower:
            agents.append({"role": "Fitness Coordinator", "expertise": "Integration of workouts and nutrition for optimal performance"})
        
        # Check for business/technical roles
        if "product" in user_spec_lower and "manager" in user_spec_lower:
            agents.append({"role": "Product Manager", "expertise": "Product strategy and project management"})
        
        if "developer" in user_spec_lower or "technical" in user_spec_lower:
            agents.append({"role": "Developer", "expertise": "Technical implementation and coding"})
        
        if "designer" in user_spec_lower or "design" in user_spec_lower:
            agents.append({"role": "Designer", "expertise": "User interface and user experience design"})
        
        if "marketing" in user_spec_lower:
            agents.append({"role": "Marketing Manager", "expertise": "Marketing strategy and campaign management"})
        
        if "data" in user_spec_lower and "analyst" in user_spec_lower:
            agents.append({"role": "Data Analyst", "expertise": "Data analysis and insights"})
        
        # If we found specific roles, use them
        if agents:
            return agents[:agent_count]  # Limit to requested number
        
        # Otherwise create generic agents
        generic_roles = ["Team Member 1", "Team Member 2", "Team Member 3", "Team Member 4", "Team Member 5"]
        return [{"role": generic_roles[i], "expertise": "General expertise"} for i in range(agent_count)]
    
    def conduct_exchange(self) -> Dict:
        """
        Conduct one exchange between all active agents
        """
        if not self.active_agents:
            return {
                'status': 'error',
                'message': 'No active agents. Please create agents first.'
            }
        
        if self.exchange_count >= self.max_exchanges:
            return self._force_conclusion()
        
        self.exchange_count += 1
        
        # Collect responses from all agents
        agent_responses = []
        for agent in self.active_agents:
            # Get recent messages from other agents for context
            other_messages = [resp['message'] for resp in agent_responses]
            
            response = self.agent_manager.generate_agent_response(
                agent['id'],
                self.conversation_history[-1]['topic'],
                self.conversation_history[-1]['context'],
                other_messages
            )
            
            agent_responses.append({
                'agent_id': agent['id'],
                'agent_role': agent['role'],
                'message': response,
                'timestamp': datetime.now().isoformat()
            })
        
        # Generate broker analysis
        broker_analysis = self._analyze_exchange(agent_responses)
        
        # Add to conversation history
        exchange_data = {
            'exchange_number': self.exchange_count,
            'agent_responses': agent_responses,
            'broker_analysis': broker_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'exchanges' not in self.conversation_history[-1]:
            self.conversation_history[-1]['exchanges'] = []
        self.conversation_history[-1]['exchanges'].append(exchange_data)
        
        return {
            'exchange_number': self.exchange_count,
            'agent_responses': agent_responses,
            'broker_analysis': broker_analysis,
            'progress': self._calculate_progress(),
            'status': 'exchange_completed'
        }
    
    def _generate_initial_message(self, topic: str, context: str, agents: List[Dict]) -> str:
        """
        Generate initial broker message
        """
        agent_list = "\n".join([f"- {agent['role']} (Expertise: {agent['expertise']})" for agent in agents])
        
        prompt = f"""You are starting a new multi-agent conversation. Generate a brief, professional opening message.

**Topic**: {topic}
**Context**: {context}
**Participants**:
{agent_list}

Your message should:
1. Welcome all participants
2. Briefly state the topic and objectives
3. Set a collaborative tone
4. Invite the first round of perspectives

Keep it concise and professional."""

        try:
            response = self._call_xai_api(prompt, max_tokens=300)
            return response.strip()
        except Exception as e:
            # Fallback initial message
            return f"Welcome everyone! We're here to discuss {topic}. {context} I'm excited to hear perspectives from our team: {', '.join([agent['role'] for agent in agents])}. Let's begin with your initial thoughts on this topic."
    
    def _analyze_exchange(self, agent_responses: List[Dict]) -> str:
        """
        Analyze the exchange and provide broker insights
        """
        responses_text = "\n\n".join([
            f"{resp['agent_role']}: {resp['message']}" 
            for resp in agent_responses
        ])
        
        prompt = f"""As a conversation broker, analyze this exchange between agents and provide insights:

**Exchange #{self.exchange_count}**

{responses_text}

Please provide a brief analysis that includes:
1. Key points raised by each agent
2. Areas of agreement or disagreement
3. Progress toward conversation goals
4. Suggestions for next steps

Keep it concise and actionable."""

        try:
            response = self._call_xai_api(prompt, max_tokens=400)
            return response.strip()
        except Exception as e:
            # Fallback analysis
            agent_names = [resp['agent_role'] for resp in agent_responses]
            return f"Excellent exchange! {', '.join(agent_names)} have provided valuable perspectives. I see good collaboration and thoughtful insights. Let's continue building on these ideas in our next exchange."
    
    def _calculate_progress(self) -> Dict:
        """
        Calculate conversation progress
        """
        progress_percentage = (self.exchange_count / self.max_exchanges) * 100
        return {
            'exchanges_completed': self.exchange_count,
            'max_exchanges': self.max_exchanges,
            'progress_percentage': progress_percentage,
            'remaining_exchanges': self.max_exchanges - self.exchange_count
        }
    
    def _force_conclusion(self) -> Dict:
        """
        Force conversation conclusion when max exchanges reached
        """
        prompt = f"""The conversation has reached the maximum number of exchanges ({self.max_exchanges}). 

Please provide a comprehensive conclusion that includes:
1. Summary of key points discussed
2. Main decisions or agreements reached
3. Action items or next steps
4. Overall assessment of the conversation's effectiveness

Topic: {self.conversation_history[-1]['topic']}"""

        try:
            conclusion = self._call_xai_api(prompt, max_tokens=500)
            
            # Update conversation status
            self.conversation_history[-1]['status'] = 'completed'
            self.conversation_history[-1]['conclusion'] = conclusion
            self.conversation_history[-1]['end_time'] = datetime.now().isoformat()
            
            return {
                'status': 'concluded',
                'conclusion': conclusion,
                'total_exchanges': self.exchange_count,
                'agents_participated': len(self.active_agents)
            }
        except Exception as e:
            return {
                'status': 'concluded',
                'conclusion': 'Conversation concluded. Thank you all for your participation.',
                'total_exchanges': self.exchange_count,
                'agents_participated': len(self.active_agents)
            }
    
    def get_conversation_summary(self) -> Dict:
        """
        Get summary of current conversation
        """
        if not self.conversation_history:
            return {'status': 'no_conversation'}
        
        current_conv = self.conversation_history[-1]
        return {
            'conversation_id': current_conv['conversation_id'],
            'topic': current_conv['topic'],
            'status': current_conv['status'],
            'agents_count': len(self.active_agents),
            'exchanges_completed': self.exchange_count,
            'max_exchanges': self.max_exchanges,
            'agents': self.active_agents
        }
    
    def reset_conversation(self):
        """
        Reset conversation state
        """
        self.conversation_history = []
        self.current_conversation_id = None
        self.exchange_count = 0
        self.active_agents = []
    
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

# Example usage and testing
if __name__ == "__main__":
    try:
        broker = DynamicBrokerAgent()
        print("✅ Dynamic Broker Agent initialized successfully!")
        
        # Test agent creation request
        result = broker.start_conversation(
            topic="Redesigning the user onboarding flow",
            context="Current drop-off rate is 40%, need to improve user retention"
        )
        
        print(f"\n📋 Broker Response:")
        print(f"Status: {result['status']}")
        if result['status'] == 'needs_agents':
            print(f"Message: {result['message'][:200]}...")
            print(f"Suggestions: {len(result['suggestions'])} agent roles suggested")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure XAI_API_TOKEN is set in your .env file") 
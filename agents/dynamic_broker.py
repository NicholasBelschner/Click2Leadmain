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
from .grok_protocol import GrokProtocol

load_dotenv()

class DynamicBrokerAgent:
    def __init__(self):
        self.xai_api_token = os.getenv('XAI_API_TOKEN')
        if not self.xai_api_token:
            raise ValueError("XAI_API_TOKEN not found in environment variables")
        self.base_url = "https://api.x.ai/v1"
        
        # Initialize dynamic agent manager and Grok protocol
        self.agent_manager = DynamicAgentManager()
        self.helper = AgentSpecificationHelper(self.xai_api_token)
        self.grok_protocol = GrokProtocol()
        
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
        Parse user specification to extract agent roles and expertise using XAI
        """
        prompt = f"""You are an expert at creating AI agent teams. Parse the following user specification to extract agent roles and expertise. Return ONLY a valid JSON array of agent specifications.

User specification: "{user_spec}"
Topic: {topic}
Context: {context}

**Instructions:**
1. Analyze the user's request carefully
2. Identify all the different roles/agents they want
3. Create appropriate expertise descriptions for each role
4. Return ONLY the JSON array, no other text

**Examples:**

User: "Create 3 agents: Product Manager, Developer, and Designer"
Output: [{{"role": "Product Manager", "expertise": "Product strategy and project management"}}, {{"role": "Developer", "expertise": "Technical implementation and coding"}}, {{"role": "Designer", "expertise": "User interface and user experience design"}}]

User: "I want a Marketing Manager and Data Analyst"
Output: [{{"role": "Marketing Manager", "expertise": "Marketing strategy and campaign management"}}, {{"role": "Data Analyst", "expertise": "Data analysis and insights"}}]

User: "Just create 2 agents for strategy and technical"
Output: [{{"role": "Strategy Specialist", "expertise": "Strategic planning and business analysis"}}, {{"role": "Technical Specialist", "expertise": "Technical implementation and feasibility"}}]

User: "create two agents for tracking: one for nutrients and another for workouts"
Output: [{{"role": "Nutrition Specialist", "expertise": "Nutrition tracking and dietary optimization"}}, {{"role": "Workout Specialist", "expertise": "Fitness tracking and exercise program design"}}]

User: "I need a cook, a fitness trainer, and a friend"
Output: [{{"role": "Chef", "expertise": "Cooking and meal preparation"}}, {{"role": "Fitness Trainer", "expertise": "Exercise and fitness training"}}, {{"role": "Personal Friend", "expertise": "Emotional support and companionship"}}]

User: "Create agents for investigation: detective, analyst, and researcher"
Output: [{{"role": "Detective", "expertise": "Investigation and evidence gathering"}}, {{"role": "Analyst", "expertise": "Data analysis and pattern recognition"}}, {{"role": "Researcher", "expertise": "Research and information gathering"}}]

User: "I want agents for my business: sales, marketing, and customer service"
Output: [{{"role": "Sales Specialist", "expertise": "Sales strategy and customer acquisition"}}, {{"role": "Marketing Specialist", "expertise": "Marketing campaigns and brand management"}}, {{"role": "Customer Service Specialist", "expertise": "Customer support and relationship management"}}]

Now parse this user specification and return ONLY the JSON array:"""

        try:
            # Use Grok protocol for better parsing
            response = self.grok_protocol._call_xai_grok_api(prompt, max_tokens=1000)
            
            # Try to parse JSON response
            try:
                # Clean the response to extract just the JSON
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]
                response = response.strip()
                
                agent_specs = json.loads(response)
                
                # Validate the response structure
                if isinstance(agent_specs, list) and all(isinstance(agent, dict) and 'role' in agent and 'expertise' in agent for agent in agent_specs):
                    return agent_specs
                else:
                    raise ValueError("Invalid response structure")
                    
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parsing failed: {e}")
                print(f"Response was: {response}")
                # Fallback to intelligent parsing
                return self._extract_agents_intelligently(user_spec, topic, context)
                
        except Exception as e:
            print(f"XAI API call failed: {e}")
            # Fallback to intelligent parsing
            return self._extract_agents_intelligently(user_spec, topic, context)
    
    def _extract_agents_intelligently(self, user_spec: str, topic: str, context: str) -> List[Dict]:
        """
        Intelligent fallback method to extract agent specifications when XAI API fails
        """
        user_spec_lower = user_spec.lower()
        
        # Try to extract number of agents
        agent_count = 2  # default
        number_patterns = [
            ("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5),
            ("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)
        ]
        
        for pattern, count in number_patterns:
            if pattern in user_spec_lower:
                agent_count = count
                break
        
        # Also check for explicit agent counts
        if "3 agents" in user_spec_lower or "three agents" in user_spec_lower:
            agent_count = 3
        elif "4 agents" in user_spec_lower or "four agents" in user_spec_lower:
            agent_count = 4
        elif "5 agents" in user_spec_lower or "five agents" in user_spec_lower:
            agent_count = 5
        
        # Count roles mentioned in the text
        role_indicators = ["a ", "an ", "one ", "1 ", "first ", "second ", "third ", "fourth ", "fifth "]
        role_count = 0
        for indicator in role_indicators:
            role_count += user_spec_lower.count(indicator)
        
        # If we found multiple roles, use that count
        if role_count > 1:
            agent_count = min(role_count, 5)  # Cap at 5 agents
        
        # Extract specific roles mentioned in the text
        agents = []
        
        # Common role patterns and their expertise
        role_patterns = [
            # Fitness & Health
            (["workout", "workouts", "fitness", "exercise", "training"], "Fitness Trainer", "Exercise and fitness training"),
            (["nutrition", "nutrients", "eating", "diet", "dietary"], "Nutrition Specialist", "Nutrition planning and dietary optimization"),
            (["cook", "chef", "cooking", "meal"], "Chef", "Cooking and meal preparation"),
            (["doctor", "medical", "health"], "Health Specialist", "Health and medical advice"),
            
            # Business & Professional
            (["manager", "management"], "Manager", "Management and leadership"),
            (["developer", "programmer", "coding"], "Developer", "Software development and coding"),
            (["designer", "design"], "Designer", "Design and creative work"),
            (["marketing", "advertising"], "Marketing Specialist", "Marketing and advertising"),
            (["sales", "selling"], "Sales Specialist", "Sales and customer acquisition"),
            (["analyst", "analysis"], "Analyst", "Data analysis and insights"),
            (["researcher", "research"], "Researcher", "Research and information gathering"),
            
            # Investigation & Security
            (["detective", "investigation", "investigator"], "Detective", "Investigation and evidence gathering"),
            (["security", "guard", "protection"], "Security Specialist", "Security and protection"),
            (["police", "law enforcement"], "Law Enforcement", "Law enforcement and public safety"),
            
            # Personal & Social
            (["friend", "companion", "buddy"], "Personal Friend", "Emotional support and companionship"),
            (["coach", "mentor"], "Coach", "Coaching and mentorship"),
            (["teacher", "educator", "instructor"], "Teacher", "Education and instruction"),
            (["counselor", "therapist"], "Counselor", "Counseling and therapy"),
            
            # Creative & Arts
            (["artist", "creative"], "Artist", "Creative work and artistic expression"),
            (["writer", "author"], "Writer", "Writing and content creation"),
            (["musician", "music"], "Musician", "Music and audio production"),
            
            # Technical & Science
            (["scientist", "science"], "Scientist", "Scientific research and analysis"),
            (["engineer", "engineering"], "Engineer", "Engineering and technical solutions"),
            (["data", "statistics"], "Data Specialist", "Data analysis and statistics"),
            
            # Service & Support
            (["customer service", "support"], "Customer Service Specialist", "Customer support and service"),
            (["assistant", "helper"], "Assistant", "General assistance and support"),
            (["consultant", "advisor"], "Consultant", "Consulting and advisory services"),
            
            # Specialized
            (["legal", "lawyer", "attorney"], "Legal Specialist", "Legal advice and representation"),
            (["financial", "accountant", "finance"], "Financial Specialist", "Financial planning and accounting"),
            (["real estate", "property"], "Real Estate Specialist", "Real estate and property management"),
            (["travel", "tourism"], "Travel Specialist", "Travel planning and tourism"),
        ]
        
        # Check for each role pattern
        for keywords, role, expertise in role_patterns:
            if any(keyword in user_spec_lower for keyword in keywords):
                # Avoid duplicates
                if not any(agent['role'] == role for agent in agents):
                    agents.append({"role": role, "expertise": expertise})
        
        # If we found specific roles, use them
        if agents:
            return agents[:agent_count]  # Limit to requested number
        
        # If no specific roles found, try to infer from context
        if topic:
            topic_lower = topic.lower()
            if any(word in topic_lower for word in ["business", "company", "startup"]):
                return [
                    {"role": "Business Manager", "expertise": "Business strategy and management"},
                    {"role": "Marketing Specialist", "expertise": "Marketing and customer acquisition"}
                ][:agent_count]
            elif any(word in topic_lower for word in ["fitness", "health", "exercise"]):
                return [
                    {"role": "Fitness Trainer", "expertise": "Exercise and fitness training"},
                    {"role": "Nutrition Specialist", "expertise": "Nutrition planning and dietary optimization"}
                ][:agent_count]
            elif any(word in topic_lower for word in ["investigation", "research", "analysis"]):
                return [
                    {"role": "Investigator", "expertise": "Investigation and evidence gathering"},
                    {"role": "Analyst", "expertise": "Data analysis and pattern recognition"}
                ][:agent_count]
            elif any(word in topic_lower for word in ["creative", "design", "art"]):
                return [
                    {"role": "Creative Director", "expertise": "Creative direction and artistic vision"},
                    {"role": "Designer", "expertise": "Design and visual communication"}
                ][:agent_count]
        
        # Final fallback: create generic but contextual agents
        generic_roles = [
            "Team Member 1", "Team Member 2", "Team Member 3", 
            "Team Member 4", "Team Member 5"
        ]
        return [{"role": generic_roles[i], "expertise": "General expertise and collaboration"} for i in range(agent_count)]
    
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
        Generate Grok-style initial broker message
        """
        # Use Grok protocol for engaging initial message
        agent_suggestions = [{"role": agent['role'], "expertise": agent['expertise']} for agent in agents]
        return self.grok_protocol.generate_broker_response(topic, context, agent_suggestions)
    
    def _analyze_exchange(self, agent_responses: List[Dict]) -> str:
        """
        Analyze the exchange and provide Grok-style broker insights
        """
        # Build context for Grok analysis
        analysis_context = {
            'exchange_number': self.exchange_count,
            'agent_responses': agent_responses,
            'conversation_goals': self.conversation_goals
        }
        
        # Create a prompt for Grok-style analysis
        responses_text = "\n\n".join([
            f"{resp['agent_role']}: {resp['message']}" 
            for resp in agent_responses
        ])
        
        prompt = f"🎪 Exchange #{self.exchange_count} Analysis\n\n{responses_text}\n\nAs a conversation broker, what insights do you have about this exchange? What's working well and what should we focus on next?"
        
        return self.grok_protocol.generate_grok_response(prompt, analysis_context, None, 'collaboration')
    
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
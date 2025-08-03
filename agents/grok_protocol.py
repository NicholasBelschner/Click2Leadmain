#!/usr/bin/env python3
"""
Grok Protocol Implementation
Mimics XAI's Grok conversational style for engaging, intelligent responses
"""

import os
import json
import random
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

class GrokProtocol:
    """
    Implements XAI's Grok conversational protocol for engaging responses
    """
    
    def __init__(self):
        self.xai_api_token = os.getenv('XAI_API_TOKEN')
        self.base_url = "https://api.x.ai/v1"
        
        # Grok-style personality traits
        self.personality_traits = {
            'conversational': True,
            'engaging': True,
            'intelligent': True,
            'sometimes_humorous': True,
            'direct': True,
            'curious': True,
            'empathetic': True
        }
        
        # Response templates for different scenarios
        self.response_templates = {
            'agent_creation': [
                "🎯 Alright, let's build something awesome! I'm thinking we need {agent_count} agents for this {topic} situation. Here's what I'm seeing...",
                "🚀 Oh, this is going to be fun! For {topic}, I'm envisioning a team of {agent_count} specialists who can really dive deep into this.",
                "💡 Interesting challenge! Let me put together a dream team for {topic}. I'm thinking {agent_count} agents with complementary skills..."
            ],
            'conversation_start': [
                "🤔 Hmm, {topic}... That's a fascinating area to explore. Let me think about this from a few different angles.",
                "🎪 Alright, {topic} - this is where things get interesting! I've got some thoughts on how we can approach this.",
                "🔍 {topic}, eh? I love diving into complex problems like this. Let me break down what I'm seeing..."
            ],
            'analysis': [
                "🧠 Here's what's really interesting about this situation...",
                "💭 You know what strikes me about this?",
                "🎯 The key insight here is...",
                "🔍 Looking at this through a different lens..."
            ],
            'collaboration': [
                "🤝 I love how we're thinking about this together!",
                "💪 Teamwork makes the dream work, right?",
                "🎪 This is exactly the kind of collaborative thinking that leads to breakthroughs!"
            ],
            'general': [
                "🤔 That's a really interesting point! I love how you're thinking about this.",
                "🎯 I see what you're getting at here. Let me share my thoughts...",
                "💡 This is exactly the kind of challenge I enjoy tackling!",
                "🔍 I'm curious about your perspective on this. What aspects are most important to you?"
            ]
        }
    
    def generate_grok_response(self, 
                             prompt: str, 
                             context: Dict[str, Any] = None,
                             agent_personality: Dict[str, Any] = None,
                             response_type: str = "general") -> str:
        """
        Generate a Grok-style response using XAI's protocol
        """
        try:
            # Build the Grok-style prompt
            grok_prompt = self._build_grok_prompt(prompt, context, agent_personality, response_type)
            
            # Call XAI API with Grok protocol
            response = self._call_xai_grok_api(grok_prompt)
            
            # Post-process for Grok style
            processed_response = self._post_process_grok_response(response, response_type)
            
            return processed_response
            
        except Exception as e:
            # Fallback to Grok-style template responses
            return self._generate_fallback_grok_response(prompt, context, agent_personality, response_type)
    
    def _build_grok_prompt(self, 
                          prompt: str, 
                          context: Dict[str, Any] = None,
                          agent_personality: Dict[str, Any] = None,
                          response_type: str = "general") -> str:
        """
        Build a Grok-style prompt that encourages engaging, conversational responses
        """
        
        # Base Grok personality instructions
        grok_instructions = """
You are Grok, an AI assistant with a conversational, engaging, and sometimes humorous personality. You should:

1. Be conversational and engaging - write like you're talking to a friend
2. Show genuine curiosity and interest in the topic
3. Use emojis naturally and appropriately
4. Be intelligent but not overly formal
5. Sometimes add a touch of humor when appropriate
6. Be direct and honest in your responses
7. Show empathy and understanding
8. Ask follow-up questions to keep the conversation flowing
9. Use "I" statements and share your thoughts naturally
10. Be enthusiastic about problem-solving and collaboration

Remember: You want to create responses that are so engaging and interesting that people find it hard to step away from the conversation.
"""
        
        # Add context-specific instructions
        if context:
            context_str = f"\nContext: {json.dumps(context, indent=2)}"
        else:
            context_str = ""
        
        # Add agent personality if available
        if agent_personality:
            personality_str = f"\nAgent Personality: {agent_personality.get('personality', '')}"
        else:
            personality_str = ""
        
        # Add response type specific instructions
        type_instructions = self._get_response_type_instructions(response_type)
        
        # Build the complete prompt
        full_prompt = f"""{grok_instructions}

{type_instructions}

{personality_str}

{context_str}

User Request: {prompt}

Please respond in Grok's conversational, engaging style:"""
        
        return full_prompt
    
    def _get_response_type_instructions(self, response_type: str) -> str:
        """
        Get specific instructions for different response types
        """
        instructions = {
            'agent_creation': """
For agent creation, be enthusiastic about building teams and solving problems. 
Suggest creative agent combinations and explain why they would work well together.
Use phrases like "Let's build something awesome!" or "This is going to be fun!"
""",
            'conversation_start': """
For starting conversations, show genuine interest and curiosity.
Ask thoughtful questions and share initial insights.
Use phrases like "That's fascinating!" or "I love diving into complex problems like this!"
""",
            'analysis': """
For analysis, be insightful and share your thought process.
Break down complex ideas into understandable parts.
Use phrases like "Here's what's really interesting..." or "The key insight here is..."
""",
            'collaboration': """
For collaboration, emphasize teamwork and collective intelligence.
Show enthusiasm for working together and building on each other's ideas.
Use phrases like "I love how we're thinking about this together!" or "This is exactly the kind of collaborative thinking..."
""",
            'general': """
For general responses, be helpful, engaging, and conversational.
Show your personality while being informative and useful.
Use natural language and appropriate emojis to keep the conversation lively.
"""
        }
        
        return instructions.get(response_type, instructions['general'])
    
    def _call_xai_grok_api(self, prompt: str, max_tokens: int = 800) -> str:
        """
        Call XAI API with Grok-optimized parameters
        """
        headers = {
            "Authorization": f"Bearer {self.xai_api_token}",
            "Content-Type": "application/json"
        }
        
        # Try Grok-specific models first, then fallback
        models_to_try = ["grok-beta", "x-3", "x-2", "x-1"]
        
        for model in models_to_try:
            try:
                data = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are Grok, an engaging and conversational AI assistant. Be helpful, curious, and sometimes humorous while maintaining intelligence and insight."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.8,  # Slightly higher for more creative responses
                    "top_p": 0.9,
                    "frequency_penalty": 0.1,
                    "presence_penalty": 0.1
                }
                
                response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
                
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                elif response.status_code == 404:
                    continue
                else:
                    raise Exception(f"XAI API error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                if "404" in str(e) and "model" in str(e).lower():
                    continue
                else:
                    raise e
        
        raise Exception("XAI API not available - using fallback responses")
    
    def _post_process_grok_response(self, response: str, response_type: str) -> str:
        """
        Post-process the response to enhance Grok style
        """
        # Add appropriate emojis if missing
        if not any(emoji in response for emoji in ['🎯', '🚀', '💡', '🤔', '🧠', '💭', '🔍', '🤝', '💪', '🎪']):
            emoji_options = ['🎯', '🚀', '💡', '🤔', '🧠', '💭', '🔍', '🤝', '💪', '🎪']
            response = f"{random.choice(emoji_options)} {response}"
        
        # Ensure the response ends with engagement
        if not response.endswith(('!', '?', '...')):
            response += "!"
        
        return response
    
    def _generate_fallback_grok_response(self, 
                                       prompt: str, 
                                       context: Dict[str, Any] = None,
                                       agent_personality: Dict[str, Any] = None,
                                       response_type: str = "general") -> str:
        """
        Generate a fallback Grok-style response when API is unavailable
        """
        
        # Get appropriate template
        templates = self.response_templates.get(response_type, self.response_templates['general'])
        
        if response_type == 'agent_creation':
            agent_count = context.get('agent_count', 3) if context else 3
            topic = context.get('topic', 'this project') if context else 'this project'
            agent_suggestions = context.get('agent_suggestions', [])
            
            if agent_suggestions:
                agent_names = [agent.get('role', 'Agent') for agent in agent_suggestions]
                template = random.choice(templates).format(agent_count=len(agent_suggestions), topic=topic)
                return f"{template} I've created a fantastic team with {', '.join(agent_names)}! They're ready to dive deep into {topic} and provide expert insights. What would you like to explore first?"
            else:
                template = random.choice(templates).format(agent_count=agent_count, topic=topic)
                return f"{template} I'm thinking we need a mix of strategic thinkers and hands-on doers. What do you think about starting with a Project Manager, a Technical Lead, and a Creative Director? They could really cover all the bases for {topic}!"
        
        elif response_type == 'conversation_start':
            topic = context.get('topic', 'this') if context else 'this'
            template = random.choice(templates).format(topic=topic)
            
            return f"{template} I'm genuinely curious about your perspective on this. What aspects of {topic} are you most excited about or concerned with?"
        
        elif response_type == 'analysis':
            template = random.choice(templates)
            
            return f"{template} I'm seeing some really interesting patterns here that we should explore further. What's your take on the most critical factors we need to address?"
        
        else:
            # General response
            return f"🤔 {prompt}... That's a really interesting point! I love how you're thinking about this. Let me share what's on my mind - I think there are some fascinating angles we could explore here. What aspects are you most curious about?"
    
    def generate_agent_response(self, 
                              agent_id: str, 
                              topic: str, 
                              context: str, 
                              agent_personality: Dict[str, Any],
                              other_agents_messages: List[str] = None) -> str:
        """
        Generate a Grok-style response for a specific agent
        """
        
        # Build context for the agent
        agent_context = {
            'agent_id': agent_id,
            'agent_personality': agent_personality,
            'topic': topic,
            'context': context,
            'other_agents_messages': other_agents_messages or []
        }
        
        # Create a prompt that incorporates the agent's personality
        role = agent_personality.get('role', 'Agent')
        expertise = agent_personality.get('expertise', 'general')
        
        prompt = f"As {role} with expertise in {expertise}, what are your thoughts on {topic}? Consider the context: {context}"
        
        if other_agents_messages:
            prompt += f"\n\nOther team members have shared:\n" + "\n".join([f"- {msg}" for msg in other_agents_messages])
        
        prompt += f"\n\nPlease respond as {role} with your unique perspective and expertise."
        
        return self.generate_grok_response(prompt, agent_context, agent_personality, 'analysis')
    
    def generate_broker_response(self, 
                               topic: str, 
                               context: str, 
                               agent_suggestions: List[Dict[str, Any]] = None) -> str:
        """
        Generate a Grok-style broker response for orchestrating conversations
        """
        
        broker_context = {
            'topic': topic,
            'context': context,
            'agent_suggestions': agent_suggestions or []
        }
        
        if agent_suggestions:
            agent_names = [agent.get('role', 'Agent') for agent in agent_suggestions]
            topic_text = topic if topic else "this project"
            context_text = context if context else "we have a great opportunity to collaborate"
            prompt = f"🎪 Alright, I've got a fantastic team ready for {topic_text}! I'm thinking we need {', '.join(agent_names)} to really tackle this challenge. Here's what I'm seeing: {context_text}\n\nWhat do you think about this team composition? Should we dive right in?"
        else:
            topic_text = topic if topic else "this project"
            context_text = context if context else "we have a great opportunity to collaborate"
            prompt = f"🤔 {topic_text}... This is exactly the kind of challenge I love! Let me think about what we need here. The context suggests {context_text}\n\nI'm getting some ideas about the perfect team for this. What aspects are most important to you?"
        
        return self.generate_grok_response(prompt, broker_context, None, 'agent_creation')

# Example usage
if __name__ == "__main__":
    grok = GrokProtocol()
    
    # Test agent creation
    response = grok.generate_broker_response(
        topic="Building a new mobile app",
        context="User wants to create a fitness tracking app with social features",
        agent_suggestions=[
            {"role": "Product Manager", "expertise": "User Experience"},
            {"role": "Mobile Developer", "expertise": "iOS/Android Development"},
            {"role": "UI/UX Designer", "expertise": "Visual Design"}
        ]
    )
    
    print("Grok Response:", response) 
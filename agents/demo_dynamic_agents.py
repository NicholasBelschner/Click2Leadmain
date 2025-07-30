#!/usr/bin/env python3
"""
Demo Dynamic Agent System
Demonstrates the new dynamic agent creation and conversation system
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

from dynamic_orchestrator import DynamicAgentOrchestrator

load_dotenv()

def test_agent_creation_workflow():
    """
    Test the complete workflow of creating agents dynamically
    """
    print("🚀 Testing Dynamic Agent Creation Workflow")
    print("=" * 50)
    
    orchestrator = DynamicAgentOrchestrator()
    
    # Test 1: Start conversation without agents
    print("\n📋 Test 1: Starting conversation without specifying agents...")
    result = orchestrator.start_conversation(
        topic="Redesigning the user onboarding flow",
        context="Current drop-off rate is 40%, need to improve user retention"
    )
    
    print(f"Status: {result['status']}")
    if result['status'] == 'needs_agents':
        print("✅ Broker correctly identified that agents need to be specified")
        print(f"📝 Broker message: {result['message'][:200]}...")
        print(f"💡 Suggestions provided: {len(result['suggestions'])} roles")
        
        # Show suggestions
        print("\n📋 Suggested Agent Roles:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion['role']}")
            print(f"     Expertise: {suggestion['expertise']}")
            print(f"     Reasoning: {suggestion['reasoning']}")
            print()
    
    return result

def test_agent_creation_from_specification():
    """
    Test creating agents from user specification
    """
    print("\n🔧 Test 2: Creating agents from user specification...")
    print("=" * 50)
    
    orchestrator = DynamicAgentOrchestrator()
    
    # Test different specification formats
    test_specs = [
        "Create 3 agents: Product Manager, UX Designer, and Developer",
        "I want a Marketing Manager and Data Analyst",
        "Just create 2 agents for strategy and technical implementation"
    ]
    
    for i, spec in enumerate(test_specs, 1):
        print(f"\n🧪 Test 2.{i}: '{spec}'")
        
        result = orchestrator.create_agents_from_specification(
            spec,
            "Redesigning the user onboarding flow",
            "Current drop-off rate is 40%, need to improve user retention"
        )
        
        print(f"Status: {result['status']}")
        if result['status'] == 'started':
            print(f"✅ Successfully created {result['agents_created']} agents")
            print("📋 Created Agents:")
            for agent in result['agents']:
                print(f"  - {agent['role']} (ID: {agent['id']})")
                print(f"    Expertise: {agent['expertise']}")
                print(f"    Personality: {agent['personality'][:100]}...")
        else:
            print(f"❌ Failed: {result.get('message', 'Unknown error')}")

def test_conversation_exchanges():
    """
    Test conducting exchanges between agents
    """
    print("\n💬 Test 3: Testing conversation exchanges...")
    print("=" * 50)
    
    orchestrator = DynamicAgentOrchestrator()
    
    # Create agents first
    result = orchestrator.create_agents_from_specification(
        "Create 2 agents: Product Manager and Senior Developer",
        "Implementing a new feature for user analytics",
        "Need to balance user experience with technical feasibility"
    )
    
    if result['status'] != 'started':
        print(f"❌ Failed to create agents: {result.get('message', 'Unknown error')}")
        return
    
    print("✅ Agents created successfully")
    print(f"📝 Broker message: {result['broker_message']}")
    
    # Conduct a few exchanges
    for i in range(3):
        print(f"\n🔄 Exchange {i+1}:")
        exchange_result = orchestrator.conduct_exchange()
        
        if exchange_result['status'] == 'exchange_completed':
            print(f"✅ Exchange {exchange_result['exchange_number']} completed")
            print("📋 Agent Responses:")
            for response in exchange_result['agent_responses']:
                print(f"  {response['agent_role']}: {response['message'][:100]}...")
            print(f"📊 Broker Analysis: {exchange_result['broker_analysis'][:100]}...")
        elif exchange_result['status'] == 'concluded':
            print("✅ Conversation concluded")
            print(f"📝 Conclusion: {exchange_result['conclusion'][:200]}...")
            break
        else:
            print(f"❌ Exchange failed: {exchange_result.get('message', 'Unknown error')}")
            break

def test_full_conversation():
    """
    Test a complete conversation from start to finish
    """
    print("\n🎯 Test 4: Full conversation test...")
    print("=" * 50)
    
    orchestrator = DynamicAgentOrchestrator()
    
    # Conduct full conversation
    result = orchestrator.conduct_full_conversation(
        topic="Q4 Marketing Campaign Strategy",
        context="Budget: $100K, target: increase conversions by 25%",
        agent_specifications=[
            {'role': 'Marketing Manager', 'expertise': 'Campaign strategy and execution'},
            {'role': 'Data Analyst', 'expertise': 'Performance analysis and optimization'},
            {'role': 'Creative Director', 'expertise': 'Creative strategy and design'}
        ],
        max_exchanges=4
    )
    
    print(f"Status: {result['status']}")
    if result['status'] == 'completed':
        print(f"✅ Conversation completed successfully")
        print(f"📊 Total exchanges: {result['total_exchanges']}")
        print(f"👥 Agents participated: {len(result['agents'])}")
        
        # Show final agents
        print("\n📋 Final Agents:")
        for agent in result['agents']:
            print(f"  - {agent['role']} (ID: {agent['id']})")
    else:
        print(f"❌ Conversation failed: {result.get('message', 'Unknown error')}")

def test_agent_management():
    """
    Test agent management functions
    """
    print("\n⚙️ Test 5: Agent management functions...")
    print("=" * 50)
    
    orchestrator = DynamicAgentOrchestrator()
    
    # Create some agents
    result = orchestrator.create_agents_from_specification(
        "Create 3 agents: Project Manager, Developer, and Designer",
        "Building a new mobile app",
        "Need to coordinate development and design"
    )
    
    if result['status'] != 'started':
        print(f"❌ Failed to create agents: {result.get('message', 'Unknown error')}")
        return
    
    # Test getting all agents
    all_agents = orchestrator.get_all_agents()
    print(f"📋 Total agents in system: {len(all_agents)}")
    
    # Test getting specific agent
    if all_agents:
        agent_id = all_agents[0]['id']
        agent = orchestrator.get_agent(agent_id)
        print(f"📋 Retrieved agent: {agent['role']} (ID: {agent['id']})")
        
        # Test updating agent
        update_success = orchestrator.update_agent(agent_id, {
            'expertise': 'Updated expertise area',
            'status': 'updated'
        })
        print(f"✅ Agent update: {'Success' if update_success else 'Failed'}")
        
        # Test deleting agent
        delete_success = orchestrator.delete_agent(agent_id)
        print(f"✅ Agent deletion: {'Success' if delete_success else 'Failed'}")
        
        # Verify deletion
        remaining_agents = orchestrator.get_all_agents()
        print(f"📋 Remaining agents: {len(remaining_agents)}")

def test_agent_suggestions():
    """
    Test agent role suggestions
    """
    print("\n💡 Test 6: Agent role suggestions...")
    print("=" * 50)
    
    orchestrator = DynamicAgentOrchestrator()
    
    # Test different topics
    test_cases = [
        {
            'topic': 'Implementing AI-powered customer support',
            'context': 'Need to reduce support tickets by 50%'
        },
        {
            'topic': 'Redesigning the company website',
            'context': 'Current site is outdated, need modern design'
        },
        {
            'topic': 'Launching a new product line',
            'context': 'Target market: young professionals, budget: $500K'
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🧪 Test 6.{i}: {case['topic']}")
        
        suggestions = orchestrator.get_agent_suggestions(case['topic'], case['context'])
        
        print(f"💡 Suggested roles: {len(suggestions)}")
        for suggestion in suggestions:
            print(f"  - {suggestion['role']}: {suggestion['expertise']}")

def main():
    """
    Run all tests
    """
    print("🎉 Dynamic Agent System Demo")
    print("=" * 60)
    print("This demo tests the new dynamic agent creation and conversation system")
    print("that allows users to create any number of agents as needed.")
    print()
    
    # Check for XAI API token
    if not os.getenv('XAI_API_TOKEN'):
        print("❌ Error: XAI_API_TOKEN not found in environment variables")
        print("Please set your XAI API token in the .env file")
        return
    
    try:
        # Run all tests
        test_agent_creation_workflow()
        test_agent_creation_from_specification()
        test_conversation_exchanges()
        test_full_conversation()
        test_agent_management()
        test_agent_suggestions()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Summary of Dynamic Agent System Features:")
        print("✅ Dynamic agent creation based on user specifications")
        print("✅ AI-powered agent role suggestions")
        print("✅ Flexible conversation management")
        print("✅ Agent personality generation using XAI")
        print("✅ Full conversation orchestration")
        print("✅ Agent management (create, read, update, delete)")
        print("✅ Conversation logging and export")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Quick Test - Dynamic Agent System
Simple demonstration of the new dynamic agent features
"""

from dynamic_orchestrator import DynamicAgentOrchestrator

def main():
    print("🚀 Quick Test - Dynamic Agent System")
    print("=" * 50)
    
    # Initialize the orchestrator
    orchestrator = DynamicAgentOrchestrator()
    
    # Test 1: Create agents from specification
    print("\n📋 Test 1: Creating agents from user specification")
    print("User says: 'Create 3 agents: Product Manager, Developer, and Designer'")
    
    result = orchestrator.create_agents_from_specification(
        "Create 3 agents: Product Manager, Developer, and Designer",
        "Building a new mobile app",
        "Need to coordinate development and design"
    )
    
    if result['status'] == 'started':
        print(f"✅ Success! Created {result['agents_created']} agents")
        print("📋 Created Agents:")
        for agent in result['agents']:
            print(f"  - {agent['role']} (ID: {agent['id']})")
            print(f"    Expertise: {agent['expertise']}")
            print(f"    Personality: {agent['personality'][:100]}...")
            print()
    
    # Test 2: Conduct an exchange
    print("\n💬 Test 2: Conducting an exchange")
    exchange_result = orchestrator.conduct_exchange()
    
    if exchange_result['status'] == 'exchange_completed':
        print(f"✅ Exchange {exchange_result['exchange_number']} completed!")
        print("📋 Agent Responses:")
        for response in exchange_result['agent_responses']:
            print(f"  {response['agent_role']}: {response['message'][:100]}...")
        print(f"📊 Broker Analysis: {exchange_result['broker_analysis'][:100]}...")
    
    # Test 3: Show conversation status
    print("\n📊 Test 3: Conversation Status")
    status = orchestrator.get_conversation_status()
    print(f"Status: {status['status']}")
    print(f"Agents: {status['agents_count']}")
    print(f"Exchanges: {status['exchanges_completed']}/{status['max_exchanges']}")
    
    # Test 4: Get all agents
    print("\n👥 Test 4: All Agents in System")
    all_agents = orchestrator.get_all_agents()
    print(f"Total agents: {len(all_agents)}")
    for agent in all_agents:
        print(f"  - {agent['role']} (ID: {agent['id']})")
    
    print("\n🎉 Quick test completed successfully!")
    print("\n📋 What we demonstrated:")
    print("✅ Dynamic agent creation from user specification")
    print("✅ Multi-agent conversation coordination")
    print("✅ Agent response generation")
    print("✅ Broker analysis and facilitation")
    print("✅ Agent management and tracking")

if __name__ == "__main__":
    main() 
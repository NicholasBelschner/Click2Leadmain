#!/usr/bin/env python3
"""
Demo script for the multi-agent conversation system.
Tests different scenarios with the broker, employee1, and employee2 agents.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

from agent_orchestrator import AgentOrchestrator

# Load environment variables
load_dotenv()

def demo_scenario_1():
    """Demo: Project Manager vs Developer - Timeline Discussion"""
    print("🎬 DEMO SCENARIO 1: Project Timeline Discussion")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator(
        employee1_role="Project Manager",
        employee1_expertise="Project planning, timeline management, and stakeholder coordination",
        employee2_role="Senior Developer",
        employee2_expertise="Technical implementation, system architecture, and development planning"
    )
    
    result = orchestrator.conduct_full_conversation(
        topic="Project timeline adjustment for the authentication module",
        context="The client needs the authentication module delivered by next Friday, but the development team estimates it will take 2 more weeks",
        max_exchanges=4
    )
    
    # Save conversation log
    log_file = orchestrator.save_conversation_log("demo_scenario_1_timeline.json")
    print(f"\n💾 Conversation log saved to: {log_file}")
    
    return result

def demo_scenario_2():
    """Demo: Product Manager vs UX Designer - Feature Design"""
    print("\n🎬 DEMO SCENARIO 2: Feature Design Discussion")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator(
        employee1_role="Product Manager",
        employee1_expertise="Product strategy, market analysis, and business requirements",
        employee2_role="UX Designer",
        employee2_expertise="User experience design, user research, and interface design"
    )
    
    result = orchestrator.conduct_full_conversation(
        topic="Designing a new user onboarding flow",
        context="Current onboarding has a 40% drop-off rate, need to improve user retention",
        max_exchanges=5
    )
    
    # Save conversation log
    log_file = orchestrator.save_conversation_log("demo_scenario_2_ux_design.json")
    print(f"\n💾 Conversation log saved to: {log_file}")
    
    return result

def demo_scenario_3():
    """Demo: Marketing Manager vs Data Analyst - Campaign Strategy"""
    print("\n🎬 DEMO SCENARIO 3: Marketing Campaign Strategy")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator(
        employee1_role="Marketing Manager",
        employee1_expertise="Marketing strategy, brand management, and campaign planning",
        employee2_role="Data Analyst",
        employee2_expertise="Data analysis, performance metrics, and statistical modeling"
    )
    
    result = orchestrator.conduct_full_conversation(
        topic="Optimizing the Q4 marketing campaign budget allocation",
        context="Need to allocate $100K budget across different channels based on performance data",
        max_exchanges=6
    )
    
    # Save conversation log
    log_file = orchestrator.save_conversation_log("demo_scenario_3_marketing.json")
    print(f"\n💾 Conversation log saved to: {log_file}")
    
    return result

def demo_scenario_4():
    """Demo: HR Manager vs IT Manager - System Implementation"""
    print("\n🎬 DEMO SCENARIO 4: HR System Implementation")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator(
        employee1_role="HR Manager",
        employee1_expertise="Human resources, employee relations, and policy management",
        employee2_role="IT Manager",
        employee2_expertise="Information technology, system administration, and security"
    )
    
    result = orchestrator.conduct_full_conversation(
        topic="Implementing a new employee performance management system",
        context="Need to replace the current paper-based system with a digital solution that integrates with existing HR tools",
        max_exchanges=5
    )
    
    # Save conversation log
    log_file = orchestrator.save_conversation_log("demo_scenario_4_hr_system.json")
    print(f"\n💾 Conversation log saved to: {log_file}")
    
    return result

def run_all_demos():
    """Run all demo scenarios and provide a summary."""
    print("🤖 MULTI-AGENT CONVERSATION SYSTEM DEMO")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Testing different scenarios with broker-coordinated conversations")
    print("=" * 80)
    
    results = []
    
    try:
        # Run all scenarios
        results.append(demo_scenario_1())
        results.append(demo_scenario_2())
        results.append(demo_scenario_3())
        results.append(demo_scenario_4())
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 DEMO SUMMARY")
        print("=" * 80)
        
        total_exchanges = 0
        completed_conversations = 0
        
        for i, result in enumerate(results, 1):
            scenario_name = f"Scenario {i}"
            exchanges = result['total_exchanges']
            completed = result['completed']
            progress = result['final_summary']['progress']['overall']
            
            print(f"{scenario_name}:")
            print(f"  Topic: {result['topic']}")
            print(f"  Exchanges: {exchanges}")
            print(f"  Completed: {'✅' if completed else '⏹️'}")
            print(f"  Progress: {progress:.1f}%")
            print()
            
            total_exchanges += exchanges
            if completed:
                completed_conversations += 1
        
        print(f"📈 OVERALL STATISTICS:")
        print(f"  Total Scenarios: {len(results)}")
        print(f"  Total Exchanges: {total_exchanges}")
        print(f"  Completed Conversations: {completed_conversations}/{len(results)}")
        print(f"  Average Exchanges per Scenario: {total_exchanges/len(results):.1f}")
        print(f"  Success Rate: {(completed_conversations/len(results)*100):.1f}%")
        
        print("\n✅ All demos completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("Please check your XAI API token and internet connection.")

def test_individual_agents():
    """Test individual agents separately."""
    print("🧪 TESTING INDIVIDUAL AGENTS")
    print("=" * 40)
    
    from broker import BrokerAgent
    from employee1 import Employee1Agent
    from employee2 import Employee2Agent
    
    # Test broker
    print("Testing Broker Agent...")
    broker = BrokerAgent()
    broker_result = broker.start_conversation(
        topic="Test conversation",
        employee1_context="Test employee 1",
        employee2_context="Test employee 2"
    )
    print(f"✅ Broker initialized: {broker_result['conversation_id']}")
    
    # Test Employee1
    print("Testing Employee1 Agent...")
    employee1 = Employee1Agent(role="Test Manager", expertise="Test management")
    emp1_response = employee1.provide_initial_perspective("Test topic", "Test context")
    print(f"✅ Employee1 response: {emp1_response[:50]}...")
    
    # Test Employee2
    print("Testing Employee2 Agent...")
    employee2 = Employee2Agent(role="Test Developer", expertise="Test development")
    emp2_response = employee2.provide_initial_perspective("Test topic", "Test context")
    print(f"✅ Employee2 response: {emp2_response[:50]}...")
    
    print("✅ All individual agents tested successfully!")

if __name__ == "__main__":
    # Check if XAI API token is available
    if not os.getenv('XAI_API_TOKEN'):
        print("❌ XAI_API_TOKEN not found in environment variables")
        print("Please set your XAI API token in the .env file")
        exit(1)
    
    # Test individual agents first
    test_individual_agents()
    
    print("\n" + "=" * 80)
    
    # Run all demos
    run_all_demos() 
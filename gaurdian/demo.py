#!/usr/bin/env python3
"""
Comprehensive demonstration of the NLP Importance Classifier system.
This script shows how to use the system for various real-world scenarios.
"""

import json
from datetime import datetime
from nlp_classifier import NLPImportanceClassifier
from database_integration import DatabaseNLPProcessor

def demo_basic_classification():
    """Demonstrate basic text classification."""
    print("=" * 60)
    print("DEMO 1: Basic Text Classification")
    print("=" * 60)
    
    classifier = NLPImportanceClassifier()
    classifier.load_model()
    
    # Sample texts from different sources
    sample_texts = [
        # Business emails
        "Meeting scheduled for Q4 budget review on Friday 2 PM",
        "Please review the attached quarterly sales report",
        "Happy birthday! Hope you have a great day!",
        
        # System logs
        "ERROR: Database connection timeout after 30 seconds",
        "INFO: User login successful - user_id: 12345",
        "DEBUG: Processing request for endpoint /api/users",
        
        # Customer data
        "Customer complaint: Product arrived damaged",
        "New customer registration: john.smith@email.com",
        "The coffee machine is broken again",
        
        # Social media
        "Just had the best pizza ever! 🍕",
        "Can't wait for the weekend!",
        "New product launch: AI-powered chatbot for customer service"
    ]
    
    print("Analyzing text importance for database export...")
    print()
    
    for text in sample_texts:
        result = classifier.predict_single(text)
        status = "✅ EXPORT" if result['is_important'] else "❌ SKIP"
        print(f"Text: {text}")
        print(f"Decision: {status}")
        print(f"Confidence: {result['confidence']:.3f}")
        print("-" * 50)

def demo_batch_processing():
    """Demonstrate batch processing with database integration."""
    print("\n" + "=" * 60)
    print("DEMO 2: Batch Processing with Database Integration")
    print("=" * 60)
    
    processor = DatabaseNLPProcessor()
    processor.load_or_train_model()
    
    # Simulate processing a batch of texts from different sources
    email_batch = [
        "Customer inquiry about product pricing and availability",
        "Meeting reminder: Team standup tomorrow at 9 AM",
        "Order confirmation #ORD-2024-001 for customer ID 45678",
        "Lunch plans with colleagues this Friday"
    ]
    
    log_batch = [
        "ERROR: Payment gateway timeout - transaction failed",
        "INFO: Database backup completed successfully",
        "WARN: High memory usage detected on server-01",
        "DEBUG: API request processed in 45ms"
    ]
    
    # Process batches
    print("Processing email batch...")
    email_results = processor.process_text_batch(email_batch, source='email_system')
    
    print("Processing log batch...")
    log_results = processor.process_text_batch(log_batch, source='system_logs')
    
    # Show statistics
    stats = processor.get_statistics()
    print(f"\nDatabase Statistics:")
    print(f"  Total texts processed: {stats['total_texts']}")
    print(f"  Important texts: {stats['important_texts']}")
    print(f"  Not important texts: {stats['not_important_texts']}")
    print(f"  Importance ratio: {stats['importance_ratio']:.2%}")
    print(f"  Average confidence: {stats['avg_confidence']:.3f}")

def demo_export_functionality():
    """Demonstrate data export functionality."""
    print("\n" + "=" * 60)
    print("DEMO 3: Data Export Functionality")
    print("=" * 60)
    
    processor = DatabaseNLPProcessor()
    processor.load_or_train_model()
    
    # Export important data in different formats
    print("Exporting important data...")
    
    # JSON export
    json_file = processor.export_important_data(output_format='json')
    print(f"JSON export completed: {json_file}")
    
    # CSV export
    csv_file = processor.export_important_data(output_format='csv')
    print(f"CSV export completed: {csv_file}")
    
    # Show sample of exported data
    with open(json_file, 'r') as f:
        exported_data = json.load(f)
    
    print(f"\nSample exported data ({len(exported_data)} records):")
    for i, record in enumerate(exported_data[:3]):
        print(f"  {i+1}. {record['text'][:50]}...")
        print(f"     Score: {record['importance_score']:.3f}")
        print(f"     Source: {record['source']}")

def demo_custom_threshold():
    """Demonstrate using custom confidence thresholds."""
    print("\n" + "=" * 60)
    print("DEMO 4: Custom Confidence Thresholds")
    print("=" * 60)
    
    classifier = NLPImportanceClassifier()
    classifier.load_model()
    
    test_texts = [
        "Critical system error: Database corruption detected",
        "User feedback: Website is slow today",
        "Financial transaction: $10,000 transfer completed",
        "Weather update: Rain expected tomorrow"
    ]
    
    thresholds = [0.3, 0.5, 0.7, 0.9]
    
    for text in test_texts:
        print(f"\nText: {text}")
        print(f"Confidence scores at different thresholds:")
        
        for threshold in thresholds:
            result = classifier.predict_single(text, threshold=threshold)
            status = "EXPORT" if result['is_important'] else "SKIP"
            print(f"  Threshold {threshold}: {status} (Confidence: {result['confidence']:.3f})")

def demo_real_world_scenario():
    """Demonstrate a real-world scenario."""
    print("\n" + "=" * 60)
    print("DEMO 5: Real-World Scenario - Customer Support System")
    print("=" * 60)
    
    processor = DatabaseNLPProcessor()
    processor.load_or_train_model()
    
    # Simulate incoming customer support messages
    support_messages = [
        "Customer complaint: Product not working as advertised",
        "Technical issue: Can't access my account",
        "General inquiry: What are your business hours?",
        "Billing question: Why was I charged twice?",
        "Feature request: Add dark mode to the app",
        "Bug report: App crashes when uploading large files",
        "Praise: Love the new interface design!",
        "Refund request: Item arrived damaged",
        "Account issue: Forgot password, need reset",
        "Product question: Does this work with iOS 15?"
    ]
    
    print("Processing customer support messages for database export...")
    print()
    
    # Process messages
    results = processor.process_text_batch(support_messages, source='customer_support')
    
    # Categorize results
    important_messages = [r for r in results if r['is_important']]
    skip_messages = [r for r in results if not r['is_important']]
    
    print(f"Results Summary:")
    print(f"  Total messages: {len(support_messages)}")
    print(f"  Important (export to DB): {len(important_messages)}")
    print(f"  Skip (don't export): {len(skip_messages)}")
    
    print(f"\nImportant messages to export:")
    for msg in important_messages:
        print(f"  ✅ {msg['text'][:60]}... (Confidence: {msg['confidence']:.3f})")
    
    print(f"\nMessages to skip:")
    for msg in skip_messages:
        print(f"  ❌ {msg['text'][:60]}... (Confidence: {msg['confidence']:.3f})")

def main():
    """Run all demonstrations."""
    print("NLP Importance Classifier - Complete System Demonstration")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Run all demos
        demo_basic_classification()
        demo_batch_processing()
        demo_export_functionality()
        demo_custom_threshold()
        demo_real_world_scenario()
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nThe NLP Importance Classifier system is ready for production use.")
        print("Key features demonstrated:")
        print("  ✅ Real-time text classification")
        print("  ✅ Batch processing capabilities")
        print("  ✅ Database integration")
        print("  ✅ Data export functionality")
        print("  ✅ Customizable confidence thresholds")
        print("  ✅ Real-world scenario handling")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        print("Please ensure the model is trained and all dependencies are installed.")

if __name__ == "__main__":
    main() 
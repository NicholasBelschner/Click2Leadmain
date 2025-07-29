#!/usr/bin/env python3
"""
Test script for the trained NLP Importance Classifier.
"""

from nlp_classifier import NLPImportanceClassifier

def test_model():
    # Load the trained model
    classifier = NLPImportanceClassifier()
    classifier.load_model()
    
    # Test texts
    test_texts = [
        "Customer email: john.doe@example.com",
        "The weather is sunny today",
        "Order #12345 shipped to 123 Main St",
        "I like pizza",
        "Database backup completed successfully",
        "User authentication failed for account ID 45678",
        "Payment processed for transaction #98765",
        "The flowers are blooming in the garden",
        "System error: Connection timeout on port 8080",
        "Meeting reminder for tomorrow at 2 PM"
    ]
    
    print("NLP Importance Classifier - Test Results")
    print("=" * 50)
    
    for text in test_texts:
        result = classifier.predict_single(text)
        status = "✅ IMPORTANT" if result['is_important'] else "❌ NOT IMPORTANT"
        print(f"Text: {text[:60]}...")
        print(f"Status: {status}")
        print(f"Confidence: {result['confidence']:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    test_model() 
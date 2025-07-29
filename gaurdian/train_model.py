#!/usr/bin/env python3
"""
Training script for the NLP Importance Classifier.
This script allows you to train the model with custom data or use the default sample data.
"""

import argparse
import json
import pandas as pd
from nlp_classifier import NLPImportanceClassifier
from database_integration import DatabaseNLPProcessor

def load_custom_data(file_path, text_column='text', label_column='label'):
    """Load custom training data from CSV or JSON file."""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    else:
        raise ValueError("File must be CSV or JSON format")
    
    texts = df[text_column].tolist()
    labels = df[label_column].tolist()
    
    return texts, labels

def create_sample_training_data():
    """Create a comprehensive sample training dataset."""
    important_texts = [
        # Customer data
        "Customer contact information including email and phone number",
        "Customer profile data with preferences and settings",
        "Customer feedback and satisfaction scores",
        "Customer support ticket details and resolutions",
        "Customer order history and purchase patterns",
        
        # Transaction data
        "Sales transaction details with product codes and quantities",
        "Financial transaction records with amounts and dates",
        "Payment processing details and transaction IDs",
        "Order tracking information and delivery status",
        "Invoice data with line items and totals",
        
        # System data
        "User authentication credentials and security tokens",
        "System error logs and debugging information",
        "Database backup schedules and retention policies",
        "API endpoint configurations and access keys",
        "User session data and activity timestamps",
        
        # Product data
        "Product inventory levels and stock counts",
        "Product pricing information and discount codes",
        "Product specifications and technical details",
        "Product reviews and ratings",
        "Product category and classification data",
        
        # Business metrics
        "Revenue reports and financial summaries",
        "Sales performance metrics and KPIs",
        "User engagement statistics and analytics",
        "Conversion rates and funnel data",
        "Customer lifetime value calculations"
    ]
    
    not_important_texts = [
        # Personal conversations
        "The weather is nice today",
        "I had coffee for breakfast",
        "The movie was entertaining",
        "Traffic was heavy this morning",
        "The restaurant had good food",
        
        # Casual activities
        "I went for a walk in the park",
        "The book was interesting to read",
        "Music helps me focus while working",
        "The sunset was beautiful yesterday",
        "I enjoy cooking on weekends",
        
        # Entertainment
        "The gym was crowded today",
        "I watched a documentary last night",
        "The flowers in the garden are blooming",
        "I took a nap after lunch",
        "The concert was amazing last week",
        
        # Random thoughts
        "I wonder what's for dinner",
        "The cat is sleeping on the couch",
        "I need to buy groceries",
        "The TV show was boring",
        "I forgot to water the plants",
        
        # Social media style
        "Just posted a new photo",
        "Having a great day",
        "Can't wait for the weekend",
        "This coffee is amazing",
        "Feeling productive today"
    ]
    
    texts = important_texts + not_important_texts
    labels = [1] * len(important_texts) + [0] * len(not_important_texts)
    
    return texts, labels

def main():
    parser = argparse.ArgumentParser(description='Train NLP Importance Classifier')
    parser.add_argument('--data', type=str, help='Path to custom training data file (CSV or JSON)')
    parser.add_argument('--text-col', type=str, default='text', help='Name of text column in data file')
    parser.add_argument('--label-col', type=str, default='label', help='Name of label column in data file')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Training batch size')
    parser.add_argument('--validation-split', type=float, default=0.2, help='Validation split ratio')
    parser.add_argument('--save-model', type=str, default='nlp_classifier_model.h5', help='Model save path')
    parser.add_argument('--save-tokenizer', type=str, default='tokenizer.pkl', help='Tokenizer save path')
    parser.add_argument('--use-database', action='store_true', help='Use database integration')
    parser.add_argument('--create-sample-data', action='store_true', help='Create and save sample training data')
    
    args = parser.parse_args()
    
    # Create sample data if requested
    if args.create_sample_data:
        texts, labels = create_sample_training_data()
        df = pd.DataFrame({'text': texts, 'label': labels})
        df.to_csv('sample_training_data.csv', index=False)
        print("Sample training data saved to 'sample_training_data.csv'")
        return
    
    # Initialize classifier
    classifier = NLPImportanceClassifier()
    
    # Load training data
    if args.data:
        print(f"Loading custom training data from {args.data}")
        texts, labels = load_custom_data(args.data, args.text_col, args.label_col)
    else:
        print("Using default sample training data")
        texts, labels = create_sample_training_data()
    
    print(f"Training data loaded:")
    print(f"  Total samples: {len(texts)}")
    print(f"  Important samples: {sum(labels)}")
    print(f"  Not important samples: {len(labels) - sum(labels)}")
    print(f"  Important ratio: {sum(labels)/len(labels):.2%}")
    
    # Train the model
    print(f"\nTraining model with {args.epochs} epochs...")
    history = classifier.train(
        texts, labels,
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=args.validation_split
    )
    
    # Save the model
    classifier.save_model(args.save_model, args.save_tokenizer)
    
    # Use database integration if requested
    if args.use_database:
        print("\nInitializing database integration...")
        processor = DatabaseNLPProcessor()
        processor.classifier = classifier
        processor.save_model_metadata(history, texts, labels)
        
        # Test with some sample texts
        test_texts = [
            "Customer email: john.doe@example.com",
            "The weather is sunny today",
            "Order #12345 shipped to 123 Main St",
            "Database backup completed successfully"
        ]
        
        results = processor.process_text_batch(test_texts, source='training_test')
        print("\nTest predictions:")
        for result in results:
            print(f"  {result['text']}: {result['prediction']} ({result['confidence']:.3f})")
    
    # Print training summary
    print(f"\nTraining completed!")
    print(f"Final accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    print(f"Model saved to: {args.save_model}")
    print(f"Tokenizer saved to: {args.save_tokenizer}")

if __name__ == "__main__":
    main() 
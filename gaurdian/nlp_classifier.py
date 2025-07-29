import tensorflow as tf
import numpy as np
import json
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import re

class NLPImportanceClassifier:
    """
    Neural network classifier to determine if natural language text is important for database export.
    Uses LSTM with word embeddings for sequence classification.
    """
    
    def __init__(self, max_words=10000, max_len=200, embedding_dim=128):
        self.max_words = max_words
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        self.tokenizer = None
        self.model = None
        self.class_names = ['Not Important', 'Important']
        
    def preprocess_text(self, text):
        """Clean and preprocess text data."""
        if isinstance(text, str):
            # Convert to lowercase
            text = text.lower()
            # Remove special characters but keep spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            # Remove extra whitespace
            text = ' '.join(text.split())
            return text
        return ""
    
    def prepare_data(self, texts, labels):
        """Prepare data for training."""
        # Preprocess all texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Create and fit tokenizer
        self.tokenizer = Tokenizer(num_words=self.max_words, oov_token='<OOV>')
        self.tokenizer.fit_on_texts(processed_texts)
        
        # Convert texts to sequences
        sequences = self.tokenizer.texts_to_sequences(processed_texts)
        
        # Pad sequences
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len, padding='post', truncating='post')
        
        return padded_sequences, np.array(labels)
    
    def build_model(self):
        """Build the neural network model."""
        self.model = Sequential([
            Embedding(self.max_words, self.embedding_dim, input_length=self.max_len),
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.3),
            Bidirectional(LSTM(32)),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return self.model
    
    def train(self, texts, labels, validation_split=0.2, epochs=50, batch_size=32):
        """Train the model."""
        # Prepare data
        X, y = self.prepare_data(texts, labels)
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42, stratify=y
        )
        
        # Build model
        self.build_model()
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        model_checkpoint = ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, model_checkpoint],
            verbose=1
        )
        
        return history
    
    def predict(self, texts, threshold=0.5):
        """Predict importance of texts."""
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Convert to sequences
        sequences = self.tokenizer.texts_to_sequences(processed_texts)
        
        # Pad sequences
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len, padding='post', truncating='post')
        
        # Make predictions
        predictions = self.model.predict(padded_sequences)
        
        # Convert to binary predictions
        binary_predictions = (predictions > threshold).astype(int)
        
        return {
            'probabilities': predictions.flatten(),
            'predictions': binary_predictions.flatten(),
            'labels': [self.class_names[int(pred)] for pred in binary_predictions.flatten()]
        }
    
    def predict_single(self, text, threshold=0.5):
        """Predict importance of a single text."""
        result = self.predict([text], threshold)
        return {
            'text': text,
            'probability': float(result['probabilities'][0]),
            'confidence': float(result['probabilities'][0]),
            'prediction': result['labels'][0],
            'is_important': bool(result['predictions'][0])
        }
    
    def evaluate(self, texts, labels):
        """Evaluate model performance."""
        predictions = self.predict(texts)
        y_true = np.array(labels)
        y_pred = predictions['predictions']
        
        print("Classification Report:")
        print(classification_report(y_true, y_pred, target_names=self.class_names))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_true, y_pred))
        
        return {
            'classification_report': classification_report(y_true, y_pred, target_names=self.class_names, output_dict=True),
            'confusion_matrix': confusion_matrix(y_true, y_pred)
        }
    
    def save_model(self, model_path='nlp_classifier_model.h5', tokenizer_path='tokenizer.pkl'):
        """Save the trained model and tokenizer."""
        if self.model is not None:
            self.model.save(model_path)
        if self.tokenizer is not None:
            with open(tokenizer_path, 'wb') as f:
                pickle.dump(self.tokenizer, f)
        print(f"Model saved to {model_path}")
        print(f"Tokenizer saved to {tokenizer_path}")
    
    def load_model(self, model_path='nlp_classifier_model.h5', tokenizer_path='tokenizer.pkl'):
        """Load a trained model and tokenizer."""
        self.model = load_model(model_path)
        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)
        print(f"Model loaded from {model_path}")
        print(f"Tokenizer loaded from {tokenizer_path}")

# Example usage and training data generator
def generate_sample_data():
    """Generate sample training data for demonstration."""
    important_texts = [
        "Customer contact information including email and phone number",
        "Sales transaction details with product codes and quantities",
        "User authentication credentials and security tokens",
        "Financial transaction records with amounts and dates",
        "Product inventory levels and stock counts",
        "Customer feedback and satisfaction scores",
        "Order tracking information and delivery status",
        "Payment processing details and transaction IDs",
        "User profile data with preferences and settings",
        "System error logs and debugging information",
        "Database backup schedules and retention policies",
        "API endpoint configurations and access keys",
        "User session data and activity timestamps",
        "Product pricing information and discount codes",
        "Customer support ticket details and resolutions"
    ]
    
    not_important_texts = [
        "The weather is nice today",
        "I had coffee for breakfast",
        "The movie was entertaining",
        "Traffic was heavy this morning",
        "The restaurant had good food",
        "I went for a walk in the park",
        "The book was interesting to read",
        "Music helps me focus while working",
        "The sunset was beautiful yesterday",
        "I enjoy cooking on weekends",
        "The gym was crowded today",
        "I watched a documentary last night",
        "The flowers in the garden are blooming",
        "I took a nap after lunch",
        "The concert was amazing last week"
    ]
    
    texts = important_texts + not_important_texts
    labels = [1] * len(important_texts) + [0] * len(not_important_texts)
    
    return texts, labels

if __name__ == "__main__":
    # Initialize classifier
    classifier = NLPImportanceClassifier()
    
    # Generate sample data
    texts, labels = generate_sample_data()
    
    print("Training NLP Importance Classifier...")
    print(f"Total samples: {len(texts)}")
    print(f"Important samples: {sum(labels)}")
    print(f"Not important samples: {len(labels) - sum(labels)}")
    
    # Train the model
    history = classifier.train(texts, labels, epochs=20)
    
    # Test predictions
    test_texts = [
        "Customer email: john.doe@example.com",
        "The weather is sunny today",
        "Order #12345 shipped to 123 Main St",
        "I like pizza",
        "Database backup completed successfully",
        "The movie was good"
    ]
    
    print("\nTesting predictions:")
    for text in test_texts:
        result = classifier.predict_single(text)
        print(f"Text: {text}")
        print(f"Prediction: {result['prediction']} (Probability: {result['probability']:.3f})")
        print()
    
    # Save the model
    classifier.save_model() 
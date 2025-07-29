import sqlite3
import json
import pandas as pd
from datetime import datetime
from nlp_classifier import NLPImportanceClassifier

class DatabaseNLPProcessor:
    """
    Utility class for processing natural language data and determining what's important for database export.
    """
    
    def __init__(self, db_path='nlp_data.db'):
        self.db_path = db_path
        self.classifier = NLPImportanceClassifier()
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table for storing processed text data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT NOT NULL,
                processed_text TEXT NOT NULL,
                importance_score REAL,
                is_important BOOLEAN,
                confidence REAL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT
            )
        ''')
        
        # Table for storing model metadata
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_version TEXT,
                training_date TIMESTAMP,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                total_samples INTEGER,
                important_samples INTEGER,
                not_important_samples INTEGER
            )
        ''')
        
        # Table for storing training data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                label INTEGER NOT NULL,
                category TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_or_train_model(self, model_path='nlp_classifier_model.h5', tokenizer_path='tokenizer.pkl'):
        """Load existing model or train a new one."""
        try:
            self.classifier.load_model(model_path, tokenizer_path)
            print("Loaded existing model successfully.")
        except FileNotFoundError:
            print("No existing model found. Training new model...")
            self.train_model()
    
    def train_model(self, custom_data=None):
        """Train the model with sample data or custom data."""
        if custom_data is None:
            # Use sample data
            from nlp_classifier import generate_sample_data
            texts, labels = generate_sample_data()
        else:
            texts, labels = custom_data
        
        # Train the model
        history = self.classifier.train(texts, labels, epochs=20)
        
        # Save model metadata
        self.save_model_metadata(history, texts, labels)
        
        return history
    
    def save_model_metadata(self, history, texts, labels):
        """Save model training metadata to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get final metrics
        final_accuracy = history.history['accuracy'][-1]
        final_precision = history.history['precision'][-1]
        final_recall = history.history['recall'][-1]
        final_f1 = 2 * (final_precision * final_recall) / (final_precision + final_recall)
        
        cursor.execute('''
            INSERT INTO model_metadata 
            (model_version, training_date, accuracy, precision, recall, f1_score, 
             total_samples, important_samples, not_important_samples)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            '1.0',
            datetime.now(),
            final_accuracy,
            final_precision,
            final_recall,
            final_f1,
            len(texts),
            sum(labels),
            len(labels) - sum(labels)
        ))
        
        conn.commit()
        conn.close()
    
    def process_text_batch(self, texts, source='unknown', threshold=0.5):
        """Process a batch of texts and store results in database."""
        if self.classifier.model is None:
            raise ValueError("Model not trained. Please train or load the model first.")
        
        # Get predictions
        predictions = self.classifier.predict(texts, threshold)
        
        # Store results in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        results = []
        for i, text in enumerate(texts):
            processed_text = self.classifier.preprocess_text(text)
            importance_score = float(predictions['probabilities'][i])
            is_important = bool(predictions['predictions'][i])
            
            cursor.execute('''
                INSERT INTO processed_texts 
                (original_text, processed_text, importance_score, is_important, 
                 confidence, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (text, processed_text, importance_score, is_important, importance_score, source))
            
            results.append({
                'text': text,
                'processed_text': processed_text,
                'importance_score': importance_score,
                'is_important': is_important,
                'confidence': importance_score,
                'source': source
            })
        
        conn.commit()
        conn.close()
        
        return results
    
    def get_important_texts(self, limit=100, min_confidence=0.7):
        """Retrieve important texts from database."""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT original_text, importance_score, confidence, source, created_at
            FROM processed_texts
            WHERE is_important = 1 AND confidence >= ?
            ORDER BY importance_score DESC
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=(min_confidence, limit))
        conn.close()
        
        return df
    
    def get_statistics(self):
        """Get processing statistics from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total processed texts
        cursor.execute('SELECT COUNT(*) FROM processed_texts')
        total_texts = cursor.fetchone()[0]
        
        # Important texts
        cursor.execute('SELECT COUNT(*) FROM processed_texts WHERE is_important = 1')
        important_texts = cursor.fetchone()[0]
        
        # Average confidence
        cursor.execute('SELECT AVG(confidence) FROM processed_texts')
        avg_confidence = cursor.fetchone()[0]
        
        # Recent activity
        cursor.execute('''
            SELECT COUNT(*) FROM processed_texts 
            WHERE created_at >= datetime('now', '-24 hours')
        ''')
        recent_activity = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_texts': total_texts,
            'important_texts': important_texts,
            'not_important_texts': total_texts - important_texts,
            'importance_ratio': important_texts / total_texts if total_texts > 0 else 0,
            'avg_confidence': avg_confidence,
            'recent_activity_24h': recent_activity
        }
    
    def export_important_data(self, output_format='json', file_path=None):
        """Export important data in various formats."""
        important_data = self.get_important_texts(limit=1000)
        
        if output_format.lower() == 'json':
            if file_path is None:
                file_path = f'important_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            export_data = []
            for _, row in important_data.iterrows():
                export_data.append({
                    'text': row['original_text'],
                    'importance_score': row['importance_score'],
                    'confidence': row['confidence'],
                    'source': row['source'],
                    'timestamp': row['created_at']
                })
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        elif output_format.lower() == 'csv':
            if file_path is None:
                file_path = f'important_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
            important_data.to_csv(file_path, index=False)
        
        print(f"Exported {len(important_data)} important records to {file_path}")
        return file_path
    
    def add_training_data(self, texts, labels, categories=None, sources=None):
        """Add new training data to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for i, (text, label) in enumerate(zip(texts, labels)):
            category = categories[i] if categories else None
            source = sources[i] if sources else None
            
            cursor.execute('''
                INSERT INTO training_data (text, label, category, source)
                VALUES (?, ?, ?, ?)
            ''', (text, label, category, source))
        
        conn.commit()
        conn.close()
        print(f"Added {len(texts)} training samples to database")

# Example usage
if __name__ == "__main__":
    # Initialize processor
    processor = DatabaseNLPProcessor()
    
    # Load or train model
    processor.load_or_train_model()
    
    # Process some sample texts
    sample_texts = [
        "Customer email: john.doe@example.com",
        "The weather is sunny today",
        "Order #12345 shipped to 123 Main St",
        "I like pizza",
        "Database backup completed successfully",
        "The movie was good",
        "User authentication failed for account ID 45678",
        "Payment processed for transaction #98765",
        "The flowers are blooming in the garden",
        "System error: Connection timeout on port 8080"
    ]
    
    results = processor.process_text_batch(sample_texts, source='example')
    
    # Print results
    print("Processing Results:")
    for result in results:
        print(f"Text: {result['text'][:50]}...")
        print(f"Important: {result['is_important']} (Confidence: {result['confidence']:.3f})")
        print()
    
    # Get statistics
    stats = processor.get_statistics()
    print("Database Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Export important data
    processor.export_important_data(output_format='json') 
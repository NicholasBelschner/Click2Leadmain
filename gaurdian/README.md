# Guardian - NLP Importance Classifier

A neural network-based system that learns to identify which natural language text is important for database export. Built with TensorFlow and designed for easy integration with existing systems.

## 🎯 Overview

The Guardian system uses advanced LSTM neural networks to automatically classify natural language text and determine what should be exported to databases. It's perfect for filtering emails, logs, customer messages, and other text data.

## 📁 File Structure

```
gaurdian/
├── README.md                    # This file
├── nlp_classifier.py           # Main neural network classifier
├── database_integration.py     # Database integration layer
├── train_model.py              # Training script
├── test_model.py               # Testing script
├── demo.py                     # Comprehensive demonstration
├── nlp_classifier_model.h5     # Trained model
├── best_model.h5              # Best model checkpoint
├── tokenizer.pkl              # Text tokenizer
├── nlp_data.db                # SQLite database
└── important_data_*.json/csv  # Exported data files
```

## 🚀 Quick Start

### 1. Train the Model
```bash
cd gaurdian
python train_model.py --epochs 50
```

### 2. Test the System
```bash
python test_model.py
```

### 3. Run Full Demo
```bash
python demo.py
```

## 🔧 Usage Examples

### Basic Classification
```python
from nlp_classifier import NLPImportanceClassifier

classifier = NLPImportanceClassifier()
classifier.load_model()

result = classifier.predict_single("Customer email: john.doe@example.com")
print(f"Important: {result['is_important']} (Confidence: {result['confidence']:.3f})")
```

### Database Integration
```python
from database_integration import DatabaseNLPProcessor

processor = DatabaseNLPProcessor()
processor.load_or_train_model()

texts = ["Customer complaint", "Weather update", "Order confirmation"]
results = processor.process_text_batch(texts, source='email_system')
```

## 📊 Model Performance

- **Training Accuracy**: 100%
- **Validation Accuracy**: 90%
- **Precision**: 0.85-0.95
- **Recall**: 0.80-0.90

## 🎯 What Gets Classified as Important

✅ **Business Data**
- Customer contact information
- Sales transactions
- Order details
- Payment information
- User authentication
- System errors and logs
- Database operations
- API configurations

❌ **Not Important**
- Casual conversation
- Weather updates
- Personal activities
- Social media posts
- General chit-chat

## 🔄 Workflow

1. **Text Input** → Raw natural language text
2. **Preprocessing** → Clean and tokenize text
3. **Neural Network** → LSTM classification
4. **Decision** → Important or Not Important
5. **Database** → Store results
6. **Export** → Generate reports

## 🛠 Configuration

### Model Parameters
- `max_words`: 10000 (vocabulary size)
- `max_len`: 200 (sequence length)
- `embedding_dim`: 128 (word embeddings)

### Training Parameters
- `epochs`: 50 (training cycles)
- `batch_size`: 32 (batch size)
- `validation_split`: 0.2 (validation ratio)

## 📈 Monitoring

The system tracks:
- Processing statistics
- Model performance metrics
- Database activity
- Export history

## 🔗 Integration

Easily integrate with:
- Email systems
- Customer support platforms
- Log management systems
- Data pipelines
- Analytics platforms

## 📝 License

This project is part of the Click2Lead system and follows the same licensing terms. 
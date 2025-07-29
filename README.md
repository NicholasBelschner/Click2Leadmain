# Click2Lead - NLP Importance Classifier

A neural network-based system that learns to identify which natural language text is important for database export. Built with TensorFlow and designed for easy integration with existing systems.

## 📁 Project Structure

```
Click2Lead/
├── gaurdian/                    # NLP Classifier System
│   ├── README.md               # Guardian system documentation
│   ├── nlp_classifier.py       # Main neural network classifier
│   ├── database_integration.py # Database integration layer
│   ├── train_model.py          # Training script
│   ├── test_model.py           # Testing script
│   ├── demo.py                 # Comprehensive demonstration
│   └── [model files & data]    # Trained models and databases
├── agents/                     # Multi-agent conversation system
│   ├── README.md               # Agent system documentation
│   ├── broker.py               # Broker agent coordinator
│   ├── employee1.py            # First conversation participant
│   ├── employee2.py            # Second conversation participant
│   ├── agent_orchestrator.py   # Main orchestrator
│   ├── demo_agents.py          # Demo scenarios
│   └── SYSTEM_SUMMARY.md       # Implementation summary
├── frontend/                   # Web interface
│   ├── README.md               # Frontend documentation
│   ├── index.html              # Main HTML page
│   ├── styles.css              # CSS styling
│   ├── script.js               # JavaScript functionality
│   └── server.py               # Flask backend server
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### NLP Classifier System
The NLP classifier system is located in the `gaurdian/` folder. See the [Guardian README](gaurdian/README.md) for detailed documentation.

```bash
cd gaurdian
python train_model.py --epochs 50
python demo.py
```

### Multi-Agent Conversation System
The agent conversation system is located in the `agents/` folder. See the [Agents README](agents/README.md) for detailed documentation.

```bash
cd agents
python demo_agents.py
```

### Web Frontend
The web interface is located in the `frontend/` folder. See the [Frontend README](frontend/README.md) for detailed documentation.

```bash
cd frontend
python server.py
# Then open http://localhost:5000 in your browser
```

## Features

- **LSTM-based Neural Network**: Uses bidirectional LSTM layers with word embeddings for accurate text classification
- **Database Integration**: Built-in SQLite database for storing processed texts and model metadata
- **Flexible Training**: Support for custom training data or built-in sample data
- **Export Capabilities**: Export important data in JSON or CSV formats
- **Real-time Processing**: Process text batches with confidence scores
- **Model Persistence**: Save and load trained models for production use

## Installation

1. **Activate your virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Train the Model

Train with default sample data:
```bash
python train_model.py
```

Train with custom data:
```bash
python train_model.py --data your_data.csv --text-col text --label-col label
```

Create sample training data:
```bash
python train_model.py --create-sample-data
```

### 2. Use the Classifier

```python
from nlp_classifier import NLPImportanceClassifier

# Load trained model
classifier = NLPImportanceClassifier()
classifier.load_model()

# Predict importance of text
result = classifier.predict_single("Customer email: john.doe@example.com")
print(f"Important: {result['is_important']} (Confidence: {result['confidence']:.3f})")
```

### 3. Database Integration

```python
from database_integration import DatabaseNLPProcessor

# Initialize processor
processor = DatabaseNLPProcessor()
processor.load_or_train_model()

# Process batch of texts
texts = [
    "Customer email: john.doe@example.com",
    "The weather is sunny today",
    "Order #12345 shipped to 123 Main St"
]

results = processor.process_text_batch(texts, source='email_processing')

# Export important data
processor.export_important_data(output_format='json')
```

## Model Architecture

The neural network uses:
- **Embedding Layer**: Converts words to dense vectors
- **Bidirectional LSTM**: Captures sequential patterns in both directions
- **Dropout Layers**: Prevents overfitting
- **Dense Layers**: Final classification with sigmoid activation

## Training Data Format

### CSV Format
```csv
text,label
"Customer email: john.doe@example.com",1
"The weather is sunny today",0
"Order #12345 shipped to 123 Main St",1
```

### JSON Format
```json
[
  {"text": "Customer email: john.doe@example.com", "label": 1},
  {"text": "The weather is sunny today", "label": 0},
  {"text": "Order #12345 shipped to 123 Main St", "label": 1}
]
```

## Database Schema

### processed_texts
- `id`: Primary key
- `original_text`: Original input text
- `processed_text`: Preprocessed text
- `importance_score`: Model confidence score
- `is_important`: Binary classification result
- `confidence`: Confidence level
- `category`: Optional category
- `created_at`: Timestamp
- `source`: Data source identifier

### model_metadata
- Training metrics and model version information

### training_data
- Stored training examples for future retraining

## API Usage

### Basic Classification
```python
# Single text prediction
result = classifier.predict_single("Your text here")

# Batch prediction
texts = ["Text 1", "Text 2", "Text 3"]
results = classifier.predict(texts)
```

### Database Operations
```python
# Get statistics
stats = processor.get_statistics()

# Get important texts
important = processor.get_important_texts(limit=100, min_confidence=0.7)

# Export data
processor.export_important_data(output_format='json', file_path='export.json')
```

## Configuration

### Model Parameters
- `max_words`: Maximum vocabulary size (default: 10000)
- `max_len`: Maximum sequence length (default: 200)
- `embedding_dim`: Word embedding dimensions (default: 128)

### Training Parameters
- `epochs`: Number of training epochs (default: 50)
- `batch_size`: Training batch size (default: 32)
- `validation_split`: Validation data ratio (default: 0.2)

## Examples

### Example 1: Email Processing
```python
emails = [
    "Customer inquiry about product pricing",
    "Meeting reminder for tomorrow",
    "Order confirmation #12345",
    "Lunch plans with colleague"
]

processor = DatabaseNLPProcessor()
processor.load_or_train_model()
results = processor.process_text_batch(emails, source='email_system')
```

### Example 2: Log Analysis
```python
logs = [
    "ERROR: Database connection failed",
    "INFO: User login successful",
    "DEBUG: Processing request",
    "WARN: High memory usage detected"
]

classifier = NLPImportanceClassifier()
classifier.load_model()

for log in logs:
    result = classifier.predict_single(log)
    if result['is_important']:
        print(f"Important log: {log}")
```

## Performance

Typical performance metrics:
- **Accuracy**: 90-95% on balanced datasets
- **Precision**: 0.85-0.95 for important class
- **Recall**: 0.80-0.90 for important class
- **Training Time**: 2-5 minutes on CPU, 30-60 seconds on GPU

## Troubleshooting

### Common Issues

1. **Memory Issues**: Reduce `max_words` or `max_len` parameters
2. **Overfitting**: Increase dropout rates or reduce model complexity
3. **Poor Performance**: Add more training data or adjust class balance
4. **Slow Training**: Use GPU acceleration or reduce batch size

### Model Loading Issues
```python
# Ensure model files exist
import os
if not os.path.exists('nlp_classifier_model.h5'):
    print("Model not found. Please train the model first.")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
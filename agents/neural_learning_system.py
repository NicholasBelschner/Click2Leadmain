#!/usr/bin/env python3
"""
Neural Network Learning System for Dynamic Agent Conversations
Learns from user interactions to improve responses and agent selection
"""

import os
import json
import pickle
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import sqlite3
from collections import defaultdict
import threading
import time

# Neural network imports
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    from transformers import AutoTokenizer, AutoModel
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. Neural learning will be disabled.")
    # Create placeholder nn module for when PyTorch is not available
    class nn:
        class Module:
            pass
        class Embedding:
            def __init__(self, *args, **kwargs):
                pass
        class LSTM:
            def __init__(self, *args, **kwargs):
                pass
        class MultiheadAttention:
            def __init__(self, *args, **kwargs):
                pass
        class Dropout:
            def __init__(self, *args, **kwargs):
                pass
        class Linear:
            def __init__(self, *args, **kwargs):
                pass
        class ReLU:
            def __init__(self, *args, **kwargs):
                pass

# Create placeholder torch module
if not TORCH_AVAILABLE:
    class torch:
        @staticmethod
        def mean(tensor, dim=None):
            return 0.0

class UserInteractionData:
    """Data structure for storing user interaction data"""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.interactions = []
        self.preferences = {}
        self.successful_patterns = []
        self.agent_preferences = defaultdict(int)
        self.response_ratings = []
        
    def add_interaction(self, prompt: str, response: str, response_type: str, 
                       agents_created: List[str] = None, user_feedback: float = None):
        """Add a new user interaction"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'response': response,
            'response_type': response_type,
            'agents_created': agents_created or [],
            'user_feedback': user_feedback,
            'success_score': self._calculate_success_score(response_type, user_feedback)
        }
        self.interactions.append(interaction)
        
        # Update preferences based on successful interactions
        if user_feedback and user_feedback > 0.7:  # High success threshold
            self.successful_patterns.append(interaction)
            if agents_created:
                for agent in agents_created:
                    self.agent_preferences[agent] += 1
    
    def _calculate_success_score(self, response_type: str, user_feedback: float) -> float:
        """Calculate success score for an interaction"""
        base_score = 0.5
        
        # Adjust based on response type
        if response_type == 'agent_creation':
            base_score += 0.2
        elif response_type == 'exchange':
            base_score += 0.3
        elif response_type == 'help':
            base_score += 0.1
            
        # Adjust based on user feedback
        if user_feedback is not None:
            base_score = (base_score + user_feedback) / 2
            
        return min(base_score, 1.0)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get current user preferences based on interaction history"""
        if not self.interactions:
            return {}
            
        preferences = {
            'preferred_agents': dict(self.agent_preferences),
            'response_style': self._analyze_response_style(),
            'common_topics': self._extract_common_topics(),
            'interaction_patterns': self._analyze_patterns()
        }
        return preferences
    
    def _analyze_response_style(self) -> Dict[str, float]:
        """Analyze user's preferred response style"""
        if not self.interactions:
            return {}
            
        response_types = [i['response_type'] for i in self.interactions]
        type_counts = defaultdict(int)
        for rt in response_types:
            type_counts[rt] += 1
            
        total = len(response_types)
        return {k: v/total for k, v in type_counts.items()}
    
    def _extract_common_topics(self) -> List[str]:
        """Extract common topics from user interactions"""
        topics = []
        for interaction in self.interactions:
            prompt = interaction['prompt'].lower()
            # Extract potential topics
            if 'fitness' in prompt or 'workout' in prompt:
                topics.append('fitness')
            if 'nutrition' in prompt or 'diet' in prompt:
                topics.append('nutrition')
            if 'business' in prompt or 'project' in prompt:
                topics.append('business')
            if 'technology' in prompt or 'development' in prompt:
                topics.append('technology')
                
        return list(set(topics))
    
    def _analyze_patterns(self) -> Dict[str, Any]:
        """Analyze interaction patterns"""
        if len(self.interactions) < 2:
            return {}
            
        patterns = {
            'avg_prompt_length': np.mean([len(i['prompt']) for i in self.interactions]),
            'preferred_agent_count': np.mean([len(i['agents_created']) for i in self.interactions if i['agents_created']]),
            'success_rate': np.mean([i['success_score'] for i in self.interactions])
        }
        return patterns

if TORCH_AVAILABLE:
    class IntentClassificationNetwork(nn.Module):
        """Neural network for classifying user intent"""
        
        def __init__(self, vocab_size: int, embedding_dim: int = 128, hidden_dim: int = 256, num_classes: int = 8):
            super(IntentClassificationNetwork, self).__init__()
            
            self.embedding = nn.Embedding(vocab_size, embedding_dim)
            self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, bidirectional=True)
            self.attention = nn.MultiheadAttention(hidden_dim * 2, num_heads=8)
            self.dropout = nn.Dropout(0.3)
            self.fc1 = nn.Linear(hidden_dim * 2, hidden_dim)
            self.fc2 = nn.Linear(hidden_dim, num_classes)
            self.relu = nn.ReLU()
            
        def forward(self, x):
            # Embedding
            embedded = self.embedding(x)
            
            # LSTM
            lstm_out, _ = self.lstm(embedded)
            
            # Attention
            attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
            
            # Global average pooling
            pooled = torch.mean(attn_out, dim=1)
            
            # Classification
            out = self.dropout(pooled)
            out = self.relu(self.fc1(out))
            out = self.dropout(out)
            out = self.fc2(out)
            
            return out

    class ResponseOptimizationNetwork(nn.Module):
        """Neural network for optimizing response generation"""
        
        def __init__(self, input_dim: int, hidden_dim: int = 256, output_dim: int = 64):
            super(ResponseOptimizationNetwork, self).__init__()
            
            self.fc1 = nn.Linear(input_dim, hidden_dim)
            self.fc2 = nn.Linear(hidden_dim, hidden_dim)
            self.fc3 = nn.Linear(hidden_dim, output_dim)
            self.dropout = nn.Dropout(0.3)
            self.relu = nn.ReLU()
            
        def forward(self, x):
            out = self.relu(self.fc1(x))
            out = self.dropout(out)
            out = self.relu(self.fc2(out))
            out = self.dropout(out)
            out = self.fc3(out)
            return out
else:
    # Placeholder classes when PyTorch is not available
    class IntentClassificationNetwork:
        def __init__(self, *args, **kwargs):
            pass
    
    class ResponseOptimizationNetwork:
        def __init__(self, *args, **kwargs):
            pass

class NeuralLearningSystem:
    """Main neural learning system for the agent conversation system"""
    
    def __init__(self, data_dir: str = "neural_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data storage
        self.user_data = UserInteractionData()
        self.vocab = {}
        self.intent_classes = [
            'agent_creation', 'conversation_management', 'help_request', 
            'status_check', 'general_conversation', 'exchange_request',
            'agent_suggestion', 'system_inquiry'
        ]
        
        # Neural networks
        self.intent_classifier = None
        self.response_optimizer = None
        self.tokenizer = None
        
        # Training state
        self.is_training = False
        self.training_lock = threading.Lock()
        
        # Initialize neural networks if PyTorch is available
        if TORCH_AVAILABLE:
            self._initialize_networks()
        
        # Load existing data
        self._load_data()
    
    def _initialize_networks(self):
        """Initialize neural networks"""
        try:
            # Initialize tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
            
            # Intent classification network
            vocab_size = len(self.tokenizer)
            self.intent_classifier = IntentClassificationNetwork(
                vocab_size=vocab_size,
                embedding_dim=128,
                hidden_dim=256,
                num_classes=len(self.intent_classes)
            )
            
            # Response optimization network
            input_dim = 128 + len(self.intent_classes) + 50  # prompt_embedding + intent + context
            self.response_optimizer = ResponseOptimizationNetwork(
                input_dim=input_dim,
                hidden_dim=256,
                output_dim=64
            )
            
            # Load pre-trained models if they exist
            self._load_models()
            
        except Exception as e:
            print(f"Error initializing neural networks: {e}")
            self.intent_classifier = None
            self.response_optimizer = None
    
    def _load_models(self):
        """Load pre-trained models"""
        try:
            intent_path = os.path.join(self.data_dir, "intent_classifier.pth")
            response_path = os.path.join(self.data_dir, "response_optimizer.pth")
            
            if os.path.exists(intent_path) and self.intent_classifier:
                self.intent_classifier.load_state_dict(torch.load(intent_path))
                print("✅ Loaded pre-trained intent classifier")
                
            if os.path.exists(response_path) and self.response_optimizer:
                self.response_optimizer.load_state_dict(torch.load(response_path))
                print("✅ Loaded pre-trained response optimizer")
                
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def _save_models(self):
        """Save trained models"""
        try:
            if self.intent_classifier:
                torch.save(self.intent_classifier.state_dict(), 
                          os.path.join(self.data_dir, "intent_classifier.pth"))
            if self.response_optimizer:
                torch.save(self.response_optimizer.state_dict(), 
                          os.path.join(self.data_dir, "response_optimizer.pth"))
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def _load_data(self):
        """Load existing interaction data"""
        try:
            data_path = os.path.join(self.data_dir, "user_data.pkl")
            if os.path.exists(data_path):
                with open(data_path, 'rb') as f:
                    self.user_data = pickle.load(f)
                print(f"✅ Loaded {len(self.user_data.interactions)} interactions")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _save_data(self):
        """Save interaction data"""
        try:
            data_path = os.path.join(self.data_dir, "user_data.pkl")
            with open(data_path, 'wb') as f:
                pickle.dump(self.user_data, f)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def predict_intent(self, prompt: str) -> Tuple[str, float]:
        """Predict user intent from prompt"""
        if not self.intent_classifier or not TORCH_AVAILABLE:
            return self._rule_based_intent(prompt), 0.8
        
        try:
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.intent_classifier(inputs['input_ids'])
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
            
            return self.intent_classes[predicted_class], confidence
            
        except Exception as e:
            print(f"Error predicting intent: {e}")
            return self._rule_based_intent(prompt), 0.8
    
    def _rule_based_intent(self, prompt: str) -> str:
        """Rule-based intent classification as fallback"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['create', 'agent', 'team', 'build']):
            return 'agent_creation'
        elif any(word in prompt_lower for word in ['exchange', 'next', 'continue']):
            return 'conversation_management'
        elif any(word in prompt_lower for word in ['help', 'what can you do']):
            return 'help_request'
        elif any(word in prompt_lower for word in ['status', 'system', 'health']):
            return 'status_check'
        else:
            return 'general_conversation'
    
    def optimize_response(self, prompt: str, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize response based on learned patterns"""
        if not self.response_optimizer or not TORCH_AVAILABLE:
            return self._rule_based_optimization(prompt, intent, context)
        
        try:
            # Create input vector
            prompt_embedding = self._get_prompt_embedding(prompt)
            intent_vector = self._get_intent_vector(intent)
            context_vector = self._get_context_vector(context)
            
            # Check if any vectors are None (PyTorch not available)
            if prompt_embedding is None or intent_vector is None or context_vector is None:
                return self._rule_based_optimization(prompt, intent, context)
            
            # Combine vectors
            combined_input = torch.cat([prompt_embedding, intent_vector, context_vector], dim=1)
            
            # Get optimization
            with torch.no_grad():
                optimization = self.response_optimizer(combined_input)
            
            return self._interpret_optimization(optimization)
            
        except Exception as e:
            print(f"Error optimizing response: {e}")
            return self._rule_based_optimization(prompt, intent, context)
    
    def _rule_based_optimization(self, prompt: str, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based response optimization as fallback"""
        optimization = {
            'response_style': 'direct',
            'agent_suggestion': [],
            'confidence_boost': 0.0,
            'personalization_level': 0.5
        }
        
        # Apply user preferences
        user_prefs = self.user_data.get_user_preferences()
        if user_prefs.get('preferred_agents'):
            optimization['agent_suggestion'] = list(user_prefs['preferred_agents'].keys())[:3]
        
        return optimization
    
    def _get_prompt_embedding(self, prompt: str):
        """Get prompt embedding"""
        if not TORCH_AVAILABLE:
            return None
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                embedding = self.intent_classifier.embedding(inputs['input_ids'])
                return torch.mean(embedding, dim=1)
        except:
            return torch.zeros(1, 128)
    
    def _get_intent_vector(self, intent: str):
        """Get intent one-hot vector"""
        if not TORCH_AVAILABLE:
            return None
        intent_idx = self.intent_classes.index(intent) if intent in self.intent_classes else 0
        vector = torch.zeros(1, len(self.intent_classes))
        vector[0][intent_idx] = 1.0
        return vector
    
    def _get_context_vector(self, context: Dict[str, Any]):
        """Get context vector"""
        if not TORCH_AVAILABLE:
            return None
        # Simple context encoding
        vector = torch.zeros(1, 50)
        if context.get('current_agents'):
            vector[0][0] = len(context['current_agents']) / 10.0
        if context.get('conversation_length'):
            vector[0][1] = min(context['conversation_length'] / 20.0, 1.0)
        return vector
    
    def _interpret_optimization(self, optimization) -> Dict[str, Any]:
        """Interpret optimization output"""
        if not TORCH_AVAILABLE:
            return {
                'response_style': 'direct',
                'agent_suggestion': [],
                'confidence_boost': 0.0,
                'personalization_level': 0.5
            }
        # Simple interpretation of the 64-dimensional output
        values = optimization[0].numpy()
        
        return {
            'response_style': 'direct' if values[0] > 0.5 else 'detailed',
            'agent_suggestion': [],
            'confidence_boost': float(values[1]),
            'personalization_level': float(values[2])
        }
    
    def learn_from_interaction(self, prompt: str, response: str, response_type: str, 
                              agents_created: List[str] = None, user_feedback: float = None):
        """Learn from a user interaction"""
        # Store interaction
        self.user_data.add_interaction(prompt, response, response_type, agents_created, user_feedback)
        
        # Save data
        self._save_data()
        
        # Trigger training if enough data
        if len(self.user_data.interactions) % 10 == 0:  # Train every 10 interactions
            self._train_networks()
    
    def _train_networks(self):
        """Train neural networks on collected data"""
        if not TORCH_AVAILABLE or len(self.user_data.interactions) < 5:
            return
        
        with self.training_lock:
            if self.is_training:
                return
            
            self.is_training = True
            
            try:
                print("🧠 Training neural networks...")
                
                # Prepare training data
                training_data = self._prepare_training_data()
                if not training_data:
                    return
                
                # Train intent classifier
                self._train_intent_classifier(training_data)
                
                # Train response optimizer
                self._train_response_optimizer(training_data)
                
                # Save models
                self._save_models()
                
                print("✅ Neural networks trained successfully")
                
            except Exception as e:
                print(f"Error training networks: {e}")
            finally:
                self.is_training = False
    
    def _prepare_training_data(self) -> List[Dict[str, Any]]:
        """Prepare training data from interactions"""
        training_data = []
        
        for interaction in self.user_data.interactions:
            if interaction['success_score'] > 0.3:  # Only use reasonably successful interactions
                training_data.append({
                    'prompt': interaction['prompt'],
                    'intent': interaction['response_type'],
                    'success_score': interaction['success_score'],
                    'agents_created': interaction['agents_created']
                })
        
        return training_data
    
    def _train_intent_classifier(self, training_data: List[Dict[str, Any]]):
        """Train the intent classification network"""
        if not self.intent_classifier or len(training_data) < 3:
            return
        
        try:
            # Prepare data
            prompts = [item['prompt'] for item in training_data]
            intents = [self.intent_classes.index(item['intent']) if item['intent'] in self.intent_classes else 0 
                      for item in training_data]
            
            # Tokenize
            inputs = self.tokenizer(prompts, padding=True, truncation=True, return_tensors="pt")
            labels = torch.tensor(intents)
            
            # Training setup
            optimizer = optim.Adam(self.intent_classifier.parameters(), lr=0.001)
            criterion = nn.CrossEntropyLoss()
            
            # Training loop
            self.intent_classifier.train()
            for epoch in range(5):  # Small number of epochs for online learning
                optimizer.zero_grad()
                outputs = self.intent_classifier(inputs['input_ids'])
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
        except Exception as e:
            print(f"Error training intent classifier: {e}")
    
    def _train_response_optimizer(self, training_data: List[Dict[str, Any]]):
        """Train the response optimization network"""
        if not self.response_optimizer or len(training_data) < 3:
            return
        
        try:
            # Prepare data
            inputs = []
            targets = []
            
            for item in training_data:
                prompt_embedding = self._get_prompt_embedding(item['prompt'])
                intent_vector = self._get_intent_vector(item['intent'])
                context_vector = self._get_context_vector({'success_score': item['success_score']})
                
                combined_input = torch.cat([prompt_embedding, intent_vector, context_vector], dim=1)
                inputs.append(combined_input)
                
                # Target: success score repeated across output dimensions
                target = torch.full((1, 64), item['success_score'])
                targets.append(target)
            
            if not inputs:
                return
            
            inputs = torch.cat(inputs, dim=0)
            targets = torch.cat(targets, dim=0)
            
            # Training setup
            optimizer = optim.Adam(self.response_optimizer.parameters(), lr=0.001)
            criterion = nn.MSELoss()
            
            # Training loop
            self.response_optimizer.train()
            for epoch in range(5):
                optimizer.zero_grad()
                outputs = self.response_optimizer(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                
        except Exception as e:
            print(f"Error training response optimizer: {e}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        stats = {
            'total_interactions': len(self.user_data.interactions),
            'successful_patterns': len(self.user_data.successful_patterns),
            'preferred_agents': dict(self.user_data.agent_preferences),
            'average_success_rate': np.mean([i['success_score'] for i in self.user_data.interactions]) if self.user_data.interactions else 0,
            'neural_networks_available': TORCH_AVAILABLE and self.intent_classifier is not None,
            'is_training': self.is_training
        }
        return stats 
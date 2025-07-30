// Agent Conversation System Frontend - Minimal Prompt Interface
class AgentConversationUI {
    constructor() {
        this.currentConversation = null;
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeCodeTabs();
        this.startRealTimeUpdates();
        this.checkSystemStatus();
    }

    initializeElements() {
        // Prompt interface elements
        this.promptInput = document.getElementById('prompt-input');
        this.sendButton = document.getElementById('send-prompt');
        this.conversationArea = document.getElementById('conversation-area');
        
        // Agent role displays (for left panel)
        this.employee1RoleDisplay = document.getElementById('employee1-role-display');
        this.employee2RoleDisplay = document.getElementById('employee2-role-display');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingText = document.getElementById('loading-text');
    }

    bindEvents() {
        // Send prompt
        this.sendButton.addEventListener('click', () => this.sendPrompt());
        
        // Enter key to send
        this.promptInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendPrompt();
            }
        });

        // Auto-resize textarea
        this.promptInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
    }

    initializeCodeTabs() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.dataset.tab;
                
                // Remove active class from all tabs
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab
                button.classList.add('active');
                document.getElementById(targetTab).classList.add('active');
                
                // Highlight syntax
                Prism.highlightAll();
            });
        });
    }

    startRealTimeUpdates() {
        // Simulate real-time code updates
        setInterval(() => {
            this.updateCodeStatus();
        }, 3000);

        // Simulate agent activity
        setInterval(() => {
            this.simulateAgentActivity();
        }, 5000);
    }

    updateCodeStatus() {
        const statusElements = document.querySelectorAll('.code-status');
        const statuses = ['Active', 'Running', 'Processing', 'Connected', 'Ready'];
        
        statusElements.forEach(element => {
            if (Math.random() > 0.7) {
                const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
                element.textContent = newStatus;
                
                // Add a brief highlight effect with grey
                element.style.color = '#333333';
                element.style.background = '#cccccc';
                setTimeout(() => {
                    element.style.color = '';
                    element.style.background = '';
                }, 500);
            }
        });
    }

    simulateAgentActivity() {
        const agents = document.querySelectorAll('.agent-card');
        agents.forEach(agent => {
            if (Math.random() > 0.8) {
                // Simulate agent activity
                const indicator = agent.querySelector('.agent-status-indicator');
                indicator.style.animation = 'pulse 0.5s ease-in-out';
                setTimeout(() => {
                    indicator.style.animation = 'pulse 2s infinite';
                }, 500);
            }
        });
    }

    async checkSystemStatus() {
        try {
            // Check if we can access the agent system
            const response = await fetch('/api/status', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.updateStatusIndicators('connected');
            } else {
                this.updateStatusIndicators('demo');
            }
        } catch (error) {
            console.log('Running in demo mode - no backend connection');
            this.updateStatusIndicators('demo');
        }
    }

    updateStatusIndicators(status) {
        const statusDots = document.querySelectorAll('.status-dot');
        const statusTexts = document.querySelectorAll('.status-text');
        
        if (status === 'connected') {
            statusDots.forEach(dot => {
                dot.classList.add('active');
                dot.style.background = '#666666';
            });
            statusTexts.forEach(text => {
                text.textContent = 'Online';
                text.style.color = '#666666';
            });
        } else {
            statusDots.forEach(dot => {
                dot.classList.add('active');
                dot.style.background = '#999999';
            });
            statusTexts.forEach(text => {
                text.textContent = 'Demo Mode';
                text.style.color = '#999999';
            });
        }
    }

    async sendPrompt() {
        const message = this.promptInput.value.trim();
        if (!message || this.isProcessing) return;

        // Add user message
        this.addMessage('user', message);
        
        // Clear input and reset size
        this.promptInput.value = '';
        this.autoResizeTextarea();
        
        // Show loading
        this.showLoading('Processing your request...');
        
        try {
            // Simulate processing delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Generate response based on message content
            const response = this.generateResponse(message);
            
            // Add assistant response
            this.addMessage('assistant', response);
            
        } catch (error) {
            console.error('Error processing message:', error);
            this.addMessage('assistant', 'Sorry, I encountered an error processing your request. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    generateResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Simple response logic based on message content
        if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
            return 'Hello! I\'m your Agent Conversation System assistant. I can help you with:\n\n• Starting conversations between agents\n• Configuring agent roles and expertise\n• Running demo scenarios\n• Monitoring system status\n\nWhat would you like to do?';
        }
        
        if (lowerMessage.includes('start') && lowerMessage.includes('conversation')) {
            return 'I can help you start a conversation between your agents. Here are some example prompts:\n\n• "Start a conversation about project timeline between a Project Manager and Senior Developer"\n• "Have Employee1 (Marketing Manager) and Employee2 (Data Analyst) discuss Q4 budget allocation"\n• "Run a demo conversation about feature design"\n\nWhat type of conversation would you like to start?';
        }
        
        if (lowerMessage.includes('agent') && lowerMessage.includes('role')) {
            return 'You can configure agent roles by typing something like:\n\n• "Set Employee1 as Project Manager with expertise in project planning"\n• "Change Employee2 to Senior Developer with technical implementation skills"\n• "Configure both agents for a marketing discussion"\n\nWhat roles would you like to set?';
        }
        
        if (lowerMessage.includes('demo') || lowerMessage.includes('example')) {
            return 'Here are some demo scenarios you can try:\n\n• "Run the project timeline demo"\n• "Start the marketing campaign discussion"\n• "Show me the feature design conversation"\n• "Demonstrate the HR system implementation"\n\nWhich demo would you like to see?';
        }
        
        if (lowerMessage.includes('status') || lowerMessage.includes('system')) {
            return 'System Status:\n\n✅ Agents: All agents are online and ready\n✅ Guardian NLP: Processing system active\n✅ XAI API: Connected and operational\n✅ Database: Connected and responsive\n\nEverything is running smoothly!';
        }
        
        if (lowerMessage.includes('help') || lowerMessage.includes('what can you do')) {
            return 'I can help you with:\n\n🤖 **Agent Management**\n• Configure agent roles and expertise\n• Start conversations between agents\n• Monitor agent activity\n\n🛡️ **Guardian System**\n• View NLP classifier status\n• Check database integration\n• Monitor model training\n\n💬 **Conversations**\n• Run demo scenarios\n• Start custom conversations\n• Track conversation progress\n\nJust ask me what you\'d like to do!';
        }
        
        // Default response
        return 'I understand you\'re asking about: "' + message + '"\n\nI can help you with agent conversations, system configuration, and running demos. Try asking me to:\n\n• Start a conversation\n• Configure agents\n• Run a demo\n• Check system status\n\nWhat would you like to do?';
    }

    addMessage(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const time = new Date().toLocaleTimeString();
        const avatar = sender === 'user' ? 'U' : 'A';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-text">${this.formatMessage(content)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        this.conversationArea.appendChild(messageDiv);
        this.conversationArea.scrollTop = this.conversationArea.scrollHeight;
    }

    formatMessage(content) {
        // Convert line breaks to <br> tags
        return content.replace(/\n/g, '<br>');
    }

    autoResizeTextarea() {
        const textarea = this.promptInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    showLoading(text = 'Processing...') {
        this.isProcessing = true;
        this.loadingText.textContent = text;
        this.loadingOverlay.style.display = 'flex';
    }

    hideLoading() {
        this.isProcessing = false;
        this.loadingOverlay.style.display = 'none';
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new AgentConversationUI();
    
    // Initialize Prism syntax highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
}); 
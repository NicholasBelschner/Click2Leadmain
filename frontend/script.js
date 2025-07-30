// Agent Conversation System Frontend - Dynamic Agent Interface
class AgentConversationUI {
    constructor() {
        this.currentConversation = null;
        this.isProcessing = false;
        this.waitingForAgentSpecification = false;
        this.currentTopic = '';
        this.currentContext = '';
        
        this.initializeElements();
        this.bindEvents();
        this.initializeCodeTabs();
        this.startRealTimeUpdates();
        this.checkSystemStatus();
        this.updateAgentsDisplay(); // Load existing agents
    }

    initializeElements() {
        // Prompt interface elements
        this.promptInput = document.getElementById('prompt-input');
        this.sendButton = document.getElementById('send-prompt');
        this.conversationArea = document.getElementById('conversation-area');
        
        // Dynamic agents container
        this.dynamicAgentsContainer = document.getElementById('dynamic-agents-container');
        
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
            const response = await fetch('/api/status', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.updateStatusIndicators(data.status === 'available' ? 'connected' : 'demo');
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
            if (this.waitingForAgentSpecification) {
                // User is specifying agents
                await this.handleAgentSpecification(message);
            } else {
                // Check if this is an agent creation request
                const lowerMessage = message.toLowerCase();
                if (lowerMessage.includes('create') && lowerMessage.includes('agent') || 
                    lowerMessage.includes('team') && lowerMessage.includes('agent') ||
                    lowerMessage.includes('employees') && lowerMessage.includes('working') ||
                    lowerMessage.includes('3 employees') || lowerMessage.includes('3 agents')) {
                    
                    // Extract topic and context from the message
                    this.currentTopic = message;
                    this.currentContext = '';
                    
                    // Send the agent creation request to the backend
                    await this.handleAgentSpecification(message);
                } else {
                    // Regular conversation or starting new conversation
                    const response = this.generateResponse(message);
                    this.addMessage('assistant', response);
                }
            }
        } catch (error) {
            console.error('Error processing message:', error);
            this.addMessage('assistant', 'Sorry, I encountered an error processing your request. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async handleAgentSpecification(userSpecification) {
        try {
            const response = await fetch('/api/agents/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    specification: userSpecification,
                    topic: this.currentTopic,
                    context: this.currentContext
                })
            });

            const result = await response.json();
            
            if (result.status === 'started') {
                this.waitingForAgentSpecification = false;
                this.currentConversation = result;
                
                // Update the dynamic agents display
                this.displayDynamicAgents(result.agents);
                
                // Add broker message
                this.addMessage('assistant', result.broker_message);
                
                // Show created agents
                const agentList = result.agents.map(agent => `${agent.role} (${agent.expertise})`).join(', ');
                this.addMessage('assistant', `✅ Created ${result.agents_created} agents: ${agentList}\n\nYou can now conduct exchanges or start a full conversation.`);
                
            } else {
                this.addMessage('assistant', `Error: ${result.message || 'Failed to create agents'}`);
            }
        } catch (error) {
            console.error('Error creating agents:', error);
            this.addMessage('assistant', 'Error creating agents. Please try again.');
        }
    }

    displayDynamicAgents(agents) {
        if (!agents || agents.length === 0) {
            this.dynamicAgentsContainer.innerHTML = `
                <div class="no-agents-message">
                    <p>No agents created yet. Start a conversation to create your team!</p>
                </div>
            `;
            return;
        }

        const agentsHTML = agents.map((agent, index) => {
            const icon = this.getAgentIcon(agent.role);
            const shortPersonality = agent.personality.length > 100 
                ? agent.personality.substring(0, 100) + '...' 
                : agent.personality;
            
            return `
                <div class="dynamic-agent-card">
                    <div class="dynamic-agent-header">
                        <div class="dynamic-agent-info">
                            <div class="dynamic-agent-icon">${icon}</div>
                            <div class="dynamic-agent-details">
                                <h4>${agent.role}</h4>
                                <p>ID: ${agent.id}</p>
                            </div>
                        </div>
                        <div class="dynamic-agent-status">
                            <div class="dynamic-agent-status-dot"></div>
                            <span class="dynamic-agent-status-text">Active</span>
                        </div>
                    </div>
                    <div class="dynamic-agent-body">
                        <div class="dynamic-agent-expertise">
                            <h5>Expertise</h5>
                            <p>${agent.expertise}</p>
                        </div>
                        <div class="dynamic-agent-personality">
                            <h5>Personality</h5>
                            <p>${shortPersonality}</p>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        this.dynamicAgentsContainer.innerHTML = agentsHTML;
    }

    getAgentIcon(role) {
        const roleLower = role.toLowerCase();
        
        if (roleLower.includes('workout') || roleLower.includes('fitness')) {
            return '💪';
        } else if (roleLower.includes('nutrition') || roleLower.includes('diet')) {
            return '🥗';
        } else if (roleLower.includes('coordinator') || roleLower.includes('manager')) {
            return '🎯';
        } else if (roleLower.includes('developer') || roleLower.includes('technical')) {
            return '💻';
        } else if (roleLower.includes('designer') || roleLower.includes('ux')) {
            return '🎨';
        } else if (roleLower.includes('product')) {
            return '📋';
        } else if (roleLower.includes('marketing')) {
            return '📢';
        } else if (roleLower.includes('data') || roleLower.includes('analyst')) {
            return '📊';
        } else {
            return '🤖';
        }
    }

    async updateAgentsDisplay() {
        try {
            const response = await fetch('/api/agents/list');
            if (response.ok) {
                const data = await response.json();
                this.displayDynamicAgents(data.agents);
            }
        } catch (error) {
            console.error('Error updating agents display:', error);
        }
    }

    generateResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Check for conversation start requests
        if (lowerMessage.includes('start') && lowerMessage.includes('conversation')) {
            this.waitingForAgentSpecification = true;
            return 'I can help you start a conversation! Please tell me:\n\n1. What topic you want to discuss\n2. How many agents you want and their roles\n\nFor example:\n• "I want to discuss project timeline with a Project Manager and Developer"\n• "Create 3 agents: Product Manager, Designer, and Developer for a feature discussion"\n• "Just create 4 agents for a marketing strategy meeting"\n\nWhat would you like to discuss?';
        }
        
        // Check for agent creation requests - this is the key fix!
        if (lowerMessage.includes('create') && lowerMessage.includes('agent') || 
            lowerMessage.includes('team') && lowerMessage.includes('agent') ||
            lowerMessage.includes('employees') && lowerMessage.includes('working') ||
            lowerMessage.includes('3 employees') || lowerMessage.includes('3 agents')) {
            
            // This will be handled in sendPrompt method
            return 'Processing your agent creation request...';
        }
        
        // Check for topic specification
        if (this.waitingForAgentSpecification && (lowerMessage.includes('discuss') || lowerMessage.includes('about'))) {
            // Extract topic and context
            this.currentTopic = message;
            this.currentContext = '';
            
            this.waitingForAgentSpecification = true;
            return `Great! I understand you want to discuss: "${message}"\n\nNow, please specify how many agents you want and their roles. For example:\n• "Create 3 agents: Product Manager, Developer, and Designer"\n• "I want 2 agents: one for strategy and one for technical"\n• "Just create 4 agents for this discussion"\n\nWhat agents would you like for this conversation?`;
        }
        
        // Check for agent specification
        if (this.waitingForAgentSpecification && (lowerMessage.includes('create') || lowerMessage.includes('agent'))) {
            return `Perfect! I'll create those agents for you. Please wait while I set up the conversation...`;
        }
        
        // Check for exchange requests
        if (lowerMessage.includes('exchange') || lowerMessage.includes('next')) {
            if (this.currentConversation) {
                this.conductExchange();
                return 'Conducting the next exchange...';
            } else {
                return 'No active conversation. Please start a conversation first.';
            }
        }
        
        // Check for full conversation requests
        if (lowerMessage.includes('full') && lowerMessage.includes('conversation')) {
            if (this.currentConversation) {
                this.runFullConversation();
                return 'Running full conversation...';
            } else {
                return 'No active conversation. Please start a conversation first.';
            }
        }
        
        // Check for status requests
        if (lowerMessage.includes('status') || lowerMessage.includes('system')) {
            return 'System Status:\n\n✅ Dynamic Agent System: Available\n✅ Agent Creation: Working\n✅ Conversation Management: Active\n✅ XAI Integration: Ready\n\nEverything is running smoothly!';
        }
        
        // Check for help requests
        if (lowerMessage.includes('help') || lowerMessage.includes('what can you do')) {
            return 'I can help you with:\n\n🤖 **Dynamic Agent Creation**\n• Create any number of agents you need\n• Specify custom roles and expertise\n• Get AI-powered suggestions\n\n💬 **Conversation Management**\n• Start multi-agent conversations\n• Conduct exchanges between agents\n• Run full conversations automatically\n\n🎯 **Examples**\n• "Start a conversation about project timeline"\n• "Create 3 agents: Manager, Developer, Designer"\n• "Run a full conversation"\n\nJust tell me what you\'d like to do!';
        }
        
        // Default response
        return 'I understand you\'re asking about: "' + message + '"\n\nI can help you create dynamic agents and manage conversations. Try asking me to:\n\n• Start a conversation\n• Create agents\n• Run exchanges\n• Check system status\n\nWhat would you like to do?';
    }

    async conductExchange() {
        try {
            const response = await fetch('/api/conversation/exchange', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();
            
            if (result.status === 'exchange_completed') {
                // Add agent responses
                for (const agentResponse of result.agent_responses) {
                    this.addMessage('assistant', `${agentResponse.agent_role}: ${agentResponse.message}`);
                }
                
                // Add broker analysis
                this.addMessage('assistant', `📊 Broker Analysis: ${result.broker_analysis}`);
                
            } else if (result.status === 'concluded') {
                this.addMessage('assistant', `🎉 Conversation concluded!\n\n${result.conclusion}`);
                this.currentConversation = null;
            } else {
                this.addMessage('assistant', `Error: ${result.message || 'Failed to conduct exchange'}`);
            }
        } catch (error) {
            this.addMessage('assistant', 'Error conducting exchange. Please try again.');
        }
    }

    async runFullConversation() {
        try {
            const response = await fetch('/api/conversation/full', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    topic: this.currentTopic,
                    context: this.currentContext,
                    max_exchanges: 4
                })
            });

            const result = await response.json();
            
            if (result.status === 'completed') {
                this.addMessage('assistant', `🎉 Full conversation completed!\n\nTotal exchanges: ${result.total_exchanges}\nAgents participated: ${result.agents.length}\n\nConversation summary and conclusions have been generated.`);
                this.currentConversation = null;
            } else {
                this.addMessage('assistant', `Error: ${result.message || 'Failed to run full conversation'}`);
            }
        } catch (error) {
            this.addMessage('assistant', 'Error running full conversation. Please try again.');
        }
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
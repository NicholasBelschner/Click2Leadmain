// Agent Conversation System Frontend - Dynamic Agent Interface

// Configuration - Update this for production deployment
const CONFIG = {
    // API Base URL - Change this to your Render URL when deployed
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5001' 
        : 'https://your-render-app-name.onrender.com', // Update this with your Render URL
    
    // Feature flags
    ENABLE_NEURAL_LEARNING: true,
    ENABLE_REAL_TIME_THOUGHTS: true,
    ENABLE_TAB_SYSTEM: true
};

class AgentConversationUI {
    constructor() {
        this.currentConversation = null;
        this.isProcessing = false;
        this.waitingForAgentSpecification = false;
        this.currentTopic = '';
        this.currentContext = '';
        this.thoughtStream = null;
        this.thoughtStreamActive = false;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeCodeTabs();
        this.startRealTimeUpdates();
        this.checkSystemStatus();
        this.updateAgentsDisplay(); // Load existing agents
        this.startGuardianThoughtProcess(); // Start Guardian thought process
        this.initializeThoughtStream(); // Initialize real-time thought stream
        this.initializeTabSystem(); // Initialize tab system
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
        
        // Thought stream container
        this.thoughtStreamContainer = document.getElementById('thought-stream-container');
        if (!this.thoughtStreamContainer) {
            // Create thought stream container if it doesn't exist
            this.createThoughtStreamContainer();
        }
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
        
        // Clear previous thoughts and show real-time processing
        await this.clearThoughtStream();
        this.showRealTimeProcessing();
        
        try {
            // Send all prompts to the intelligent conversation processor
            const response = await fetch('/api/conversation/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    context: {
                        currentTopic: this.currentTopic,
                        currentContext: this.currentContext,
                        waitingForAgentSpecification: this.waitingForAgentSpecification
                    }
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                // Handle different response types
                if (result.type === 'agent_creation') {
                    this.waitingForAgentSpecification = false;
                    this.currentConversation = result;
                    
                    // Update the dynamic agents display
                    if (result.agents && result.agents.length > 0) {
                        this.displayDynamicAgents(result.agents);
                    }
                    
                    // Add broker message
                    this.addMessage('assistant', result.response);
                    
                    // Show created agents summary
                    if (result.agents_created > 0) {
                        const agentList = result.agents.map(agent => `${agent.role} (${agent.expertise})`).join(', ');
                        this.addMessage('assistant', `✅ Created ${result.agents_created} agents: ${agentList}\n\nYou can now conduct exchanges or start a full conversation.`);
                    }
                    
                } else if (result.type === 'exchange') {
                    // Handle exchange results
                    this.addMessage('assistant', result.response);
                    
                } else if (result.type === 'learning_stats') {
                    // Handle learning stats request
                    await this.showLearningStats();
                    
                } else {
                    // Handle all other response types (help, status, general, etc.)
                    this.addMessage('assistant', result.response);
                }
                
            } else {
                this.addMessage('assistant', `Error: ${result.response || 'Failed to process your request'}`);
            }
            
        } catch (error) {
            console.error('Error processing message:', error);
            this.addMessage('assistant', 'Sorry, I encountered an error processing your request. Please try again.');
        } finally {
            this.hideRealTimeProcessing();
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

        const agentsHTML = `
            <div class="zoom-agent-grid">
                ${agents.map((agent, index) => {
                    const icon = this.getAgentIcon(agent.role);
                    const shortPersonality = agent.personality.length > 100 
                        ? agent.personality.substring(0, 100) + '...' 
                        : agent.personality;
                    
                    return `
                        <div class="zoom-agent-tile" data-agent-id="${agent.id}">
                            <div class="zoom-agent-video-area">
                                <div class="zoom-agent-avatar">${icon}</div>
                                <div class="zoom-agent-status"></div>
                            </div>
                            <div class="zoom-agent-info">
                                <div class="zoom-agent-name">${agent.role}</div>
                                <div class="zoom-agent-role">${agent.expertise}</div>
                            </div>
                            <div class="zoom-agent-thoughts" id="agent-thoughts-${agent.id}">
                                <div class="agent-thought-entry">
                                    <span class="agent-thought-timestamp">${new Date().toLocaleTimeString()}</span>
                                    <span class="agent-thought-text">Initializing agent systems...</span>
                                </div>
                                <div class="agent-thought-entry">
                                    <span class="agent-thought-timestamp">${new Date().toLocaleTimeString()}</span>
                                    <span class="agent-thought-text">Loading expertise: ${agent.expertise}</span>
                                </div>
                                <div class="agent-thought-entry">
                                    <span class="agent-thought-timestamp">${new Date().toLocaleTimeString()}</span>
                                    <span class="agent-thought-text">Ready for conversation</span>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        this.dynamicAgentsContainer.innerHTML = agentsHTML;
        
        // Start real-time thought processes for each agent
        agents.forEach(agent => {
            this.startAgentThoughtProcess(agent);
        });
    }

    startAgentThoughtProcess(agent) {
        const thoughtsContainer = document.getElementById(`agent-thoughts-${agent.id}`);
        if (!thoughtsContainer) return;

        const thoughtProcesses = [
            `Analyzing current conversation context...`,
            `Processing user request for ${agent.role.toLowerCase()} perspective...`,
            `Generating response based on expertise in ${agent.expertise.toLowerCase()}...`,
            `Considering best approach for user's needs...`,
            `Formulating professional recommendation...`,
            `Preparing to contribute to team discussion...`,
            `Evaluating potential solutions and strategies...`,
            `Ready to provide ${agent.role.toLowerCase()} insights...`
        ];

        let thoughtIndex = 0;
        
        const addThought = () => {
            if (thoughtIndex < thoughtProcesses.length) {
                const thoughtEntry = document.createElement('div');
                thoughtEntry.className = 'agent-thought-entry';
                thoughtEntry.innerHTML = `
                    <span class="agent-thought-timestamp">${new Date().toLocaleTimeString()}</span>
                    <span class="agent-thought-text">${thoughtProcesses[thoughtIndex]}</span>
                `;
                
                thoughtsContainer.appendChild(thoughtEntry);
                thoughtsContainer.scrollTop = thoughtsContainer.scrollHeight;
                
                thoughtIndex++;
                
                // Continue the thought process
                setTimeout(addThought, Math.random() * 3000 + 2000); // 2-5 seconds
            }
        };

        // Start the thought process after a short delay
        setTimeout(addThought, 1000);
    }

    startGuardianThoughtProcess() {
        const guardianStream = document.getElementById('guardian-thought-stream');
        if (!guardianStream) return;

        const guardianThoughts = [
            'Monitoring system performance and health...',
            'Analyzing incoming text data for importance classification...',
            'Processing neural network predictions with confidence scores...',
            'Updating database with new classification results...',
            'Optimizing model performance based on recent data...',
            'Maintaining system security and data integrity...',
            'Preparing for next text analysis request...',
            'Guardian NLP system operating at optimal efficiency...'
        ];

        let thoughtIndex = 0;
        
        const addGuardianThought = () => {
            if (thoughtIndex < guardianThoughts.length) {
                const thoughtEntry = document.createElement('div');
                thoughtEntry.className = 'thought-entry';
                thoughtEntry.innerHTML = `
                    <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                    <span class="thought-text">${guardianThoughts[thoughtIndex]}</span>
                `;
                
                guardianStream.appendChild(thoughtEntry);
                guardianStream.scrollTop = guardianStream.scrollHeight;
                
                thoughtIndex++;
                
                // Continue the thought process
                setTimeout(addGuardianThought, Math.random() * 4000 + 3000); // 3-7 seconds
            }
        };

        // Start the Guardian thought process
        setTimeout(addGuardianThought, 2000);
    }

    addAgentThought(agentId, thought) {
        const thoughtsContainer = document.getElementById(`agent-thoughts-${agentId}`);
        if (!thoughtsContainer) return;

        const thoughtEntry = document.createElement('div');
        thoughtEntry.className = 'agent-thought-entry';
        thoughtEntry.innerHTML = `
            <span class="agent-thought-timestamp">${new Date().toLocaleTimeString()}</span>
            <span class="agent-thought-text">${thought}</span>
        `;
        
        thoughtsContainer.appendChild(thoughtEntry);
        thoughtsContainer.scrollTop = thoughtsContainer.scrollHeight;
    }

    addGuardianThought(thought) {
        const guardianStream = document.getElementById('guardian-thought-stream');
        if (!guardianStream) return;

        const thoughtEntry = document.createElement('div');
        thoughtEntry.className = 'thought-entry';
        thoughtEntry.innerHTML = `
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
            <span class="thought-text">${thought}</span>
        `;
        
        guardianStream.appendChild(thoughtEntry);
        guardianStream.scrollTop = guardianStream.scrollHeight;
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
                
                // Update tab system if available
                if (tabManager) {
                    tabManager.updateAgentsTab(data.agents);
                }
            }
        } catch (error) {
            console.error('Error updating agents display:', error);
        }
    }

    // Removed generateResponse method - now using intelligent backend processing

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

    showRealTimeProcessing() {
        this.isProcessing = true;
        
        // Show the thought stream container prominently
        if (this.thoughtStreamContainer) {
            this.thoughtStreamContainer.style.display = 'block';
            this.thoughtStreamContainer.style.border = '2px solid #007bff';
            this.thoughtStreamContainer.style.background = '#f8f9fa';
        }
        
        // Add initial processing thought
        this.addThoughtToStream({
            timestamp: new Date().toISOString(),
            type: 'system',
            message: 'Starting to process your request...'
        });
    }

    hideRealTimeProcessing() {
        this.isProcessing = false;
        
        // Remove highlighting from thought stream container
        if (this.thoughtStreamContainer) {
            this.thoughtStreamContainer.style.border = '';
            this.thoughtStreamContainer.style.background = '';
        }
    }

    createThoughtStreamContainer() {
        // Create thought stream container
        const container = document.createElement('div');
        container.id = 'thought-stream-container';
        container.className = 'thought-stream-container';
        container.innerHTML = `
            <div class="thought-stream-header">
                <h3>🤔 Real-Time Thought Process</h3>
                <button id="clear-thoughts" class="clear-thoughts-btn">Clear</button>
            </div>
            <div id="thought-stream-content" class="thought-stream-content">
                <div class="thought-entry">
                    <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                    <span class="thought-text">Thought stream initialized. Waiting for activity...</span>
                </div>
            </div>
        `;
        
        // Insert after conversation area
        const conversationArea = document.getElementById('conversation-area');
        if (conversationArea && conversationArea.parentNode) {
            conversationArea.parentNode.insertBefore(container, conversationArea.nextSibling);
        }
        
        this.thoughtStreamContainer = container;
        
        // Bind clear button
        const clearBtn = container.querySelector('#clear-thoughts');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearThoughtStream());
        }
    }

    initializeThoughtStream() {
        if (this.thoughtStreamActive) return;
        
        try {
            this.thoughtStream = new EventSource('/api/thoughts/stream');
            this.thoughtStreamActive = true;
            
            this.thoughtStream.onmessage = (event) => {
                try {
                    const thought = JSON.parse(event.data);
                    this.addThoughtToStream(thought);
                } catch (error) {
                    console.error('Error parsing thought:', error);
                }
            };
            
            this.thoughtStream.onerror = (error) => {
                console.error('Thought stream error:', error);
                this.thoughtStreamActive = false;
                // Try to reconnect after 5 seconds
                setTimeout(() => this.initializeThoughtStream(), 5000);
            };
            
        } catch (error) {
            console.error('Error initializing thought stream:', error);
        }
    }

    addThoughtToStream(thought) {
        const content = document.getElementById('thought-stream-content');
        if (!content) return;
        
        const thoughtEntry = document.createElement('div');
        thoughtEntry.className = 'thought-entry';
        
        const timestamp = new Date(thought.timestamp).toLocaleTimeString();
        const thoughtType = thought.type || 'system';
        const agentId = thought.agent_id || '';
        
        let thoughtText = thought.message;
        if (agentId) {
            thoughtText = `[Agent ${agentId}] ${thoughtText}`;
        }
        
        thoughtEntry.innerHTML = `
            <span class="timestamp">${timestamp}</span>
            <span class="thought-type">${thoughtType}</span>
            <span class="thought-text">${thoughtText}</span>
        `;
        
        content.appendChild(thoughtEntry);
        content.scrollTop = content.scrollHeight;
        
        // Add highlight effect
        thoughtEntry.style.background = '#f0f0f0';
        setTimeout(() => {
            thoughtEntry.style.background = '';
        }, 1000);
    }

    async clearThoughtStream() {
        try {
            await fetch('/api/thoughts/clear', { method: 'POST' });
            const content = document.getElementById('thought-stream-content');
            if (content) {
                content.innerHTML = `
                    <div class="thought-entry">
                        <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                        <span class="thought-text">Thought stream cleared. Waiting for new activity...</span>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error clearing thought stream:', error);
        }
    }

    async showLearningStats() {
        try {
            const response = await fetch('/api/learning/stats');
            const stats = await response.json();
            
            if (stats.error) {
                this.addMessage('assistant', `Learning system not available: ${stats.error}`);
                return;
            }
            
            const statsMessage = `🧠 **Neural Learning System Stats**

**📊 Interaction Data:**
• Total interactions: ${stats.total_interactions}
• Successful patterns: ${stats.successful_patterns}
• Average success rate: ${(stats.average_success_rate * 100).toFixed(1)}%

**🤖 Preferred Agents:**
${Object.entries(stats.preferred_agents).map(([agent, count]) => `• ${agent}: ${count} times`).join('\n') || 'None yet'}

**🔧 System Status:**
• Neural networks: ${stats.neural_networks_available ? '✅ Available' : '❌ Not available'}
• Training status: ${stats.is_training ? '🔄 Training' : '✅ Ready'}

The system is learning from your interactions to provide better responses!`;
            
            this.addMessage('assistant', statsMessage);
            
        } catch (error) {
            console.error('Error fetching learning stats:', error);
            this.addMessage('assistant', 'Error fetching learning statistics.');
        }
    }

    initializeTabSystem() {
        // Initialize the tab manager
        tabManager = new TabManager();
        tabManager.initialize();
        
        // Update agents tab when agents are loaded
        this.updateAgentsDisplay();
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
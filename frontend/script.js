// Agent Conversation System Frontend
class AgentConversationUI {
    constructor() {
        this.currentConversation = null;
        this.exchangeCount = 0;
        this.maxExchanges = 4;
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.checkSystemStatus();
    }

    initializeElements() {
        // Configuration elements
        this.employee1Role = document.getElementById('employee1-role');
        this.employee1Expertise = document.getElementById('employee1-expertise');
        this.employee2Role = document.getElementById('employee2-role');
        this.employee2Expertise = document.getElementById('employee2-expertise');
        
        // Conversation elements
        this.conversationTopic = document.getElementById('conversation-topic');
        this.conversationContext = document.getElementById('conversation-context');
        this.maxExchangesSelect = document.getElementById('max-exchanges');
        
        // Display elements
        this.conversationDisplay = document.getElementById('conversation-display');
        this.conversationContent = document.getElementById('conversation-content');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        
        // Control buttons
        this.startButton = document.getElementById('start-conversation');
        this.nextExchangeButton = document.getElementById('next-exchange');
        this.runFullButton = document.getElementById('run-full-conversation');
        this.resetButton = document.getElementById('reset-conversation');
        
        // Demo buttons
        this.demoButtons = document.querySelectorAll('.btn-demo');
        
        // Status elements
        this.apiStatus = document.getElementById('api-status');
        this.agentsStatus = document.getElementById('agents-status');
        this.conversationStatus = document.getElementById('conversation-status');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingText = document.getElementById('loading-text');
    }

    bindEvents() {
        // Start conversation
        this.startButton.addEventListener('click', () => this.startConversation());
        
        // Next exchange
        this.nextExchangeButton.addEventListener('click', () => this.nextExchange());
        
        // Run full conversation
        this.runFullButton.addEventListener('click', () => this.runFullConversation());
        
        // Reset conversation
        this.resetButton.addEventListener('click', () => this.resetConversation());
        
        // Demo buttons
        this.demoButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const scenario = e.target.dataset.scenario;
                this.loadDemoScenario(scenario);
            });
        });
        
        // Max exchanges change
        this.maxExchangesSelect.addEventListener('change', (e) => {
            this.maxExchanges = parseInt(e.target.value);
            this.updateProgress();
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
                this.updateStatus('api-status', 'Connected', 'success');
                this.updateStatus('agents-status', 'Ready', 'success');
            } else {
                this.updateStatus('api-status', 'Not Connected', 'error');
                this.updateStatus('agents-status', 'Not Available', 'error');
            }
        } catch (error) {
            console.log('Running in demo mode - no backend connection');
            this.updateStatus('api-status', 'Demo Mode', 'warning');
            this.updateStatus('agents-status', 'Demo Mode', 'warning');
        }
    }

    updateStatus(elementId, text, type = '') {
        const element = document.getElementById(elementId);
        element.textContent = text;
        element.className = `status-value ${type}`;
    }

    async startConversation() {
        if (this.isProcessing) return;
        
        const topic = this.conversationTopic.value.trim();
        const context = this.conversationContext.value.trim();
        
        if (!topic) {
            alert('Please enter a conversation topic');
            return;
        }
        
        this.showLoading('Starting conversation...');
        
        try {
            // In a real implementation, this would call the backend
            // For now, we'll simulate the conversation start
            await this.simulateConversationStart(topic, context);
            
            this.conversationDisplay.style.display = 'block';
            this.updateStatus('conversation-status', 'Active', 'success');
            this.exchangeCount = 0;
            this.updateProgress();
            
            // Add initial messages
            this.addMessage('broker', 'Conversation started', 'Conversation initialized with the specified topic and context.');
            
        } catch (error) {
            console.error('Error starting conversation:', error);
            alert('Error starting conversation. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async simulateConversationStart(topic, context) {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Simulate initial perspectives
        const employee1Role = this.employee1Role.value;
        const employee2Role = this.employee2Role.value;
        
        this.addMessage('employee1', `${employee1Role} Initial Perspective`, 
            `As a ${employee1Role}, I believe we should approach this topic systematically. ${topic} requires careful consideration of our current processes and potential improvements.`);
        
        this.addMessage('employee2', `${employee2Role} Initial Perspective`, 
            `From a ${employee2Role} perspective, I see several technical considerations we need to address. ${topic} involves both strategic and implementation challenges.`);
        
        this.addMessage('broker', 'Analysis', 
            'Both perspectives provide valuable insights. Employee1 focuses on systematic approach while Employee2 emphasizes technical considerations. Let\'s explore these viewpoints further.');
    }

    async nextExchange() {
        if (this.isProcessing || this.exchangeCount >= this.maxExchanges) return;
        
        this.showLoading('Processing next exchange...');
        
        try {
            await this.simulateExchange();
            this.exchangeCount++;
            this.updateProgress();
            
            if (this.exchangeCount >= this.maxExchanges) {
                this.concludeConversation();
            }
            
        } catch (error) {
            console.error('Error processing exchange:', error);
            alert('Error processing exchange. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async simulateExchange() {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        const employee1Role = this.employee1Role.value;
        const employee2Role = this.employee2Role.value;
        
        // Simulate employee responses
        this.addMessage('employee1', `${employee1Role} Response`, 
            `I understand the technical challenges you've raised. From a management perspective, we need to balance these technical requirements with our timeline and resource constraints.`);
        
        this.addMessage('employee2', `${employee2Role} Response`, 
            `Thank you for considering the technical aspects. I believe we can find a middle ground that addresses both the technical requirements and the business constraints.`);
        
        // Simulate broker analysis
        this.addMessage('broker', 'Exchange Analysis', 
            'Excellent progress! Both parties are showing willingness to collaborate and find common ground. The conversation is moving toward a constructive resolution.');
    }

    async runFullConversation() {
        if (this.isProcessing) return;
        
        this.showLoading('Running full conversation...');
        
        try {
            // Run all exchanges
            for (let i = 0; i < this.maxExchanges; i++) {
                await this.simulateExchange();
                this.exchangeCount++;
                this.updateProgress();
                await new Promise(resolve => setTimeout(resolve, 1000)); // Brief pause between exchanges
            }
            
            this.concludeConversation();
            
        } catch (error) {
            console.error('Error running full conversation:', error);
            alert('Error running full conversation. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    concludeConversation() {
        this.addMessage('broker', 'Conversation Conclusion', 
            'The conversation has reached a successful conclusion. Both parties have achieved mutual understanding and identified a path forward. Key decisions and next steps have been established.');
        
        this.updateStatus('conversation-status', 'Completed', 'success');
        this.nextExchangeButton.style.display = 'none';
        this.runFullButton.disabled = true;
    }

    loadDemoScenario(scenario) {
        const scenarios = {
            project: {
                topic: 'Project Timeline Adjustment for Authentication Module',
                context: 'Client needs delivery by Friday, team estimates 2 more weeks',
                employee1Role: 'Project Manager',
                employee1Expertise: 'Project planning and coordination',
                employee2Role: 'Senior Developer',
                employee2Expertise: 'Technical implementation and system architecture'
            },
            design: {
                topic: 'Redesigning User Onboarding Flow',
                context: '40% drop-off rate, need to improve retention',
                employee1Role: 'Product Manager',
                employee1Expertise: 'Product strategy and user experience',
                employee2Role: 'UX Designer',
                employee2Expertise: 'User interface design and user research'
            },
            marketing: {
                topic: 'Q4 Marketing Campaign Budget Allocation',
                context: '$100K budget across different channels',
                employee1Role: 'Marketing Manager',
                employee1Expertise: 'Marketing strategy and campaign management',
                employee2Role: 'Data Analyst',
                employee2Expertise: 'Data analysis and performance optimization'
            },
            hr: {
                topic: 'Employee Performance Management System Implementation',
                context: 'Replace paper-based system with digital solution',
                employee1Role: 'HR Manager',
                employee1Expertise: 'Human resources and employee relations',
                employee2Role: 'IT Manager',
                employee2Expertise: 'Information technology and system implementation'
            }
        };
        
        const selectedScenario = scenarios[scenario];
        if (selectedScenario) {
            this.conversationTopic.value = selectedScenario.topic;
            this.conversationContext.value = selectedScenario.context;
            this.employee1Role.value = selectedScenario.employee1Role;
            this.employee1Expertise.value = selectedScenario.employee1Expertise;
            this.employee2Role.value = selectedScenario.employee2Role;
            this.employee2Expertise.value = selectedScenario.employee2Expertise;
            
            // Highlight the selected demo button
            this.demoButtons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        }
    }

    resetConversation() {
        this.conversationContent.innerHTML = '';
        this.conversationDisplay.style.display = 'none';
        this.exchangeCount = 0;
        this.updateProgress();
        this.updateStatus('conversation-status', 'Idle');
        
        // Reset buttons
        this.nextExchangeButton.style.display = 'none';
        this.runFullButton.disabled = false;
    }

    updateProgress() {
        const progress = (this.exchangeCount / this.maxExchanges) * 100;
        this.progressFill.style.width = `${progress}%`;
        this.progressText.textContent = `Exchange ${this.exchangeCount} of ${this.maxExchanges}`;
    }

    addMessage(sender, title, content, analysis = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const time = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-sender">${title}</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-content">${content}</div>
            ${analysis ? `<div class="message-analysis">${analysis}</div>` : ''}
        `;
        
        this.conversationContent.appendChild(messageDiv);
        this.conversationContent.scrollTop = this.conversationContent.scrollHeight;
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
});

// Add some CSS for active demo button state
const style = document.createElement('style');
style.textContent = `
    .btn-demo.active {
        background: #000000 !important;
        color: white !important;
        border-color: #000000 !important;
    }
`;
document.head.appendChild(style); 
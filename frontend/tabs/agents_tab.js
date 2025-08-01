// Agents Tab Component
class AgentsTab {
    constructor() {
        this.container = null;
        this.agentsContainer = null;
        this.guardianContainer = null;
    }

    create() {
        const container = document.createElement('div');
        container.className = 'tab-content agents-tab';
        container.id = 'agents-tab-content';
        
        container.innerHTML = `
            <div class="tab-section">
                <h3>🤖 Dynamic Agents</h3>
                <div id="dynamic-agents-container">
                    <div class="no-agents-message">
                        <p>No agents created yet. Start a conversation to create your team!</p>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>🛡️ Guardian System</h3>
                <div class="guardian-operations-container">
                    <div class="guardian-status">
                        <div class="status-indicator active"></div>
                        <span class="status-text">Processing</span>
                    </div>
                    <div class="guardian-thoughts">
                        <div class="thought-stream" id="guardian-thought-stream">
                            <div class="thought-entry">
                                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                                <span class="thought-text">Initializing Guardian NLP system...</span>
                            </div>
                            <div class="thought-entry">
                                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                                <span class="thought-text">Loading neural network models...</span>
                            </div>
                            <div class="thought-entry">
                                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                                <span class="thought-text">Establishing database connections...</span>
                            </div>
                            <div class="thought-entry">
                                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                                <span class="thought-text">Guardian system ready for text analysis</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.container = container;
        this.agentsContainer = container.querySelector('#dynamic-agents-container');
        this.guardianContainer = container.querySelector('#guardian-thought-stream');
        
        return container;
    }

    updateAgents(agents) {
        if (!this.agentsContainer) return;
        
        if (!agents || agents.length === 0) {
            this.agentsContainer.innerHTML = `
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

        this.agentsContainer.innerHTML = agentsHTML;
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

    addGuardianThought(thought) {
        if (!this.guardianContainer) return;

        const thoughtEntry = document.createElement('div');
        thoughtEntry.className = 'thought-entry';
        thoughtEntry.innerHTML = `
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
            <span class="thought-text">${thought}</span>
        `;
        
        this.guardianContainer.appendChild(thoughtEntry);
        this.guardianContainer.scrollTop = this.guardianContainer.scrollHeight;
    }

    show() {
        if (this.container) {
            this.container.style.display = 'block';
        }
    }

    hide() {
        if (this.container) {
            this.container.style.display = 'none';
        }
    }
} 
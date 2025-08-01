// Tab Manager - Handles all tab functionality
class TabManager {
    constructor() {
        this.tabs = {};
        this.activeTab = null;
        this.tabContainer = null;
        this.contentContainer = null;
    }

    initialize() {
        this.createTabBar();
        this.createContentArea();
        this.initializeTabs();
        this.setupEventListeners();
    }

    createTabBar() {
        const tabBar = document.createElement('div');
        tabBar.className = 'tab-bar';
        tabBar.id = 'tab-bar';
        
        tabBar.innerHTML = `
            <div class="tab-item active" data-tab="agents">
                <span class="tab-icon">🤖</span>
                <span class="tab-label">Agents & Guardian</span>
            </div>
            <div class="tab-item" data-tab="health">
                <span class="tab-icon">📱</span>
                <span class="tab-label">Health Data</span>
            </div>
            <div class="tab-item" data-tab="neural">
                <span class="tab-icon">🧠</span>
                <span class="tab-label">Neural Architecture</span>
            </div>
            <div class="tab-item" data-tab="video">
                <span class="tab-icon">📹</span>
                <span class="tab-label">Video Analysis</span>
            </div>
        `;
        
        // Insert tab bar at the top of the left panel
        const leftPanel = document.querySelector('.left-panel');
        if (leftPanel) {
            leftPanel.insertBefore(tabBar, leftPanel.firstChild);
        }
        
        this.tabContainer = tabBar;
    }

    createContentArea() {
        // Create content area for tabs
        const contentArea = document.createElement('div');
        contentArea.className = 'tab-content-area';
        contentArea.id = 'tab-content-area';
        
        // Insert content area after tab bar in left panel
        const leftPanel = document.querySelector('.left-panel');
        if (leftPanel) {
            const tabBar = leftPanel.querySelector('#tab-bar');
            if (tabBar) {
                leftPanel.insertBefore(contentArea, tabBar.nextSibling);
            } else {
                leftPanel.appendChild(contentArea);
            }
        }
        
        this.contentContainer = contentArea;
    }

    initializeTabs() {
        // Initialize all tab components
        this.tabs = {
            agents: new AgentsTab(),
            health: new HealthDataTab(),
            neural: new NeuralArchitectureTab(),
            video: new VideoAnalysisTab()
        };
        
        // Create tab content
        Object.keys(this.tabs).forEach(tabKey => {
            const tab = this.tabs[tabKey];
            const content = tab.create();
            content.style.display = 'none';
            this.contentContainer.appendChild(content);
        });
        
        // Set default active tab
        this.switchTab('agents');
    }

    setupEventListeners() {
        // Add click listeners to tab items
        const tabItems = this.tabContainer.querySelectorAll('.tab-item');
        tabItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const tabKey = item.getAttribute('data-tab');
                this.switchTab(tabKey);
            });
        });
    }

    switchTab(tabKey) {
        // Hide all tabs
        Object.keys(this.tabs).forEach(key => {
            this.tabs[key].hide();
        });
        
        // Remove active class from all tab items
        const tabItems = this.tabContainer.querySelectorAll('.tab-item');
        tabItems.forEach(item => {
            item.classList.remove('active');
        });
        
        // Show selected tab
        if (this.tabs[tabKey]) {
            this.tabs[tabKey].show();
            this.activeTab = tabKey;
            
            // Add active class to selected tab item
            const activeTabItem = this.tabContainer.querySelector(`[data-tab="${tabKey}"]`);
            if (activeTabItem) {
                activeTabItem.classList.add('active');
            }
        }
    }

    getActiveTab() {
        return this.activeTab;
    }

    getTab(tabKey) {
        return this.tabs[tabKey];
    }

    updateAgentsTab(agents) {
        if (this.tabs.agents) {
            this.tabs.agents.updateAgents(agents);
        }
    }

    addGuardianThought(thought) {
        if (this.tabs.agents) {
            this.tabs.agents.addGuardianThought(thought);
        }
    }
}

// Global tab manager instance
let tabManager; 
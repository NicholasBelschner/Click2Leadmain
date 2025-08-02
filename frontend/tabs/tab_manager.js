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
        // Don't create tab bar - we only want the Agents & Guardian content
        // The content will be displayed directly in the left panel
        this.tabContainer = null;
    }

    createContentArea() {
        // Use the existing left panel content directly
        const leftPanel = document.querySelector('.left-panel');
        if (leftPanel) {
            this.contentContainer = leftPanel;
        }
    }

    initializeTabs() {
        // Only initialize the agents tab (which includes Guardian)
        this.tabs = {
            agents: new AgentsTab()
        };
        
        // Show the agents tab content directly
        if (this.tabs.agents) {
            this.tabs.agents.show();
            this.activeTab = 'agents';
        }
    }

    setupEventListeners() {
        // No event listeners needed since we only have one tab
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
# Tab System Documentation

## Overview
The tab system provides an organized way to display different features and functionalities in the left panel of the application. Each tab represents a different aspect of the system and can be easily extended.

## File Structure
```
frontend/tabs/
├── README.md                    # This documentation
├── tab_manager.js              # Main tab manager that handles switching and coordination
├── agents_tab.js               # Agents & Guardian system tab
├── health_data_tab.js          # Apple Watch health data tab
├── neural_architecture_tab.js  # Personal neural network architecture tab
└── video_analysis_tab.js       # Video/picture upload and analysis tab
```

## Tab Components

### 1. Agents Tab (`agents_tab.js`)
**Purpose**: Displays the current dynamic agents and guardian system
**Features**:
- Shows all created agents with their roles and expertise
- Displays agent thoughts and status
- Guardian system operations and thoughts
- Real-time agent updates

**Key Methods**:
- `updateAgents(agents)` - Updates the agents display
- `addGuardianThought(thought)` - Adds guardian system thoughts
- `getAgentIcon(role)` - Returns appropriate icon for agent role

### 2. Health Data Tab (`health_data_tab.js`)
**Purpose**: Apple Watch health data integration and display
**Features**:
- Apple Watch connection status
- Real-time heart rate and vitals monitoring
- Sleep analysis and tracking
- Activity rings and workout history
- Health trends and AI recommendations

**Key Methods**:
- `connectToWatch()` - Simulates Apple Watch connection
- `updateHeartRate(rate)` - Updates heart rate display
- `simulateDataStream()` - Simulates real-time health data

### 3. Neural Architecture Tab (`neural_architecture_tab.js`)
**Purpose**: Personal neural network architecture system
**Features**:
- Cognitive components modeling (thinking patterns, learning mechanisms, etc.)
- Neural network training dashboard
- Personal system modeling (time management, energy management)
- AI agent integration with cognitive mirror
- Continuous learning loop visualization

**Key Methods**:
- `startTraining()` - Initiates neural network training
- `updateComponentStatus(component, status)` - Updates component status
- `simulateTraining()` - Simulates training progress

### 4. Video Analysis Tab (`video_analysis_tab.js`)
**Purpose**: Athletic movement analysis through video/photo uploads
**Features**:
- Drag & drop file upload interface
- Video and photo analysis capabilities
- AI agent integration for movement analysis
- Progress tracking and recommendations
- File management and analysis results

**Key Methods**:
- `handleFileUpload(files)` - Processes uploaded files
- `analyzeFile(fileId)` - Analyzes specific file
- `addAnalysisResult(fileData)` - Adds analysis results

## Tab Manager (`tab_manager.js`)
**Purpose**: Coordinates all tabs and handles switching
**Features**:
- Tab creation and initialization
- Tab switching logic
- Global tab state management
- Integration with main application

**Key Methods**:
- `initialize()` - Initializes the entire tab system
- `switchTab(tabKey)` - Switches to specified tab
- `updateAgentsTab(agents)` - Updates agents tab with new data

## Integration with Main Application

### HTML Integration
The tab system is integrated into the main HTML through script tags:
```html
<!-- Tab Components -->
<script src="tabs/agents_tab.js"></script>
<script src="tabs/health_data_tab.js"></script>
<script src="tabs/neural_architecture_tab.js"></script>
<script src="tabs/video_analysis_tab.js"></script>
<script src="tabs/tab_manager.js"></script>
```

### JavaScript Integration
The main application initializes the tab system:
```javascript
initializeTabSystem() {
    tabManager = new TabManager();
    tabManager.initialize();
    this.updateAgentsDisplay();
}
```

### CSS Styling
The tab system uses comprehensive CSS styling located in `styles.css`:
- Tab bar styling and animations
- Tab content area styling
- Component-specific styling for each tab
- Responsive design considerations

## Adding New Tabs

To add a new tab:

1. **Create the tab component file** (`new_tab.js`):
```javascript
class NewTab {
    constructor() {
        this.container = null;
    }

    create() {
        const container = document.createElement('div');
        container.className = 'tab-content new-tab';
        container.id = 'new-tab-content';
        
        container.innerHTML = `
            <div class="tab-section">
                <h3>New Tab Title</h3>
                <!-- Tab content here -->
            </div>
        `;
        
        this.container = container;
        return container;
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
```

2. **Add to tab manager** (`tab_manager.js`):
```javascript
// In initializeTabs() method
this.tabs = {
    agents: new AgentsTab(),
    health: new HealthDataTab(),
    neural: new NeuralArchitectureTab(),
    video: new VideoAnalysisTab(),
    new: new NewTab() // Add new tab
};
```

3. **Add tab bar item**:
```javascript
// In createTabBar() method
tabBar.innerHTML = `
    <!-- Existing tabs -->
    <div class="tab-item" data-tab="new">
        <span class="tab-icon">🆕</span>
        <span class="tab-label">New Tab</span>
    </div>
`;
```

4. **Add to HTML**:
```html
<script src="tabs/new_tab.js"></script>
```

5. **Add CSS styling** in `styles.css`

## Best Practices

1. **Consistent Structure**: Each tab should follow the same basic structure with `create()`, `show()`, and `hide()` methods.

2. **Event Handling**: Use proper event delegation and cleanup for event listeners.

3. **State Management**: Keep tab-specific state within the tab component.

4. **Responsive Design**: Ensure tabs work well on different screen sizes.

5. **Performance**: Lazy load tab content when possible to improve initial load times.

6. **Accessibility**: Include proper ARIA labels and keyboard navigation support.

## Future Enhancements

- **Tab Persistence**: Remember the last active tab across sessions
- **Dynamic Tab Loading**: Load tab content on demand
- **Tab Customization**: Allow users to reorder or hide tabs
- **Tab Notifications**: Show notifications/badges on tabs
- **Tab Search**: Search functionality across all tabs
- **Tab Export/Import**: Save and restore tab configurations 
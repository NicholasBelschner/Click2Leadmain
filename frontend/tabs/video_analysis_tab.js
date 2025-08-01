// Video Analysis Tab Component - Athletic Movement Analysis System
class VideoAnalysisTab {
    constructor() {
        this.container = null;
        this.uploadedFiles = [];
        this.analysisResults = [];
        this.isAnalyzing = false;
    }

    create() {
        const container = document.createElement('div');
        container.className = 'tab-content video-analysis-tab';
        container.id = 'video-analysis-tab-content';
        
        container.innerHTML = `
            <div class="tab-section">
                <h3>📹 Athletic Movement Analysis</h3>
                <div class="analysis-overview">
                    <p class="analysis-description">
                        Upload videos and photos for AI-powered movement analysis. Perfect your athletic techniques 
                        with personalized feedback from our AI agents.
                    </p>
                    <div class="analysis-status">
                        <div class="status-indicator active"></div>
                        <span class="status-text">Analysis System Ready</span>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>📤 Upload Interface</h3>
                <div class="upload-container">
                    <div class="upload-area" id="upload-area">
                        <div class="upload-icon">📁</div>
                        <div class="upload-text">
                            <h4>Drag & Drop Files Here</h4>
                            <p>or click to browse</p>
                        </div>
                        <input type="file" id="file-input" multiple accept="video/*,image/*" style="display: none;">
                    </div>
                    
                    <div class="upload-options">
                        <div class="upload-option">
                            <h4>🎥 Video Analysis</h4>
                            <p>Upload workout videos, sports footage, or movement sequences</p>
                            <ul>
                                <li>Form correction suggestions</li>
                                <li>Movement pattern analysis</li>
                                <li>Progress tracking over time</li>
                            </ul>
                        </div>
                        <div class="upload-option">
                            <h4>📸 Photo Analysis</h4>
                            <p>Upload before/after photos or movement snapshots</p>
                            <ul>
                                <li>Posture analysis</li>
                                <li>Before/after comparisons</li>
                                <li>Technique improvement tips</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>📋 Uploaded Files</h3>
                <div class="files-container" id="files-container">
                    <div class="no-files-message">
                        <p>No files uploaded yet. Drag and drop videos or photos to get started!</p>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>🔍 Analysis Results</h3>
                <div class="analysis-results-container" id="analysis-results">
                    <div class="no-analysis-message">
                        <p>Upload files to see analysis results and AI recommendations.</p>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>🤖 AI Agent Integration</h3>
                <div class="agent-integration">
                    <div class="agent-card">
                        <div class="agent-header">
                            <div class="agent-icon">🏃‍♂️</div>
                            <div class="agent-info">
                                <div class="agent-name">Movement Analysis Specialist</div>
                                <div class="agent-status">Ready for Analysis</div>
                            </div>
                        </div>
                        <div class="agent-description">
                            Analyzes form and technique, identifies areas for improvement, and provides specific correction advice.
                        </div>
                        <div class="agent-actions">
                            <button class="action-btn" onclick="videoAnalysisTab.analyzeWithAgent('movement')">
                                🔍 Analyze Movement
                            </button>
                        </div>
                    </div>
                    
                    <div class="agent-card">
                        <div class="agent-header">
                            <div class="agent-icon">💪</div>
                            <div class="agent-info">
                                <div class="agent-name">Sports Performance Coach</div>
                                <div class="agent-status">Ready for Analysis</div>
                            </div>
                        </div>
                        <div class="agent-description">
                            Evaluates athletic performance, suggests training modifications, and tracks progress over time.
                        </div>
                        <div class="agent-actions">
                            <button class="action-btn" onclick="videoAnalysisTab.analyzeWithAgent('performance')">
                                📊 Performance Review
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>📈 Progress Tracking</h3>
                <div class="progress-tracking">
                    <div class="progress-chart" id="progress-chart">
                        <h4>Movement Improvement Over Time</h4>
                        <div class="chart-placeholder">Progress chart will appear here</div>
                    </div>
                    
                    <div class="progress-metrics">
                        <div class="metric-card">
                            <div class="metric-icon">🎯</div>
                            <div class="metric-value">87%</div>
                            <div class="metric-label">Form Accuracy</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-icon">📈</div>
                            <div class="metric-value">+12%</div>
                            <div class="metric-label">Improvement</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-icon">📊</div>
                            <div class="metric-value">24</div>
                            <div class="metric-label">Analyses</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>🎯 Training Recommendations</h3>
                <div class="recommendations-container" id="recommendations">
                    <div class="recommendation-card">
                        <div class="recommendation-header">
                            <span class="recommendation-icon">💡</span>
                            <span class="recommendation-title">Form Improvement</span>
                        </div>
                        <div class="recommendation-content">
                            <p>Based on your recent squat analysis, focus on keeping your knees aligned with your toes and maintaining a neutral spine position.</p>
                        </div>
                        <div class="recommendation-actions">
                            <button class="recommendation-btn">View Exercise</button>
                            <button class="recommendation-btn">Practice Drill</button>
                        </div>
                    </div>
                    
                    <div class="recommendation-card">
                        <div class="recommendation-header">
                            <span class="recommendation-icon">🎯</span>
                            <span class="recommendation-title">Strength Building</span>
                        </div>
                        <div class="recommendation-content">
                            <p>Your deadlift form shows good hip hinge mechanics. Consider adding Romanian deadlifts to improve hamstring flexibility.</p>
                        </div>
                        <div class="recommendation-actions">
                            <button class="recommendation-btn">View Exercise</button>
                            <button class="recommendation-btn">Practice Drill</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.container = container;
        this.setupEventListeners();
        
        return container;
    }

    setupEventListeners() {
        const uploadArea = this.container.querySelector('#upload-area');
        const fileInput = this.container.querySelector('#file-input');
        
        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        // File input change
        fileInput.addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files);
        });
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            this.handleFileUpload(e.dataTransfer.files);
        });
    }

    handleFileUpload(files) {
        Array.from(files).forEach(file => {
            this.addFile(file);
        });
    }

    addFile(file) {
        const fileId = Date.now() + Math.random();
        const fileData = {
            id: fileId,
            name: file.name,
            type: file.type,
            size: file.size,
            uploadTime: new Date(),
            status: 'uploaded'
        };
        
        this.uploadedFiles.push(fileData);
        this.updateFilesDisplay();
        this.autoAnalyze(fileData);
    }

    updateFilesDisplay() {
        const filesContainer = this.container.querySelector('#files-container');
        
        if (this.uploadedFiles.length === 0) {
            filesContainer.innerHTML = `
                <div class="no-files-message">
                    <p>No files uploaded yet. Drag and drop videos or photos to get started!</p>
                </div>
            `;
            return;
        }
        
        const filesHTML = this.uploadedFiles.map(file => `
            <div class="file-item" data-file-id="${file.id}">
                <div class="file-icon">${this.getFileIcon(file.type)}</div>
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-details">
                        <span class="file-size">${this.formatFileSize(file.size)}</span>
                        <span class="file-time">${file.uploadTime.toLocaleTimeString()}</span>
                    </div>
                </div>
                <div class="file-status">
                    <span class="status-badge ${file.status}">${file.status}</span>
                </div>
                <div class="file-actions">
                    <button class="action-btn small" onclick="videoAnalysisTab.analyzeFile('${file.id}')">
                        🔍 Analyze
                    </button>
                    <button class="action-btn small" onclick="videoAnalysisTab.deleteFile('${file.id}')">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `).join('');
        
        filesContainer.innerHTML = filesHTML;
    }

    getFileIcon(type) {
        if (type.startsWith('video/')) {
            return '🎥';
        } else if (type.startsWith('image/')) {
            return '📸';
        } else {
            return '📄';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    autoAnalyze(fileData) {
        fileData.status = 'analyzing';
        this.updateFilesDisplay();
        
        // Simulate analysis
        setTimeout(() => {
            fileData.status = 'analyzed';
            this.addAnalysisResult(fileData);
            this.updateFilesDisplay();
        }, 3000);
    }

    analyzeFile(fileId) {
        const file = this.uploadedFiles.find(f => f.id == fileId);
        if (file) {
            file.status = 'analyzing';
            this.updateFilesDisplay();
            
            setTimeout(() => {
                file.status = 'analyzed';
                this.addAnalysisResult(file);
                this.updateFilesDisplay();
            }, 2000);
        }
    }

    deleteFile(fileId) {
        this.uploadedFiles = this.uploadedFiles.filter(f => f.id != fileId);
        this.updateFilesDisplay();
    }

    addAnalysisResult(fileData) {
        const result = {
            id: Date.now(),
            fileId: fileData.id,
            fileName: fileData.name,
            analysis: this.generateMockAnalysis(fileData),
            timestamp: new Date()
        };
        
        this.analysisResults.push(result);
        this.updateAnalysisDisplay();
    }

    generateMockAnalysis(fileData) {
        const analyses = [
            "Good form overall! Focus on maintaining proper alignment during the movement.",
            "Excellent technique! Consider adding more weight to challenge yourself.",
            "Form needs improvement. Focus on keeping your core engaged throughout the movement.",
            "Great progress! Your form has improved significantly since the last analysis.",
            "Pay attention to your breathing pattern. Try to exhale during the exertion phase."
        ];
        
        return analyses[Math.floor(Math.random() * analyses.length)];
    }

    updateAnalysisDisplay() {
        const resultsContainer = this.container.querySelector('#analysis-results');
        
        if (this.analysisResults.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-analysis-message">
                    <p>Upload files to see analysis results and AI recommendations.</p>
                </div>
            `;
            return;
        }
        
        const resultsHTML = this.analysisResults.map(result => `
            <div class="analysis-result" data-result-id="${result.id}">
                <div class="result-header">
                    <div class="result-file">${result.fileName}</div>
                    <div class="result-time">${result.timestamp.toLocaleTimeString()}</div>
                </div>
                <div class="result-content">
                    <p>${result.analysis}</p>
                </div>
                <div class="result-actions">
                    <button class="action-btn small" onclick="videoAnalysisTab.viewDetailedAnalysis('${result.id}')">
                        📊 View Details
                    </button>
                    <button class="action-btn small" onclick="videoAnalysisTab.shareAnalysis('${result.id}')">
                        📤 Share
                    </button>
                </div>
            </div>
        `).join('');
        
        resultsContainer.innerHTML = resultsHTML;
    }

    analyzeWithAgent(agentType) {
        console.log(`Analyzing with ${agentType} agent...`);
        // Agent analysis logic
    }

    viewDetailedAnalysis(resultId) {
        console.log(`Viewing detailed analysis for result ${resultId}...`);
        // Detailed analysis view logic
    }

    shareAnalysis(resultId) {
        console.log(`Sharing analysis result ${resultId}...`);
        // Share analysis logic
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
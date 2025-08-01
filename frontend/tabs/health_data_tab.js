// Health Data Tab Component - Apple Watch Integration
class HealthDataTab {
    constructor() {
        this.container = null;
        this.dataContainer = null;
        this.isConnected = false;
        this.healthData = {
            heartRate: [],
            sleep: [],
            activity: [],
            vitals: [],
            workouts: []
        };
    }

    create() {
        const container = document.createElement('div');
        container.className = 'tab-content health-data-tab';
        container.id = 'health-data-tab-content';
        
        container.innerHTML = `
            <div class="tab-section">
                <h3>📱 Apple Watch Health Data</h3>
                <div class="health-connection-status">
                    <div class="connection-indicator ${this.isConnected ? 'connected' : 'disconnected'}"></div>
                    <span class="connection-text">${this.isConnected ? 'Connected to Apple Watch' : 'Not connected to Apple Watch'}</span>
                    <button class="connect-btn" onclick="healthDataTab.connectToWatch()">
                        ${this.isConnected ? 'Disconnect' : 'Connect to Apple Watch'}
                    </button>
                </div>
            </div>

            <div class="tab-section">
                <h3>❤️ Heart Rate & Vitals</h3>
                <div class="health-metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon">❤️</div>
                        <div class="metric-value" id="current-heart-rate">--</div>
                        <div class="metric-label">Current Heart Rate</div>
                        <div class="metric-unit">BPM</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">🫁</div>
                        <div class="metric-value" id="respiratory-rate">--</div>
                        <div class="metric-label">Respiratory Rate</div>
                        <div class="metric-unit">Breaths/min</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">🩸</div>
                        <div class="metric-value" id="blood-oxygen">--</div>
                        <div class="metric-label">Blood Oxygen</div>
                        <div class="metric-unit">%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">🌡️</div>
                        <div class="metric-value" id="body-temperature">--</div>
                        <div class="metric-label">Body Temperature</div>
                        <div class="metric-unit">°F</div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>😴 Sleep Analysis</h3>
                <div class="sleep-data-container">
                    <div class="sleep-summary">
                        <div class="sleep-metric">
                            <span class="sleep-label">Last Night's Sleep:</span>
                            <span class="sleep-value" id="sleep-duration">--</span>
                        </div>
                        <div class="sleep-metric">
                            <span class="sleep-label">Sleep Quality:</span>
                            <span class="sleep-value" id="sleep-quality">--</span>
                        </div>
                        <div class="sleep-metric">
                            <span class="sleep-label">Deep Sleep:</span>
                            <span class="sleep-value" id="deep-sleep">--</span>
                        </div>
                        <div class="sleep-metric">
                            <span class="sleep-label">REM Sleep:</span>
                            <span class="sleep-value" id="rem-sleep">--</span>
                        </div>
                    </div>
                    <div class="sleep-chart" id="sleep-chart">
                        <div class="chart-placeholder">Sleep pattern chart will appear here</div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>🏃‍♂️ Activity & Workouts</h3>
                <div class="activity-data-container">
                    <div class="activity-rings">
                        <div class="ring-container">
                            <div class="ring" id="move-ring">
                                <div class="ring-fill" style="--fill: 75%"></div>
                                <div class="ring-label">Move</div>
                                <div class="ring-value">750/1000 cal</div>
                            </div>
                        </div>
                        <div class="ring-container">
                            <div class="ring" id="exercise-ring">
                                <div class="ring-fill" style="--fill: 60%"></div>
                                <div class="ring-label">Exercise</div>
                                <div class="ring-value">30/30 min</div>
                            </div>
                        </div>
                        <div class="ring-container">
                            <div class="ring" id="stand-ring">
                                <div class="ring-fill" style="--fill: 90%"></div>
                                <div class="ring-label">Stand</div>
                                <div class="ring-value">9/12 hours</div>
                            </div>
                        </div>
                    </div>
                    <div class="recent-workouts" id="recent-workouts">
                        <h4>Recent Workouts</h4>
                        <div class="workout-list">
                            <div class="workout-item">
                                <div class="workout-icon">🏃‍♂️</div>
                                <div class="workout-details">
                                    <div class="workout-name">Outdoor Run</div>
                                    <div class="workout-time">Today, 7:30 AM</div>
                                    <div class="workout-stats">5.2 miles • 42:15 • 487 cal</div>
                                </div>
                            </div>
                            <div class="workout-item">
                                <div class="workout-icon">💪</div>
                                <div class="workout-details">
                                    <div class="workout-name">Strength Training</div>
                                    <div class="workout-time">Yesterday, 6:00 PM</div>
                                    <div class="workout-stats">45 min • 312 cal</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>📊 Health Trends</h3>
                <div class="trends-container">
                    <div class="trend-chart" id="heart-rate-trend">
                        <h4>Heart Rate Trends (7 days)</h4>
                        <div class="chart-placeholder">Heart rate trend chart will appear here</div>
                    </div>
                    <div class="trend-chart" id="activity-trend">
                        <h4>Activity Trends (7 days)</h4>
                        <div class="chart-placeholder">Activity trend chart will appear here</div>
                    </div>
                </div>
            </div>

            <div class="tab-section">
                <h3>🤖 AI Health Analysis</h3>
                <div class="ai-analysis-container">
                    <div class="analysis-card">
                        <div class="analysis-header">
                            <span class="analysis-icon">🧠</span>
                            <span class="analysis-title">Neural Network Analysis</span>
                        </div>
                        <div class="analysis-content" id="health-analysis">
                            <p>Connect your Apple Watch to get personalized health insights and recommendations from our AI agents.</p>
                        </div>
                    </div>
                    <div class="health-recommendations" id="health-recommendations">
                        <h4>AI Recommendations</h4>
                        <div class="recommendation-list">
                            <div class="recommendation-item">
                                <span class="recommendation-icon">💡</span>
                                <span class="recommendation-text">Based on your sleep patterns, consider going to bed 30 minutes earlier for better recovery.</span>
                            </div>
                            <div class="recommendation-item">
                                <span class="recommendation-icon">💡</span>
                                <span class="recommendation-text">Your heart rate variability suggests good cardiovascular fitness. Keep up the excellent work!</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.container = container;
        this.dataContainer = container.querySelector('#health-data-tab-content');
        
        return container;
    }

    connectToWatch() {
        // Simulate Apple Watch connection
        this.isConnected = !this.isConnected;
        this.updateConnectionStatus();
        
        if (this.isConnected) {
            this.simulateDataStream();
        }
    }

    updateConnectionStatus() {
        const indicator = this.container.querySelector('.connection-indicator');
        const text = this.container.querySelector('.connection-text');
        const button = this.container.querySelector('.connect-btn');
        
        if (this.isConnected) {
            indicator.className = 'connection-indicator connected';
            text.textContent = 'Connected to Apple Watch';
            button.textContent = 'Disconnect';
        } else {
            indicator.className = 'connection-indicator disconnected';
            text.textContent = 'Not connected to Apple Watch';
            button.textContent = 'Connect to Apple Watch';
        }
    }

    simulateDataStream() {
        if (!this.isConnected) return;
        
        // Simulate real-time heart rate updates
        setInterval(() => {
            if (this.isConnected) {
                const heartRate = Math.floor(Math.random() * 40) + 60; // 60-100 BPM
                this.updateHeartRate(heartRate);
            }
        }, 5000);
        
        // Simulate other health metrics
        this.updateVitals();
        this.updateSleepData();
        this.updateActivityData();
    }

    updateHeartRate(rate) {
        const element = this.container.querySelector('#current-heart-rate');
        if (element) {
            element.textContent = rate;
            element.className = 'metric-value ' + (rate > 80 ? 'high' : rate < 70 ? 'low' : 'normal');
        }
    }

    updateVitals() {
        const respiratoryRate = Math.floor(Math.random() * 6) + 12; // 12-18 breaths/min
        const bloodOxygen = Math.floor(Math.random() * 5) + 95; // 95-100%
        const bodyTemp = (Math.random() * 2 + 97.5).toFixed(1); // 97.5-99.5°F
        
        this.container.querySelector('#respiratory-rate').textContent = respiratoryRate;
        this.container.querySelector('#blood-oxygen').textContent = bloodOxygen;
        this.container.querySelector('#body-temperature').textContent = bodyTemp;
    }

    updateSleepData() {
        const sleepDuration = '7h 23m';
        const sleepQuality = 'Good';
        const deepSleep = '1h 45m';
        const remSleep = '2h 12m';
        
        this.container.querySelector('#sleep-duration').textContent = sleepDuration;
        this.container.querySelector('#sleep-quality').textContent = sleepQuality;
        this.container.querySelector('#deep-sleep').textContent = deepSleep;
        this.container.querySelector('#rem-sleep').textContent = remSleep;
    }

    updateActivityData() {
        // Update activity rings with simulated data
        const moveRing = this.container.querySelector('#move-ring .ring-fill');
        const exerciseRing = this.container.querySelector('#exercise-ring .ring-fill');
        const standRing = this.container.querySelector('#stand-ring .ring-fill');
        
        if (moveRing) moveRing.style.setProperty('--fill', Math.random() * 100 + '%');
        if (exerciseRing) exerciseRing.style.setProperty('--fill', Math.random() * 100 + '%');
        if (standRing) standRing.style.setProperty('--fill', Math.random() * 100 + '%');
    }

    updateHealthAnalysis(analysis) {
        const analysisElement = this.container.querySelector('#health-analysis');
        if (analysisElement) {
            analysisElement.innerHTML = analysis;
        }
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
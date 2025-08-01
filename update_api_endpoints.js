// Script to update API endpoints for production deployment
// Run this after you get your Render URL

const fs = require('fs');
const path = require('path');

// Read the script.js file
const scriptPath = path.join(__dirname, 'frontend', 'script.js');
let content = fs.readFileSync(scriptPath, 'utf8');

// Replace all API endpoints to use CONFIG.API_BASE_URL
const replacements = [
    ["fetch('/api/status'", "fetch(`${CONFIG.API_BASE_URL}/api/status`"],
    ["fetch('/api/conversation/process'", "fetch(`${CONFIG.API_BASE_URL}/api/conversation/process`"],
    ["fetch('/api/agents/create'", "fetch(`${CONFIG.API_BASE_URL}/api/agents/create`"],
    ["fetch('/api/agents/list'", "fetch(`${CONFIG.API_BASE_URL}/api/agents/list`"],
    ["fetch('/api/conversation/exchange'", "fetch(`${CONFIG.API_BASE_URL}/api/conversation/exchange`"],
    ["fetch('/api/conversation/full'", "fetch(`${CONFIG.API_BASE_URL}/api/conversation/full`"],
    ["fetch('/api/thoughts/clear'", "fetch(`${CONFIG.API_BASE_URL}/api/thoughts/clear`"],
    ["fetch('/api/learning/stats'", "fetch(`${CONFIG.API_BASE_URL}/api/learning/stats`"],
    ["fetch('/api/thoughts/stream'", "fetch(`${CONFIG.API_BASE_URL}/api/thoughts/stream`"]
];

replacements.forEach(([old, new_]) => {
    content = content.replace(new RegExp(old.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), new_);
});

// Write back to file
fs.writeFileSync(scriptPath, content);

console.log('✅ API endpoints updated for production deployment!');
console.log('📝 Remember to update CONFIG.API_BASE_URL with your Render URL'); 
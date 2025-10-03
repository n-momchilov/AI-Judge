#!/usr/bin/env python3
"""
Simple Web UI for AI GDPR Judge using Flask
"""

from flask import Flask, render_template, request, jsonify
import json
import threading
import webbrowser
import time
from gdpr_judge import GDPRJudge
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global judge instance
judge = None

def initialize_judge():
    """Initialize the GDPR Judge"""
    global judge
    try:
        judge = GDPRJudge()
        logger.info("AI GDPR Judge initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize AI Judge: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze GDPR compliance"""
    try:
        data = request.get_json()
        scenario = data.get('scenario', '').strip()
        context = data.get('context', {})
        
        if not scenario:
            return jsonify({'error': 'Please provide a scenario to analyze'}), 400
        
        if not judge:
            return jsonify({'error': 'AI Judge not initialized'}), 500
        
        # Perform analysis
        analysis = judge.analyze_gdpr_compliance(scenario, context)
        
        # Convert to JSON-serializable format
        result = {
            'issue': analysis.issue,
            'applicable_articles': analysis.applicable_articles,
            'legal_requirements': analysis.legal_requirements,
            'compliance_checklist': analysis.compliance_checklist,
            'risk_assessment': analysis.risk_assessment,
            'recommendations': analysis.recommendations,
            'confidence_score': analysis.confidence_score,
            'supporting_passages': analysis.supporting_passages,
            'precedents': [
                {
                    'case_name': p.case_name,
                    'court': p.court,
                    'year': p.year,
                    'key_points': p.key_points,
                    'gdpr_articles': p.gdpr_articles,
                    'relevance_score': p.relevance_score
                }
                for p in analysis.precedents
            ]
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/articles')
def get_articles():
    """Get GDPR articles"""
    try:
        if not judge:
            return jsonify({'error': 'AI Judge not initialized'}), 500
        
        return jsonify(judge.gdpr_knowledge['articles'])
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        return jsonify({'error': f'Failed to get articles: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'judge_initialized': judge is not None
    })

def create_templates():
    """Create HTML templates"""
    import os
    
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Main HTML template
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI GDPR Judge ⚖️</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .main-content {
            padding: 30px;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        textarea, select, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        textarea:focus, select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results {
            display: none;
            margin-top: 30px;
        }
        
        .result-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        
        .result-section h3 {
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .result-section h3::before {
            content: "⚖️";
            margin-right: 10px;
        }
        
        .article-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .article-tag {
            background: #e3f2fd;
            color: #1976d2;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .requirement-list, .checklist-list, .recommendation-list {
            list-style: none;
        }
        
        .requirement-list li, .checklist-list li, .recommendation-list li {
            background: white;
            margin: 8px 0;
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid #667eea;
        }
        
        .risk-assessment {
            padding: 15px;
            border-radius: 8px;
            font-weight: 600;
        }
        
        .risk-low {
            background: #e8f5e8;
            color: #2e7d32;
            border-left: 4px solid #4caf50;
        }
        
        .risk-medium {
            background: #fff3e0;
            color: #f57c00;
            border-left: 4px solid #ff9800;
        }
        
        .risk-high {
            background: #ffebee;
            color: #c62828;
            border-left: 4px solid #f44336;
        }
        
        .confidence-score {
            text-align: center;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .confidence-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%);
            transition: width 0.3s ease;
        }
        
        .precedent-item {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .precedent-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        
        .precedent-meta {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #f44336;
            margin: 20px 0;
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 24px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
            font-weight: 600;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .main-content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚖️ AI GDPR Judge</h1>
            <p>Specialized AI Assistant for GDPR Compliance and EU Data Protection Law</p>
        </div>
        
        <div class="main-content">
            <div class="tabs">
                <div class="tab active" onclick="switchTab('analysis')">🔍 Legal Analysis</div>
                <div class="tab" onclick="switchTab('articles')">📚 Article Reference</div>
                <div class="tab" onclick="switchTab('about')">ℹ️ About</div>
            </div>
            
            <!-- Analysis Tab -->
            <div id="analysis" class="tab-content active">
                <div class="input-section">
                    <div class="input-group">
                        <label for="scenario">Describe your GDPR scenario or question:</label>
                        <textarea id="scenario" placeholder="Example: A company wants to collect customer data for marketing without explicit consent, claiming legitimate interest as the legal basis..."></textarea>
                    </div>
                    
                    <div class="input-group">
                        <label for="dataTypes">Data Types Involved:</label>
                        <select id="dataTypes" multiple>
                            <option value="Personal Data">Personal Data</option>
                            <option value="Special Categories">Special Categories</option>
                            <option value="Biometric Data">Biometric Data</option>
                            <option value="Location Data">Location Data</option>
                            <option value="Financial Data">Financial Data</option>
                            <option value="Health Data">Health Data</option>
                        </select>
                    </div>
                    
                    <div class="input-group">
                        <label for="legalBasis">Claimed Legal Basis:</label>
                        <select id="legalBasis">
                            <option value="">Select legal basis</option>
                            <option value="Consent">Consent</option>
                            <option value="Contract">Contract</option>
                            <option value="Legal Obligation">Legal Obligation</option>
                            <option value="Vital Interests">Vital Interests</option>
                            <option value="Public Task">Public Task</option>
                            <option value="Legitimate Interests">Legitimate Interests</option>
                        </select>
                    </div>
                    
                    <button class="btn" onclick="analyzeScenario()">⚖️ Analyze Compliance</button>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing compliance with GDPR...</p>
                </div>
                
                <div class="results" id="results">
                    <!-- Results will be populated here -->
                </div>
            </div>
            
            <!-- Articles Tab -->
            <div id="articles" class="tab-content">
                <div class="input-group">
                    <label for="articleSearch">Search GDPR Articles:</label>
                    <input type="text" id="articleSearch" placeholder="Search by keyword..." onkeyup="searchArticles()">
                </div>
                <div id="articlesList">
                    <!-- Articles will be populated here -->
                </div>
            </div>
            
            <!-- About Tab -->
            <div id="about" class="tab-content">
                <div class="result-section">
                    <h3>About AI GDPR Judge</h3>
                    <p>The AI GDPR Judge is a specialized artificial intelligence system designed to provide accurate legal analysis and compliance guidance for the General Data Protection Regulation (GDPR) and EU data protection law.</p>
                    
                    <h4>Key Features:</h4>
                    <ul>
                        <li><strong>Comprehensive Legal Analysis:</strong> Analyzes scenarios against GDPR requirements</li>
                        <li><strong>Article-Specific Guidance:</strong> References specific GDPR articles and provisions</li>
                        <li><strong>Case Law Integration:</strong> Incorporates relevant legal precedents and court decisions</li>
                        <li><strong>Risk Assessment:</strong> Evaluates compliance risks and potential violations</li>
                        <li><strong>Practical Recommendations:</strong> Provides actionable compliance guidance</li>
                        <li><strong>Local Processing:</strong> All analysis performed locally for data privacy</li>
                    </ul>
                    
                    <h4>Legal Disclaimer:</h4>
                    <p><strong>This AI system is designed for educational and preliminary analysis purposes only.</strong> It should not be considered as legal advice. For official legal matters, always consult with qualified legal professionals.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let articles = {};
        
        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {
            loadArticles();
        });
        
        function switchTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }
        
        async function analyzeScenario() {
            const scenario = document.getElementById('scenario').value.trim();
            if (!scenario) {
                alert('Please provide a scenario to analyze.');
                return;
            }
            
            const dataTypes = Array.from(document.getElementById('dataTypes').selectedOptions).map(option => option.value);
            const legalBasis = document.getElementById('legalBasis').value;
            
            const context = {
                data_types: dataTypes,
                legal_basis: legalBasis
            };
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        scenario: scenario,
                        context: context
                    })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    displayError(result.error || 'Analysis failed');
                }
            } catch (error) {
                displayError('Network error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function displayResults(analysis) {
            const resultsDiv = document.getElementById('results');
            
            let riskClass = 'risk-low';
            if (analysis.risk_assessment.toLowerCase().includes('high')) {
                riskClass = 'risk-high';
            } else if (analysis.risk_assessment.toLowerCase().includes('medium') || analysis.risk_assessment.toLowerCase().includes('moderate')) {
                riskClass = 'risk-medium';
            }
            
            const confidencePercent = Math.round(analysis.confidence_score * 100);
            
            resultsDiv.innerHTML = `
                <div class="result-section">
                    <h3>📋 Issue Identified</h3>
                    <p>${analysis.issue}</p>
                </div>
                
                <div class="result-section">
                    <h3>📜 Applicable GDPR Articles</h3>
                    <div class="article-list">
                        ${analysis.applicable_articles.map(article => `<span class="article-tag">${article}</span>`).join('')}
                    </div>
                </div>
                
                <div class="result-section">
                    <h3>⚖️ Legal Requirements</h3>
                    <ul class="requirement-list">
                        ${analysis.legal_requirements.map(req => `<li>${req}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="result-section">
                    <h3>✅ Compliance Checklist</h3>
                    <ul class="checklist-list">
                        ${analysis.compliance_checklist.map(check => `<li>${check}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="result-section">
                    <h3>⚠️ Risk Assessment</h3>
                    <div class="risk-assessment ${riskClass}">
                        ${analysis.risk_assessment}
                    </div>
                </div>
                
                <div class="result-section">
                    <h3>💡 Recommendations</h3>
                    <ul class="recommendation-list">
                        ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
                
                ${analysis.precedents.length > 0 ? `
                <div class="result-section">
                    <h3>📚 Relevant Legal Precedents</h3>
                    ${analysis.precedents.map(precedent => `
                        <div class="precedent-item">
                            <div class="precedent-title">${precedent.case_name}</div>
                            <div class="precedent-meta">${precedent.court}, ${precedent.year} (Relevance: ${Math.round(precedent.relevance_score * 100)}%)</div>
                            <ul>
                                ${precedent.key_points.map(point => `<li>${point}</li>`).join('')}
                            </ul>
                            <p><strong>Relevant Articles:</strong> ${precedent.gdpr_articles.join(', ')}</p>
                        </div>
                    `).join('')}
                </div>
                ` : ''}
                
                <div class="confidence-score">
                    <h3>🎯 Analysis Confidence</h3>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                    </div>
                    <p><strong>${confidencePercent}%</strong> confidence level</p>
                    ${confidencePercent < 50 ? '<p style="color: #f44336;">⚠️ Low confidence analysis. Manual legal review strongly recommended.</p>' : 
                      confidencePercent < 80 ? '<p style="color: #ff9800;">ℹ️ Moderate confidence. Consider additional legal consultation for complex matters.</p>' : 
                      '<p style="color: #4caf50;">✅ High confidence analysis.</p>'}
                </div>
            `;
            
            resultsDiv.style.display = 'block';
        }
        
        function displayError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `<div class="error">❌ ${message}</div>`;
            resultsDiv.style.display = 'block';
        }
        
        async function loadArticles() {
            try {
                const response = await fetch('/articles');
                if (response.ok) {
                    articles = await response.json();
                    displayArticles(articles);
                }
            } catch (error) {
                console.error('Failed to load articles:', error);
            }
        }
        
        function displayArticles(articlesToShow) {
            const articlesList = document.getElementById('articlesList');
            articlesList.innerHTML = Object.entries(articlesToShow).map(([article, description]) => `
                <div class="result-section">
                    <h3>${article}</h3>
                    <p>${description}</p>
                </div>
            `).join('');
        }
        
        function searchArticles() {
            const searchTerm = document.getElementById('articleSearch').value.toLowerCase();
            const filteredArticles = {};
            
            Object.entries(articles).forEach(([article, description]) => {
                if (article.toLowerCase().includes(searchTerm) || description.toLowerCase().includes(searchTerm)) {
                    filteredArticles[article] = description;
                }
            });
            
            displayArticles(filteredArticles);
        }
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def run_web_ui(host='localhost', port=5001, debug=False):
    """Run the web UI"""
    print("🚀 Starting AI GDPR Judge Web UI...")
    
    # Initialize the judge
    if not initialize_judge():
        print("❌ Failed to initialize AI Judge. Please check your setup.")
        return False
    
    # Create templates
    create_templates()
    
    print(f"✅ AI GDPR Judge Web UI is running!")
    print(f"🌐 Open your browser and go to: http://{host}:{port}")
    print("⚖️ Ready to analyze GDPR compliance scenarios!")
    print("\nPress Ctrl+C to stop the server.")
    
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 AI GDPR Judge Web UI stopped.")
        return True

if __name__ == "__main__":
    run_web_ui()

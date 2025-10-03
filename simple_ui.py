#!/usr/bin/env python3
"""
Simple Web UI for AI GDPR Judge
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
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

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
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
            max-width: 1000px;
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
        
        textarea, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        textarea:focus, select:focus {
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
            color: #667eea;
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
            background: #fff3e0;
            color: #f57c00;
            border-left: 4px solid #ff9800;
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
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #f44336;
            margin: 20px 0;
        }
        
        .success {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
            margin: 20px 0;
        }
        
        .status {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .status.ready {
            background: #e8f5e8;
            color: #2e7d32;
        }
        
        .status.error {
            background: #ffebee;
            color: #c62828;
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
            <div id="status" class="status ready">
                ✅ AI GDPR Judge is ready to analyze your scenarios
            </div>
            
            <div class="input-section">
                <div class="input-group">
                    <label for="scenario">Describe your GDPR scenario or question:</label>
                    <textarea id="scenario" placeholder="Example: A company wants to collect customer data for marketing without explicit consent, claiming legitimate interest as the legal basis..."></textarea>
                </div>
                
                <div class="input-group">
                    <label for="legalBasis">Claimed Legal Basis (Optional):</label>
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
    </div>

    <script>
        async function analyzeScenario() {
            const scenario = document.getElementById('scenario').value.trim();
            if (!scenario) {
                alert('Please provide a scenario to analyze.');
                return;
            }
            
            const legalBasis = document.getElementById('legalBasis').value;
            
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
                        legal_basis: legalBasis
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
                    <div class="risk-assessment">
                        ${analysis.risk_assessment}
                    </div>
                </div>
                
                <div class="result-section">
                    <h3>💡 Recommendations</h3>
                    <ul class="recommendation-list">
                        ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="confidence-score">
                    <h3>🎯 Analysis Confidence</h3>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                    </div>
                    <p><strong>${confidencePercent}%</strong> confidence level</p>
                    ${confidencePercent < 50 ? '<p style="color: #f44336;">⚠️ Low confidence - manual legal review recommended</p>' : 
                      confidencePercent < 80 ? '<p style="color: #ff9800;">ℹ️ Moderate confidence - consider additional consultation</p>' : 
                      '<p style="color: #4caf50;">✅ High confidence analysis</p>'}
                </div>
            `;
            
            resultsDiv.style.display = 'block';
        }
        
        function displayError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `<div class="error">❌ ${message}</div>`;
            resultsDiv.style.display = 'block';
        }
        
        // Check system status on load
        window.addEventListener('load', async function() {
            try {
                const response = await fetch('/health');
                const status = await response.json();
                
                const statusDiv = document.getElementById('status');
                if (status.judge_initialized) {
                    statusDiv.className = 'status ready';
                    statusDiv.textContent = '✅ AI GDPR Judge is ready to analyze your scenarios';
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.textContent = '❌ AI GDPR Judge not initialized. Please check the server logs.';
                }
            } catch (error) {
                const statusDiv = document.getElementById('status');
                statusDiv.className = 'status error';
                statusDiv.textContent = '❌ Cannot connect to AI GDPR Judge service';
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze GDPR compliance"""
    try:
        data = request.get_json()
        scenario = data.get('scenario', '').strip()
        legal_basis = data.get('legal_basis', '')
        
        if not scenario:
            return jsonify({'error': 'Please provide a scenario to analyze'}), 400
        
        if not judge:
            return jsonify({'error': 'AI Judge not initialized'}), 500
        
        # Prepare context
        context = {}
        if legal_basis:
            context['legal_basis'] = legal_basis
        
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
            'supporting_passages': analysis.supporting_passages
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'judge_initialized': judge is not None
    })

def run_simple_ui(host='localhost', port=5002, debug=False):
    """Run the simple web UI"""
    print("🚀 Starting AI GDPR Judge Simple Web UI...")
    
    # Initialize the judge
    if not initialize_judge():
        print("❌ Failed to initialize AI Judge. Please check your setup.")
        return False
    
    print(f"✅ AI GDPR Judge Simple Web UI is running!")
    print(f"🌐 Open your browser and go to: http://{host}:{port}")
    print("⚖️ Ready to analyze GDPR compliance scenarios!")
    print("\nPress Ctrl+C to stop the server.")
    
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 AI GDPR Judge Simple Web UI stopped.")
        return True

if __name__ == "__main__":
    run_simple_ui()

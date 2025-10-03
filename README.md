# AI GDPR Judge ⚖️

A specialized AI assistant for GDPR compliance and EU data protection law analysis, designed to provide accurate legal guidance with minimal hallucination.

## 🎯 Features

- **Comprehensive Legal Analysis**: Analyzes scenarios against GDPR requirements
- **Article-Specific Guidance**: References specific GDPR articles and provisions  
- **Case Law Integration**: Incorporates relevant legal precedents and court decisions
- **Risk Assessment**: Evaluates compliance risks and potential violations
- **Practical Recommendations**: Provides actionable compliance guidance
- **Local Processing**: All analysis performed locally for data privacy
- **Web Interface**: User-friendly Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama (for local AI model)
- Internet connection (for initial model download)

### Installation

1. **Clone or download this repository**
   ```bash
   cd "Nikola Demo"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the GDPR knowledge base** (run again if you update `data/GDPR.pdf`)
   ```bash
   python data/build_gdpr_corpus.py
   python data/build_gdpr_vector_store.py
   ```

4. **Setup Ollama and AI models**
   ```bash
   python setup_ollama.py
   ```

5. **Start the AI GDPR Judge**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 🔧 Manual Setup (Alternative)

If the automatic setup fails:

1. **Install Ollama manually**
   - Visit [https://ollama.ai](https://ollama.ai)
   - Download and install for your platform

2. **Start Ollama service**
   ```bash
   ollama serve
   ```

3. **Pull a model** (in a new terminal)
   ```bash
   ollama pull llama3.1:8b
   ```

4. **Test the model**
   ```bash
   ollama run llama3.1:8b
   ```

## 📚 Usage

### Web Interface

1. **Legal Analysis Tab**: Enter your GDPR scenario for comprehensive analysis
2. **Compliance Check Tab**: Quick checks for data processing lawfulness
3. **Article Reference Tab**: Browse and search GDPR articles
4. **About Tab**: Learn more about the system

### Python API

```python
from gdpr_judge import GDPRJudge

# Initialize the judge
judge = GDPRJudge()

# Analyze a scenario
scenario = """
A company wants to collect customer email addresses for marketing 
purposes without explicit consent, claiming legitimate interest.
"""

analysis = judge.analyze_gdpr_compliance(scenario)

print(f"Issue: {analysis.issue}")
print(f"Applicable Articles: {analysis.applicable_articles}")
print(f"Risk Assessment: {analysis.risk_assessment}")
```

## 🏛️ Legal Knowledge Base

The AI Judge includes:

- **Complete GDPR Articles**: All 99 articles with descriptions
- **Legal Principles**: 7 core data protection principles
- **Case Law**: Key CJEU decisions and precedents
- **Rights Framework**: Complete data subject rights
- **Compliance Guidelines**: Practical implementation guidance

### Key Legal Precedents Included

- **Google Spain v AEPD** (2014) - Right to be forgotten
- **Schrems I & II** (2015, 2020) - Data transfers and adequacy
- **Weltimmo v NAIH** (2015) - Establishment criteria
- **Google LLC v CNIL** (2019) - Global delisting

## ⚖️ Legal Disclaimer

This AI system is designed for **educational and preliminary analysis purposes only**. It should not be considered as legal advice. For official legal matters, always consult with qualified legal professionals.

## 🔒 Privacy & Security

- **Local Processing**: All AI analysis runs locally on your machine
- **No Data Transmission**: Your scenarios are not sent to external servers
- **GDPR Compliant**: The system itself adheres to data protection principles

## 🛠️ Technical Details

- **AI Model**: Ollama with Llama 3.1 (8B or 70B parameters)
- **Framework**: Streamlit for web interface
- **Language**: Python 3.8+
- **Dependencies**: See `requirements.txt`

## 📊 Model Recommendations

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `llama3.1:8b` | 8B | Fast | Good | General use, quick analysis |
| `llama3.1:70b` | 70B | Slower | Excellent | Complex legal scenarios |
| `mistral:7b` | 7B | Fast | Good | Alternative option |

## 🐛 Troubleshooting

### Common Issues

1. **"Ollama not found"**
   - Install Ollama from [https://ollama.ai](https://ollama.ai)
   - Ensure it's in your PATH

2. **"Model not found"**
   - Run `ollama pull llama3.1:8b`
   - Check available models with `ollama list`

3. **"Connection refused"**
   - Start Ollama service: `ollama serve`
   - Check if port 11434 is available

4. **Low confidence scores**
   - Try a more specific scenario
   - Use the 70B model for complex cases
   - Provide more context

### Getting Help

- Check the Streamlit interface logs
- Verify Ollama is running: `ollama list`
- Test model directly: `ollama run llama3.1:8b`

## 🔄 Updates

To update the system:

1. Pull latest changes
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Update models: `ollama pull llama3.1:8b`

## 📄 License

This project is for educational purposes. Please ensure compliance with all applicable laws and regulations when using for legal analysis.

## 🤝 Contributing

This is an educational project. For improvements or suggestions, please create an issue or pull request.

---

**Remember**: This AI system is a tool to assist with preliminary legal analysis. Always consult qualified legal professionals for official legal advice.

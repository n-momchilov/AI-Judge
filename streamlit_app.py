#!/usr/bin/env python3
"""
Streamlit Web Interface for AI GDPR Judge
"""

import streamlit as st
import json
from gdpr_judge import GDPRJudge, LegalAnalysis
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="AI GDPR Judge",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    html, body {
        font-size: 1.08rem;
        line-height: 1.65;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
        font-size: 1.08rem;
        line-height: 1.65;
    }
    .stTabs [data-baseweb="tab"] button div[data-testid="stMarkdownContainer"] p {
        font-size: 1.12rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.35rem 0.75rem;
    }
    .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label, .stMultiselect label, .stNumberInput label {
        font-size: 1.08rem;
    }
    textarea, input, select {
        font-size: 1.08rem !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox div[role="listbox"] span,
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
    section[data-testid="stSidebar"] .stButton button {
        font-size: 1.08rem;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 1.15rem;
    }
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .legal-analysis {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .risk-high {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    .risk-medium {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    .risk-low {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
    }
    .article-reference {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_judge():
    """Initialize the GDPR Judge with error handling"""
    if 'judge' not in st.session_state:
        try:
            with st.spinner("Initializing AI GDPR Judge..."):
                st.session_state.judge = GDPRJudge()
            st.success("AI Judge initialized successfully!")
        except Exception as e:
            st.error(f"Failed to initialize AI Judge: {e}")
            st.error("Please ensure Ollama is running and the model is available.")
            return None
    return st.session_state.judge

def display_legal_analysis(analysis: LegalAnalysis):
    """Display legal analysis in a structured format"""
    
    # Header
    st.markdown(f"<div class='legal-analysis'><h3>⚖️ Legal Analysis</h3></div>", 
                unsafe_allow_html=True)
    
    # Issue
    st.subheader("📋 Issue Identified")
    st.write(analysis.issue)
    
    # Applicable Articles
    if analysis.applicable_articles:
        st.subheader("📜 Applicable GDPR Articles")
        for article in analysis.applicable_articles:
            st.markdown(f"<div class='article-reference'><strong>{article}</strong></div>", 
                       unsafe_allow_html=True)
    
    # Supporting GDPR Passages
    if analysis.supporting_passages:
        st.subheader("Supporting GDPR Passages")
        for passage in analysis.supporting_passages:
            header = passage.get('article', 'Article ?')
            title = passage.get('title')
            if title:
                header += f" - {title}"
            score = passage.get('score')
            if isinstance(score, (int, float)):
                header += f" (score {score:.2f})"
            with st.expander(header):
                chapter = passage.get('chapter')
                if chapter:
                    st.markdown(f"**Chapter:** {chapter}")
                section = passage.get('section')
                if section:
                    st.markdown(f"**Section:** {section}")
                st.write(passage.get('text', ''))

    # Legal Requirements
    if analysis.legal_requirements:
        st.subheader("⚖️ Legal Requirements")
        for i, req in enumerate(analysis.legal_requirements, 1):
            st.write(f"{i}. {req}")
    
    # Compliance Checklist
    if analysis.compliance_checklist:
        st.subheader("✅ Compliance Checklist")
        checklist_df = pd.DataFrame({
            'Requirement': analysis.compliance_checklist,
            'Status': ['❌ Not Checked'] * len(analysis.compliance_checklist)
        })
        st.dataframe(checklist_df, use_container_width=True)
    
    # Risk Assessment
    st.subheader("⚠️ Risk Assessment")
    risk_class = "risk-low"
    if "high" in analysis.risk_assessment.lower():
        risk_class = "risk-high"
    elif "medium" in analysis.risk_assessment.lower() or "moderate" in analysis.risk_assessment.lower():
        risk_class = "risk-medium"
    
    st.markdown(f"<div class='legal-analysis {risk_class}'>{analysis.risk_assessment}</div>", 
                unsafe_allow_html=True)
    
    # Recommendations
    if analysis.recommendations:
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(analysis.recommendations, 1):
            st.write(f"{i}. {rec}")
    
    # Legal Precedents
    if analysis.precedents:
        st.subheader("📚 Relevant Legal Precedents")
        for precedent in analysis.precedents:
            with st.expander(f"{precedent.case_name} ({precedent.court}, {precedent.year})"):
                st.write(f"**Relevance Score:** {precedent.relevance_score:.2f}")
                st.write("**Key Points:**")
                for point in precedent.key_points:
                    st.write(f"  • {point}")
                st.write(f"**Relevant Articles:** {', '.join(precedent.gdpr_articles)}")
    
    # Confidence Score
    st.subheader("🎯 Analysis Confidence")
    confidence_color = "red" if analysis.confidence_score < 0.5 else "orange" if analysis.confidence_score < 0.8 else "green"
    st.markdown(f"**Confidence Level:** <span style='color: {confidence_color}'>{analysis.confidence_score:.1%}</span>", 
                unsafe_allow_html=True)
    
    if analysis.confidence_score < 0.5:
        st.warning("⚠️ Low confidence analysis. Manual legal review strongly recommended.")
    elif analysis.confidence_score < 0.8:
        st.info("ℹ️ Moderate confidence. Consider additional legal consultation for complex matters.")

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("<h1 class='main-header'>⚖️ AI GDPR Judge</h1>", unsafe_allow_html=True)
    st.markdown("### Specialized AI Assistant for GDPR Compliance and EU Data Protection Law")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Model selection
        model_options = ["llama3.1:8b", "llama3.1:70b", "mistral:7b", "codellama:7b"]
        selected_model = st.selectbox("Select AI Model", model_options, index=0)
        
        # Analysis type
        analysis_type = st.radio(
            "Analysis Type",
            ["General Compliance", "Data Processing Lawfulness", "Rights Assessment", "Breach Analysis"]
        )
        
        st.header("📚 Quick Reference")
        st.markdown("""
        **Key GDPR Articles:**
        - Article 5: Principles
        - Article 6: Lawfulness
        - Article 7: Consent
        - Article 15-22: Data Subject Rights
        - Article 25: Privacy by Design
        - Article 32: Security
        - Article 33-34: Breach Notification
        """)
    
    # Initialize judge
    judge = initialize_judge()
    if judge is None:
        st.stop()
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Legal Analysis", "📊 Compliance Check", "📚 Article Reference", "ℹ️ About"])
    
    with tab1:
        st.header("Legal Scenario Analysis")
        
        # Scenario input
        scenario = st.text_area(
            "Describe your GDPR scenario or question:",
            placeholder="Example: A company wants to collect customer data for marketing without explicit consent...",
            height=150
        )
        
        # Additional context
        with st.expander("Additional Context (Optional)"):
            data_types = st.multiselect(
                "Data Types Involved",
                ["Personal Data", "Special Categories", "Biometric Data", "Location Data", "Financial Data", "Health Data"]
            )
            
            processing_purpose = st.text_input("Processing Purpose", key="context_processing_purpose")
            
            legal_basis = st.selectbox(
                "Claimed Legal Basis",
                ["", "Consent", "Contract", "Legal Obligation", "Vital Interests", "Public Task", "Legitimate Interests"]
            )
            
            data_subjects = st.selectbox(
                "Data Subjects",
                ["", "Adults", "Children", "Employees", "Customers", "Website Visitors", "Patients"]
            )
        
        # Analysis button
        if st.button("⚖️ Analyze Compliance", type="primary"):
            if not scenario.strip():
                st.error("Please provide a scenario to analyze.")
            else:
                # Prepare context
                context = {
                    "data_types": data_types,
                    "processing_purpose": processing_purpose,
                    "legal_basis": legal_basis,
                    "data_subjects": data_subjects,
                    "analysis_type": analysis_type
                }
                
                # Perform analysis
                with st.spinner("Analyzing compliance with GDPR..."):
                    analysis = judge.analyze_gdpr_compliance(scenario, context)
                
                # Display results
                display_legal_analysis(analysis)
                
                # Download option
                analysis_data = {
                    "timestamp": datetime.now().isoformat(),
                    "scenario": scenario,
                    "context": context,
                    "analysis": {
                        "issue": analysis.issue,
                        "applicable_articles": analysis.applicable_articles,
                        "legal_requirements": analysis.legal_requirements,
                        "compliance_checklist": analysis.compliance_checklist,
                        "risk_assessment": analysis.risk_assessment,
                        "recommendations": analysis.recommendations,
                        "confidence_score": analysis.confidence_score
                    }
                }
                
                st.download_button(
                    "📥 Download Analysis Report",
                    json.dumps(analysis_data, indent=2),
                    file_name=f"gdpr_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    with tab2:
        st.header("Quick Compliance Check")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Data Processing Lawfulness")
            purpose = st.text_input("Processing Purpose", key="quick_check_processing_purpose")
            data_types_input = st.text_input("Data Types (comma-separated)")
            legal_basis_input = st.selectbox(
                "Legal Basis",
                ["Consent", "Contract", "Legal Obligation", "Vital Interests", "Public Task", "Legitimate Interests"]
            )
            
            if st.button("Check Lawfulness"):
                if purpose and data_types_input and legal_basis_input:
                    data_types_list = [dt.strip() for dt in data_types_input.split(",")]
                    result = judge.check_data_processing_lawfulness(purpose, data_types_list, legal_basis_input)
                    
                    if result["is_lawful"]:
                        st.success("✅ Processing appears lawful")
                    else:
                        st.error("❌ Processing may not be lawful")
                    
                    st.write("**Reasoning:**", result["reasoning"])
                    
                    if result["alternative_basis"]:
                        st.write("**Alternative Legal Bases:**", ", ".join(result["alternative_basis"]))
                    
                    if result["requirements"]:
                        st.write("**Requirements:**")
                        for req in result["requirements"]:
                            st.write(f"  • {req}")
                else:
                    st.warning("Please fill in all fields")
        
        with col2:
            st.subheader("GDPR Principles Check")
            principles = [
                "Lawfulness, fairness and transparency",
                "Purpose limitation",
                "Data minimisation",
                "Accuracy",
                "Storage limitation",
                "Integrity and confidentiality",
                "Accountability"
            ]
            
            principle_status = {}
            for principle in principles:
                principle_status[principle] = st.checkbox(principle)
            
            if st.button("Assess Principles"):
                compliant_count = sum(principle_status.values())
                total_count = len(principles)
                
                if compliant_count == total_count:
                    st.success(f"✅ All {total_count} principles addressed")
                else:
                    st.warning(f"⚠️ {compliant_count}/{total_count} principles addressed")
                    missing = [p for p, status in principle_status.items() if not status]
                    st.write("**Missing principles:**")
                    for principle in missing:
                        st.write(f"  • {principle}")
    
    with tab3:
        st.header("GDPR Article Reference")
        
        # Article search
        search_term = st.text_input("Search articles by keyword:")
        
        # Display articles
        articles = judge.gdpr_knowledge["articles"]
        
        if search_term:
            filtered_articles = {
                k: v for k, v in articles.items() 
                if search_term.lower() in k.lower() or search_term.lower() in v.lower()
            }
        else:
            filtered_articles = articles
        
        for article, description in filtered_articles.items():
            with st.expander(f"{article}: {description[:50]}..."):
                st.write(description)
                
                # Get detailed explanation
                if st.button(f"Get detailed explanation for {article}"):
                    explanation = judge.get_article_explanation(article)
                    st.write(explanation)
    
    with tab4:
        st.header("About AI GDPR Judge")
        
        st.markdown("""
        ### 🤖 AI GDPR Judge
        
        The AI GDPR Judge is a specialized artificial intelligence system designed to provide 
        accurate legal analysis and compliance guidance for the General Data Protection 
        Regulation (GDPR) and EU data protection law.
        
        ### 🎯 Key Features
        
        - **Comprehensive Legal Analysis**: Analyzes scenarios against GDPR requirements
        - **Article-Specific Guidance**: References specific GDPR articles and provisions
        - **Case Law Integration**: Incorporates relevant legal precedents and court decisions
        - **Risk Assessment**: Evaluates compliance risks and potential violations
        - **Practical Recommendations**: Provides actionable compliance guidance
        - **Local Processing**: All analysis performed locally for data privacy
        
        ### ⚖️ Legal Disclaimer
        
        This AI system is designed for educational and preliminary analysis purposes only. 
        It should not be considered as legal advice. For official legal matters, always 
        consult with qualified legal professionals.
        
        ### 🔧 Technical Details
        
        - **Model**: Ollama with specialized legal training
        - **Knowledge Base**: Comprehensive GDPR articles and case law
        - **Processing**: Local deployment for privacy compliance
        - **Accuracy**: Designed to minimize hallucination through structured prompts
        
        ### 📚 Data Sources
        
        - Official GDPR text and recitals
        - CJEU case law and decisions
        - EDPB guidelines and opinions
        - National supervisory authority decisions
        """)
        
        st.info("""
        **Note**: This system is designed for educational purposes and preliminary analysis. 
        Always consult with qualified legal professionals for official legal advice.
        """)

if __name__ == "__main__":
    main()

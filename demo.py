#!/usr/bin/env python3
"""
Demo script for AI GDPR Judge
"""

import time
from gdpr_judge import GDPRJudge

def print_separator():
    print("=" * 80)

def print_header(title):
    print(f"\n🔍 {title}")
    print("-" * 60)

def demo_scenarios():
    """Run demo scenarios"""
    print("⚖️ AI GDPR Judge - Interactive Demo")
    print_separator()
    
    # Initialize the judge
    print("🤖 Initializing AI GDPR Judge...")
    try:
        judge = GDPRJudge()
        print("✅ AI Judge initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Demo scenarios
    scenarios = [
        {
            "title": "Marketing Without Consent",
            "scenario": """
            A company wants to collect customer email addresses for marketing purposes 
            without explicit consent, claiming legitimate interest as the legal basis.
            They plan to store the data for 5 years and share it with third-party 
            marketing partners.
            """,
            "context": {
                "data_types": ["Personal Data"],
                "legal_basis": "Legitimate Interests",
                "processing_purpose": "Marketing"
            }
        },
        {
            "title": "Employee Monitoring",
            "scenario": """
            An employer wants to monitor employee computer usage, including websites visited,
            emails sent, and keystrokes typed. They claim this is necessary for security
            and productivity purposes.
            """,
            "context": {
                "data_types": ["Personal Data", "Special Categories"],
                "legal_basis": "Legitimate Interests",
                "data_subjects": "Employees"
            }
        },
        {
            "title": "Data Breach Response",
            "scenario": """
            A company discovered that customer personal data was accessed by unauthorized
            third parties. The breach affected 10,000 customers and included names, 
            email addresses, and payment information.
            """,
            "context": {
                "data_types": ["Personal Data", "Financial Data"],
                "analysis_type": "Breach Analysis"
            }
        }
    ]
    
    for i, demo in enumerate(scenarios, 1):
        print_header(f"Demo {i}: {demo['title']}")
        print(f"Scenario: {demo['scenario'].strip()}")
        
        print("\n⚖️ Analyzing compliance...")
        try:
            analysis = judge.analyze_gdpr_compliance(demo['scenario'], demo['context'])
            
            print(f"\n📋 Issue: {analysis.issue}")
            
            if analysis.applicable_articles:
                print(f"\n📜 Applicable Articles: {', '.join(analysis.applicable_articles)}")
            
            if analysis.legal_requirements:
                print(f"\n⚖️ Legal Requirements:")
                for j, req in enumerate(analysis.legal_requirements, 1):
                    print(f"  {j}. {req}")
            
            if analysis.compliance_checklist:
                print(f"\n✅ Compliance Checklist:")
                for j, check in enumerate(analysis.compliance_checklist, 1):
                    print(f"  {j}. {check}")
            
            print(f"\n⚠️ Risk Assessment: {analysis.risk_assessment}")
            
            if analysis.recommendations:
                print(f"\n💡 Recommendations:")
                for j, rec in enumerate(analysis.recommendations, 1):
                    print(f"  {j}. {rec}")
            
            if analysis.precedents:
                print(f"\n📚 Relevant Legal Precedents:")
                for precedent in analysis.precedents[:2]:  # Show top 2
                    print(f"  • {precedent.case_name} ({precedent.court}, {precedent.year})")
                    print(f"    Relevance: {precedent.relevance_score:.1%}")
            
            print(f"\n🎯 Confidence Score: {analysis.confidence_score:.1%}")
            
            if analysis.confidence_score < 0.5:
                print("⚠️ Low confidence - manual legal review recommended")
            elif analysis.confidence_score < 0.8:
                print("ℹ️ Moderate confidence - consider additional consultation")
            else:
                print("✅ High confidence analysis")
                
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
        
        if i < len(scenarios):
            print("\n" + "="*80)
            time.sleep(2)  # Pause between demos
    
    print_separator()
    print("🎉 Demo completed!")
    print("\nTo use the interactive web interface:")
    print("  python3 launch_ui.py")
    print("\nTo use the command line interface:")
    print("  python3 run.py --mode cli")

def interactive_demo():
    """Interactive demo where user can input scenarios"""
    print("⚖️ AI GDPR Judge - Interactive Mode")
    print_separator()
    
    # Initialize the judge
    print("🤖 Initializing AI GDPR Judge...")
    try:
        judge = GDPRJudge()
        print("✅ AI Judge initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    print("\nEnter your GDPR scenarios for analysis (type 'quit' to exit):")
    print_separator()
    
    while True:
        print("\n📝 Enter your scenario:")
        scenario = input("> ").strip()
        
        if scenario.lower() in ['quit', 'exit', 'q']:
            break
        
        if not scenario:
            print("Please enter a scenario to analyze.")
            continue
        
        print("\n⚖️ Analyzing compliance...")
        try:
            analysis = judge.analyze_gdpr_compliance(scenario)
            
            print(f"\n📋 Issue: {analysis.issue}")
            print(f"📜 Articles: {', '.join(analysis.applicable_articles)}")
            print(f"⚠️ Risk: {analysis.risk_assessment}")
            print(f"🎯 Confidence: {analysis.confidence_score:.1%}")
            
            if analysis.recommendations:
                print(f"\n💡 Top Recommendations:")
                for rec in analysis.recommendations[:3]:
                    print(f"  • {rec}")
                    
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
        
        print("\n" + "-"*60)
    
    print("\n👋 Thank you for using AI GDPR Judge!")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_demo()
    else:
        demo_scenarios()

if __name__ == "__main__":
    main()

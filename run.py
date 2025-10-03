#!/usr/bin/env python3
"""
Main runner script for AI GDPR Judge
"""

import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import ollama # type: ignore
        import streamlit
        import pandas
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
    except:
        pass
    
    print("❌ Ollama service is not running")
    print("Please start Ollama: ollama serve")
    return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting AI GDPR Judge...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 AI GDPR Judge stopped")
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

def run_cli():
    """Run the command-line interface"""
    print("🤖 Starting AI GDPR Judge CLI...")
    try:
        from gdpr_judge import GDPRJudge
        
        judge = GDPRJudge()
        print("AI Judge initialized successfully!")
        print("\nEnter your GDPR scenario (or 'quit' to exit):")
        
        while True:
            scenario = input("\n> ")
            if scenario.lower() in ['quit', 'exit', 'q']:
                break
            
            if scenario.strip():
                print("\nAnalyzing...")
                analysis = judge.analyze_gdpr_compliance(scenario)
                
                print(f"\n📋 Issue: {analysis.issue}")
                print(f"📜 Articles: {', '.join(analysis.applicable_articles)}")
                print(f"⚠️ Risk: {analysis.risk_assessment}")
                print(f"💡 Recommendations:")
                for rec in analysis.recommendations:
                    print(f"  • {rec}")
                print(f"🎯 Confidence: {analysis.confidence_score:.1%}")
        
        print("\n👋 Goodbye!")
        
    except Exception as e:
        print(f"❌ Error in CLI: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="AI GDPR Judge")
    parser.add_argument(
        "--mode", 
        choices=["web", "cli"], 
        default="web",
        help="Run mode: web interface or command line"
    )
    parser.add_argument(
        "--skip-checks", 
        action="store_true",
        help="Skip dependency and service checks"
    )
    
    args = parser.parse_args()
    
    print("⚖️ AI GDPR Judge")
    print("=" * 30)
    
    if not args.skip_checks:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Check Ollama service
        if not check_ollama_running():
            print("\nTo start Ollama:")
            print("1. Open a new terminal")
            print("2. Run: ollama serve")
            print("3. Run this script again")
            sys.exit(1)
    
    # Run the appropriate mode
    if args.mode == "web":
        run_streamlit()
    elif args.mode == "cli":
        run_cli()

if __name__ == "__main__":
    main()

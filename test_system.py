#!/usr/bin/env python3
"""
Test script for AI GDPR Judge system
"""

import sys
import traceback

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        import ollama
        print("✅ ollama imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ollama: {e}")
        return False
    
    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import streamlit: {e}")
        return False
    
    try:
        from gdpr_judge import GDPRJudge
        print("✅ GDPRJudge imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import GDPRJudge: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
    
    return True

def test_ollama_connection():
    """Test connection to Ollama service"""
    print("\nTesting Ollama connection...")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
        else:
            print(f"❌ Ollama service returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama service: {e}")
        print("Please ensure Ollama is running: ollama serve")
        return False

def test_gdpr_judge_initialization():
    """Test GDPR Judge initialization"""
    print("\nTesting GDPR Judge initialization...")
    
    try:
        from gdpr_judge import GDPRJudge
        judge = GDPRJudge()
        print("✅ GDPR Judge initialized successfully")
        
        # Test knowledge base
        if judge.gdpr_knowledge and judge.legal_precedents:
            print("✅ Knowledge base loaded successfully")
            print(f"  - {len(judge.gdpr_knowledge['articles'])} GDPR articles")
            print(f"  - {len(judge.legal_precedents)} legal precedents")
        else:
            print("❌ Knowledge base not loaded properly")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize GDPR Judge: {e}")
        traceback.print_exc()
        return False

def test_legal_analysis():
    """Test legal analysis functionality"""
    print("\nTesting legal analysis...")
    
    try:
        from gdpr_judge import GDPRJudge
        judge = GDPRJudge()
        
        # Simple test scenario
        scenario = "A company collects customer emails for marketing without consent"
        
        print(f"Testing scenario: {scenario}")
        analysis = judge.analyze_gdpr_compliance(scenario)
        
        if analysis and analysis.issue:
            print("✅ Legal analysis completed")
            print(f"  - Issue: {analysis.issue}")
            print(f"  - Articles: {len(analysis.applicable_articles)}")
            print(f"  - Confidence: {analysis.confidence_score:.2f}")
            return True
        else:
            print("❌ Legal analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in legal analysis test: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Test configuration system"""
    print("\nTesting configuration...")
    
    try:
        from config import Config, validate_config
        config = Config()
        
        print(f"✅ Configuration loaded")
        print(f"  - Ollama Host: {config.OLLAMA_HOST}")
        print(f"  - Model: {config.OLLAMA_MODEL}")
        print(f"  - Confidence Threshold: {config.DEFAULT_CONFIDENCE_THRESHOLD}")
        
        if validate_config():
            print("✅ Configuration is valid")
            return True
        else:
            print("❌ Configuration validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in configuration test: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI GDPR Judge System Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Ollama Connection", test_ollama_connection),
        ("Configuration", test_config),
        ("GDPR Judge Init", test_gdpr_judge_initialization),
        ("Legal Analysis", test_legal_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nTo start the system:")
        print("  python3 run.py --mode web    # Web interface")
        print("  python3 run.py --mode cli    # Command line")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install dependencies: pip3 install -r requirements.txt")
        print("2. Start Ollama: ollama serve")
        print("3. Pull model: ollama pull llama3.1:8b")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

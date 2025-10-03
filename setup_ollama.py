#!/usr/bin/env python3
"""
Setup script for Ollama and AI GDPR Judge
"""

import subprocess
import sys
import os
import requests
import time

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """Install Ollama"""
    print("Installing Ollama...")
    
    # Detect OS
    if sys.platform == "darwin":  # macOS
        print("Detected macOS. Please install Ollama manually from https://ollama.ai")
        print("After installation, run this script again.")
        return False
    elif sys.platform.startswith("linux"):
        # Install Ollama on Linux
        try:
            subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh'], check=True)
            subprocess.run(['sh', 'install.sh'], check=True)
            return True
        except subprocess.CalledProcessError:
            print("Failed to install Ollama automatically. Please install manually from https://ollama.ai")
            return False
    else:
        print(f"Unsupported platform: {sys.platform}")
        print("Please install Ollama manually from https://ollama.ai")
        return False

def start_ollama_service():
    """Start Ollama service"""
    print("Starting Ollama service...")
    try:
        # Start Ollama in background
        subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for service to start
        return True
    except Exception as e:
        print(f"Failed to start Ollama service: {e}")
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def pull_model(model_name="llama3.1:8b"):
    """Pull the specified model"""
    print(f"Pulling model: {model_name}")
    try:
        result = subprocess.run(['ollama', 'pull', model_name], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"Successfully pulled {model_name}")
            return True
        else:
            print(f"Failed to pull {model_name}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"Timeout while pulling {model_name}")
        return False
    except Exception as e:
        print(f"Error pulling {model_name}: {e}")
        return False

def list_available_models():
    """List available models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Available models:")
            print(result.stdout)
            return True
        else:
            print("Failed to list models")
            return False
    except Exception as e:
        print(f"Error listing models: {e}")
        return False

def test_model(model_name="llama3.1:8b"):
    """Test if the model works"""
    print(f"Testing model: {model_name}")
    try:
        import ollama
        client = ollama.Client()
        response = client.generate(
            model=model_name,
            prompt="Hello, are you working?",
            options={"temperature": 0.1}
        )
        print("✅ Model test successful!")
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up AI GDPR Judge with Ollama")
    print("=" * 50)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("❌ Ollama not found. Installing...")
        if not install_ollama():
            print("❌ Failed to install Ollama. Please install manually.")
            return False
    else:
        print("✅ Ollama is installed")
    
    # Check if Ollama service is running
    if not check_ollama_running():
        print("❌ Ollama service not running. Starting...")
        if not start_ollama_service():
            print("❌ Failed to start Ollama service")
            return False
    else:
        print("✅ Ollama service is running")
    
    # List available models
    print("\n📋 Checking available models...")
    list_available_models()
    
    # Pull recommended model
    recommended_models = ["llama3.1:8b", "llama3.1:70b", "mistral:7b"]
    
    for model in recommended_models:
        print(f"\n🔄 Attempting to pull {model}...")
        if pull_model(model):
            print(f"✅ Successfully pulled {model}")
            
            # Test the model
            if test_model(model):
                print(f"✅ {model} is working correctly")
                print(f"\n🎉 Setup complete! You can now use the AI GDPR Judge with {model}")
                return True
            else:
                print(f"❌ {model} failed testing")
        else:
            print(f"❌ Failed to pull {model}")
    
    print("\n❌ Setup failed. No working models found.")
    print("Please check your internet connection and try again.")
    return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 To start the AI GDPR Judge, run:")
        print("   streamlit run streamlit_app.py")
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")

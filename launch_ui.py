#!/usr/bin/env python3
"""
Launcher script for AI GDPR Judge Web UI
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_ollama_running():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main launcher function"""
    print("🚀 AI GDPR Judge - Web UI Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("gdpr_judge.py").exists():
        print("❌ Please run this script from the AI GDPR Judge directory")
        return False
    
    # Check if virtual environment exists
    if not Path("gdpr_judge_env").exists():
        print("❌ Virtual environment not found. Please run setup first.")
        return False
    
    # Check Ollama
    if not check_ollama_running():
        print("❌ Ollama service not running. Please start it first:")
        print("   ollama serve")
        return False
    
    print("✅ Ollama service is running")
    
    # Try different ports
    ports = [5000, 5001, 5002, 8000, 8080]
    
    for port in ports:
        try:
            print(f"🌐 Starting web UI on port {port}...")
            
            # Start the web UI
            env = os.environ.copy()
            env['PATH'] = str(Path("gdpr_judge_env/bin").absolute()) + ":" + env.get('PATH', '')
            
            process = subprocess.Popen([
                str(Path("gdpr_judge_env/bin/python")),
                "web_ui.py"
            ], env=env)
            
            # Wait a moment for the server to start
            time.sleep(3)
            
            # Check if the process is still running
            if process.poll() is None:
                print(f"✅ Web UI started successfully on port {port}")
                print(f"🌐 Open your browser and go to: http://localhost:{port}")
                
                # Try to open browser
                try:
                    webbrowser.open(f"http://localhost:{port}")
                    print("🌐 Browser opened automatically")
                except:
                    print("🌐 Please open your browser manually")
                
                print("\n⚖️ AI GDPR Judge is ready!")
                print("Press Ctrl+C to stop the server.")
                
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n👋 Stopping AI GDPR Judge...")
                    process.terminate()
                    process.wait()
                    print("✅ Stopped successfully")
                
                return True
            else:
                print(f"❌ Failed to start on port {port}")
                
        except Exception as e:
            print(f"❌ Error starting on port {port}: {e}")
            continue
    
    print("❌ Could not start web UI on any port")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

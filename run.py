#!/usr/bin/env python3
"""
Simple runner script for the Databricks Agent Bricks Tester
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    try:
        # Check if requirements are installed
        try:
            import streamlit
            import openai
            import yaml
            from dotenv import load_dotenv
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("📦 Installing requirements...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed!")

        # Run the app
        print("🚀 Starting Databricks Agent Bricks Tester...")
        print("🌐 The app will open in your browser at http://localhost:8501")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

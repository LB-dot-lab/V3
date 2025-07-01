#!/usr/bin/env python3
"""
RemedyOS - Natural Healing System
Simple runner script for local development
"""

import subprocess
import sys
import os

def main():
    """Run the RemedyOS application"""
    try:
        print("🌱 Starting RemedyOS - Your Natural Healing System")
        print("📍 Application will be available at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 RemedyOS stopped by user")
    except Exception as e:
        print(f"❌ Error starting RemedyOS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
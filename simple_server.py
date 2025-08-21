#!/usr/bin/env python3
"""
Simple server runner without auto-reload (for testing)
Author: nhatchuba
"""

import sys
import os

def main():
    print("[SIMPLE] Starting RAG Search Web Interface (No Auto-reload)...")
    print("=" * 60)
    
    # Import and run the web interface directly
    try:
        from web_search_interface import app, init_search_system
        
        # Initialize search system
        if init_search_system():
            print("[SIMPLE] Web interface starting at: http://localhost:5000")
            print("[SIMPLE] Press Ctrl+C to stop")
            print("=" * 60)
            
            # Run Flask without debug mode
            app.run(host='0.0.0.0', port=5000, debug=False)
        else:
            print("[ERROR] Failed to initialize search system. Please check your setup.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[SIMPLE] Server stopped by user")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

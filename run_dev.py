#!/usr/bin/env python3
"""
Development server runner with enhanced auto-reload capabilities
Author: nhatchuba
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CodeChangeHandler(FileSystemEventHandler):
    """Handler for file system events that trigger server restart"""
    
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_modified = {}
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Only watch Python files and HTML templates
        if not (event.src_path.endswith('.py') or 
                event.src_path.endswith('.html') or
                event.src_path.endswith('.css') or
                event.src_path.endswith('.js')):
            return
            
        # Avoid rapid fire restarts
        current_time = time.time()
        if event.src_path in self.last_modified:
            if current_time - self.last_modified[event.src_path] < 1:
                return
                
        self.last_modified[event.src_path] = current_time
        
        print(f"🔄 File changed: {event.src_path}")
        print("🔄 Restarting server...")
        self.restart_callback()

class DevServer:
    """Development server with file watching and auto-restart"""
    
    def __init__(self):
        self.process = None
        self.observer = None
        self.running = False
        
    def start_server(self):
        """Start the Flask development server"""
        if self.process:
            self.stop_server()
            
        print("🚀 Starting Flask development server...")
        self.process = subprocess.Popen([
            sys.executable, 'web_search_interface.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        # Print server output in real-time
        self.print_server_output()
        
    def stop_server(self):
        """Stop the Flask development server"""
        if self.process:
            print("⏹️  Stopping server...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.process = None
            
    def print_server_output(self):
        """Print server output in real-time"""
        if not self.process:
            return
            
        # Read and print output until server is ready
        startup_complete = False
        while self.process and self.process.poll() is None and not startup_complete:
            try:
                line = self.process.stdout.readline()
                if line:
                    print(line.rstrip())
                    if "Ready for vector search testing!" in line:
                        startup_complete = True
                        break
            except:
                break
                
    def restart_server(self):
        """Restart the server"""
        self.stop_server()
        time.sleep(1)  # Give a moment for cleanup
        self.start_server()
        
    def setup_file_watcher(self):
        """Setup file system watcher for auto-reload"""
        handler = CodeChangeHandler(self.restart_server)
        self.observer = Observer()
        
        # Watch current directory and subdirectories
        watch_paths = [
            '.',
            'templates',
            'rag',
            'embeddings', 
            're_rank',
            'insert_data',
            'llms'
        ]
        
        for path in watch_paths:
            if os.path.exists(path):
                self.observer.schedule(handler, path, recursive=True)
                print(f"👀 Watching: {path}")
                
        self.observer.start()
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Shutting down development server...")
        self.running = False
        self.stop_server()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        sys.exit(0)
        
    def run(self):
        """Main run loop"""
        print("=" * 60)
        print("🔧 RAG Development Server with Auto-Reload")
        print("=" * 60)
        print("📁 Current directory:", os.getcwd())
        print("🐍 Python version:", sys.version.split()[0])
        print("⌨️  Press Ctrl+C to stop")
        print("=" * 60)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Setup file watcher
        self.setup_file_watcher()
        
        # Start server
        self.start_server()
        
        # Keep running
        self.running = True
        try:
            while self.running:
                time.sleep(1)
                # Check if server process is still alive
                if self.process and self.process.poll() is not None:
                    print("❌ Server process died, restarting...")
                    self.start_server()
                    
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    # Check if watchdog is installed
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ watchdog package not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'watchdog'])
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    
    server = DevServer()
    server.run()

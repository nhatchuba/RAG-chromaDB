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
import codecs
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

def safe_print(text):
    """Safely print text with emoji fallback for Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace common emojis with text equivalents
        text = (text.replace("🔄", "[RELOAD]")
                   .replace("🚀", "[START]")
                   .replace("⏹️", "[STOP]")
                   .replace("👀", "[WATCH]")
                   .replace("🔧", "[DEV]")
                   .replace("📁", "[DIR]")
                   .replace("🐍", "[PYTHON]")
                   .replace("⌨️", "[CTRL+C]")
                   .replace("❌", "[ERROR]")
                   .replace("🛑", "[SHUTDOWN]"))
        print(text)

class CodeChangeHandler(FileSystemEventHandler):
    """Handler for file system events that trigger server restart"""
    
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_modified = {}
        self.ignore_patterns = [
            'run_dev.py',  # Don't restart when this file changes to avoid loops
            '__pycache__',
            '.git',
            '.pyc',
            '.log'
        ]
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if pattern in event.src_path:
                return
            
        # Only watch Python files and HTML templates
        if not (event.src_path.endswith('.py') or 
                event.src_path.endswith('.html') or
                event.src_path.endswith('.css') or
                event.src_path.endswith('.js')):
            return
            
        # Avoid rapid fire restarts - increased debounce time
        current_time = time.time()
        if event.src_path in self.last_modified:
            if current_time - self.last_modified[event.src_path] < 2:  # Increased to 2 seconds
                return
                
        self.last_modified[event.src_path] = current_time
        
        safe_print(f"🔄 File changed: {event.src_path}")
        safe_print("🔄 Restarting server...")
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
            
        safe_print("🚀 Starting Flask development server...")
        
        # Setup environment for UTF-8 support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUNBUFFERED'] = '1'
        
        self.process = subprocess.Popen([
            sys.executable, 'web_search_interface.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, env=env)
        
        # Print server output in real-time
        self.print_server_output()
        
    def stop_server(self):
        """Stop the Flask development server"""
        if self.process:
            safe_print("⏹️  Stopping server...")
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
                    safe_print(line.rstrip())
                    if "Ready for vector search testing!" in line or "[SEARCH] Ready for vector search testing!" in line:
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
        
        # Watch specific directories and root for key files
        watch_dirs = [
            'templates',
            'rag',
            'embeddings', 
            're_rank',
            'insert_data',
            'llms'
        ]
        
        # Watch directories
        for path in watch_dirs:
            if os.path.exists(path):
                self.observer.schedule(handler, path, recursive=True)
                safe_print(f"👀 Watching: {path}")
                
        # Watch root directory but with better filtering
        self.observer.schedule(handler, '.', recursive=False)
        safe_print("👀 Watching: . (root files only)")
                
        self.observer.start()
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        safe_print("\n🛑 Shutting down development server...")
        self.running = False
        self.stop_server()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        sys.exit(0)
        
    def run(self):
        """Main run loop"""
        safe_print("=" * 60)
        safe_print("🔧 RAG Development Server with Auto-Reload")
        safe_print("=" * 60)
        safe_print("📁 Current directory: " + os.getcwd())
        safe_print("🐍 Python version: " + sys.version.split()[0])
        safe_print("⌨️  Press Ctrl+C to stop")
        safe_print("=" * 60)
        
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
                    safe_print("❌ Server process died, restarting...")
                    self.start_server()
                    
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

if __name__ == '__main__':
    # Check if watchdog is installed
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        safe_print("❌ watchdog package not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'watchdog'])
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    
    server = DevServer()
    server.run()

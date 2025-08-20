#!/usr/bin/env python3
"""
Web Interface for RAG Vector Search Testing
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setup_search_only import SearchOnlyRAG
from smart_answer_extractor import SmartAnswerExtractor

app = Flask(__name__)
CORS(app)

# Global instances
search_rag = None
answer_extractor = SmartAnswerExtractor()

def init_search_system():
    """Initialize the search system"""
    global search_rag
    try:
        print("🚀 Initializing RAG Search System...")
        search_rag = SearchOnlyRAG()
        print("✅ Search system ready!")
        return True
    except Exception as e:
        print(f"❌ Error initializing search system: {e}")
        return False

@app.route('/')
def index():
    """Main search interface"""
    return render_template('search.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    """Search API endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        limit = data.get('limit', 5)
        use_rerank = data.get('use_rerank', True)
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        if search_rag is None:
            return jsonify({'error': 'Search system not initialized'}), 500
        
        # Record search time
        start_time = time.time()
        results = search_rag.search(query=query, limit=limit, use_rerank=use_rerank)
        search_time = time.time() - start_time
        
        # Add search time to results
        results['search_time'] = round(search_time, 3)
        
        # Extract smart answer
        if 'results' in results and results['results']:
            smart_answer = answer_extractor.extract_smart_answer(query, results['results'])
            results['smart_answer'] = smart_answer
            
            # Mark the best result
            best_result_id = smart_answer['best_result']['_id']
            for i, result in enumerate(results['results']):
                if result['_id'] == best_result_id:
                    results['results'][i]['is_best'] = True
                    break
        
        return jsonify(results)
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """Check system status"""
    return jsonify({
        'status': 'ready' if search_rag else 'not_initialized',
        'message': 'Search system is ready' if search_rag else 'Search system not initialized'
    })

@app.route('/api/sample_queries')
def api_sample_queries():
    """Get sample queries for testing"""
    samples = [
        "iPhone 15 có những màu gì",
        "giá điện thoại iPhone 14",
        "khuyến mãi iPhone",
        "điện thoại Samsung dưới 10 triệu",
        "Xiaomi có RAM 8GB",
        "điện thoại camera 48MP",
        "Oppo pin lâu",
        "Nokia giá rẻ",
        "điện thoại màn hình OLED",
        "Vivo chống nước"
    ]
    return jsonify({'samples': samples})

if __name__ == '__main__':
    print("🌐 Starting RAG Search Web Interface...")
    print("=" * 60)
    
    # Initialize search system
    if init_search_system():
        print(f"🌐 Web interface starting at: http://localhost:5000")
        print("🔍 Ready for vector search testing!")
        print("=" * 60)
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize search system. Please check your setup.")
        sys.exit(1)

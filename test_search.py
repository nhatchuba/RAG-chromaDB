#!/usr/bin/env python3
"""
Quick test script for search-only functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from setup_search_only import SearchOnlyRAG

def test_search():
    print("🚀 Starting Search Test...")
    
    try:
        # Initialize search system
        search_rag = SearchOnlyRAG()
        
        # Test queries
        test_queries = [
            "iPhone 15 có những màu gì",
            "giá điện thoại iPhone 14",
            "khuyến mãi iPhone"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Testing query: '{query}'")
            print('='*60)
            
            results = search_rag.search(query=query, limit=3, use_rerank=True)
            
            if "error" in results:
                print(f"❌ Error: {results['error']}")
            else:
                print(f"✅ Found {results['total_found']} results")
                for i, result in enumerate(results['results'], 1):
                    print(f"\n{i}. ID: {result['_id']}")
                    print(f"   Score: {result.get('score', 'N/A'):.4f}")
                    if 'rerank_score' in result:
                        print(f"   Rerank Score: {result['rerank_score']:.4f}")
                    print(f"   Content: {result['combined_information'][:150]}...")
        
        print(f"\n{'='*60}")
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search()


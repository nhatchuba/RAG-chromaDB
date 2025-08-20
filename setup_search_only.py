"""
Setup RAG Search environment without LLM APIs
Only for vector search functionality
"""
import os
import argparse
from rag.core import RAG
from embeddings import SentenceTransformerEmbedding, EmbeddingConfig
from insert_data import load_csv_to_chromadb
import chromadb
from re_rank import Reranker

class SearchOnlyRAG:
    def __init__(self, embedding_model: str = 'Alibaba-NLP/gte-multilingual-base', 
                 reranker_model: str = 'Alibaba-NLP/gte-multilingual-reranker-base'):
        self.embedding_model = embedding_model
        self.reranker_model = reranker_model
        
        # Setup ChromaDB
        self.setup_chromadb()
        
        # Setup RAG (without LLM)
        self.rag = RAG(
            type='chromadb',
            embeddingName=self.embedding_model,
            llm=None  # No LLM needed for search only
        )
        
        # Setup Reranker
        self.reranker = Reranker(model_name=self.reranker_model)
        
    def setup_chromadb(self):
        """Setup ChromaDB with data if collection doesn't exist"""
        def chromadb_collection_exists(collection_name: str, persist_dir: str = "./chroma_db") -> bool:
            try:
                client = chromadb.PersistentClient(path=persist_dir)
                collections = client.list_collections()
                return any(col.name == collection_name for col in collections)
            except Exception as e:
                print(f"Error checking ChromaDB collection: {e}")
                return False
                
        def csv_exists(folder_path: str) -> list:
            """Check if any CSV file exists in the given folder"""
            if not os.path.isdir(folder_path):
                return []
            csv_paths = [
                os.path.abspath(os.path.join(folder_path, file))
                for file in os.listdir(folder_path)
                if file.lower().endswith(".csv") and os.path.isfile(os.path.join(folder_path, file))
            ]
            return csv_paths
        
        collection_name = self.embedding_model.split('/')[-1]
        
        if not chromadb_collection_exists(collection_name=collection_name):
            csv_files = csv_exists(folder_path="data")
            if len(csv_files) == 0:
                raise FileNotFoundError("No CSV files found in data folder!")
            else:
                print(f"Collection {collection_name} does not exist.")
                print("Creating new collection from CSV data...")
                print(f"Found {len(csv_files)} CSV files.")
                
                for i, csv_file in enumerate(csv_files):              
                    load_csv_to_chromadb(csv_path=csv_file, persist_dir="./chroma_db", model_name=self.embedding_model)
                    print(f"Processed {i+1}/{len(csv_files)} files.")
                print("✅ Data loading completed!")
        else:
            print(f"✅ Collection {collection_name} already exists!")

    def search(self, query: str, limit: int = 4, use_rerank: bool = True):
        """Perform vector search with optional reranking"""
        print(f"🔍 Searching for: '{query}'")
        
        # Vector search
        results = self.rag.vector_search(query, limit=limit*2 if use_rerank else limit)
        
        if not results:
            return {"error": "No results found"}
        
        if use_rerank:
            # Extract passages for reranking
            passages = [result['combined_information'] for result in results]
            
            # Rerank
            scores, ranked_passages = self.reranker(query, passages)
            
            # Combine results with rerank scores
            reranked_results = []
            for i, passage in enumerate(ranked_passages[:limit]):
                # Find original result for this passage
                original_result = next(r for r in results if r['combined_information'] == passage)
                reranked_results.append({
                    **original_result,
                    'rerank_score': scores[i],
                    'rank': i + 1
                })
            results = reranked_results
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results)
        }

def main():
    parser = argparse.ArgumentParser(description="RAG Search Only - No LLM needed")
    parser.add_argument('--embedding_model', type=str, default='Alibaba-NLP/gte-multilingual-base', 
                       help='Embedding model name')
    parser.add_argument('--reranker', type=str, default='Alibaba-NLP/gte-multilingual-reranker-base', 
                       help='Reranker model name')
    parser.add_argument('--query', type=str, help='Search query')
    parser.add_argument('--limit', type=int, default=4, help='Number of results to return')
    parser.add_argument('--no-rerank', action='store_true', help='Disable reranking')
    
    args = parser.parse_args()
    
    print("🚀 Starting RAG Search-Only Environment")
    print("=" * 50)
    print(f"📊 Embedding Model: {args.embedding_model}")
    print(f"🔄 Reranker Model: {args.reranker}")
    print("=" * 50)
    
    # Initialize search system
    search_rag = SearchOnlyRAG(
        embedding_model=args.embedding_model,
        reranker_model=args.reranker
    )
    
    if args.query:
        # Single query mode
        results = search_rag.search(
            query=args.query, 
            limit=args.limit, 
            use_rerank=not args.no_rerank
        )
        
        print(f"\n📋 Results for: '{results['query']}'")
        print("-" * 50)
        
        if "error" in results:
            print(f"❌ {results['error']}")
        else:
            for i, result in enumerate(results['results'], 1):
                print(f"\n{i}. ID: {result['_id']}")
                print(f"   Score: {result.get('score', 'N/A'):.4f}")
                if 'rerank_score' in result:
                    print(f"   Rerank Score: {result['rerank_score']:.4f}")
                print(f"   Content: {result['combined_information'][:200]}...")
    else:
        # Interactive mode
        print("\n🔍 Interactive Search Mode (type 'quit' to exit)")
        while True:
            try:
                query = input("\nEnter your search query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                    
                if query:
                    results = search_rag.search(
                        query=query, 
                        limit=args.limit, 
                        use_rerank=not args.no_rerank
                    )
                    
                    print(f"\n📋 Results for: '{results['query']}'")
                    print("-" * 50)
                    
                    if "error" in results:
                        print(f"❌ {results['error']}")
                    else:
                        for i, result in enumerate(results['results'], 1):
                            print(f"\n{i}. ID: {result['_id']}")
                            print(f"   Score: {result.get('score', 'N/A'):.4f}")
                            if 'rerank_score' in result:
                                print(f"   Rerank Score: {result['rerank_score']:.4f}")
                            print(f"   Content: {result['combined_information'][:200]}...")
                            
            except KeyboardInterrupt:
                break
                
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()


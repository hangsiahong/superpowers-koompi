import os
import lancedb
import pandas as pd
import requests
import json
import argparse
from pathlib import Path

# Configuration
API_URL = "https://ai.koompi.cloud/v1/embeddings"
MODEL = "gemini-embedding-001" # or similar Gemini embedding model

def get_embedding(text):
    api_key = os.environ.get("KCONSOLE_API_KEY")
    if not api_key:
        raise ValueError("KCONSOLE_API_KEY not found")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-BACKEND": "gemini"
    }
    payload = {
        "model": MODEL,
        "input": text
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    return response.json()['data'][0]['embedding']

def chunk_file(file_path, chunk_size=1000):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple chunking by characters (for now)
            return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return []

def index_directory(db_path, target_dir):
    db = lancedb.connect(db_path)
    table_name = "code_index"
    
    data = []
    
    # Iterate through files
    for path in Path(target_dir).rglob('*'):
        if path.is_file() and not any(part.startswith('.') for part in path.parts):
            if path.suffix in ['.py', '.md', '.txt', '.js', '.ts', '.sh', '.json']:
                print(f"Indexing {path}...")
                chunks = chunk_file(path)
                for i, chunk in enumerate(chunks):
                    vector = get_embedding(chunk)
                    if vector:
                        data.append({
                            "vector": vector,
                            "text": chunk,
                            "path": str(path),
                            "chunk_id": i
                        })
    
    if data:
        if table_name in db.table_names():
            db[table_name].add(data)
        else:
            db.create_table(table_name, data=data)
        print("Indexing complete.")
    else:
        print("No data found to index.")

def search(db_path, query, limit=5):
    db = lancedb.connect(db_path)
    table = db.open_table("code_index")
    
    query_vector = get_embedding(query)
    if not query_vector:
        return
    
    results = table.search(query_vector).limit(limit).to_pandas()
    for _, row in results.iterrows():
        print(f"\n--- Result (Score: {row.get('_distance', 'N/A')}) ---")
        print(f"Path: {row['path']}")
        print(f"Content: {row['text'][:200]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", help="Directory to index")
    parser.add_argument("--search", help="Query to search")
    parser.add_argument("--db", default=".lancedb", help="LanceDB path")
    args = parser.parse_args()
    
    if args.index:
        index_directory(args.db, args.index)
    elif args.search:
        search(args.db, args.search)
    else:
        parser.print_help()

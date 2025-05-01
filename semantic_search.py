import numpy as np
import faiss
import os
import google.generativeai as genai
from google.generativeai import embed_content
from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
embedding_model = genai.get_model("models/embedding-001")

embedding_dim = 768  

def extract_nodes_with_embeddings(tree):
    """
    Recursively extract valid nodes that contain proper 768-dimensional embeddings.
    """
    nodes = []

    def recurse(node):
        embedding = node.get("embedding")
        if embedding and isinstance(embedding, list) and len(embedding) == embedding_dim:
            try:
                float_embedding = [float(x) for x in embedding]
                nodes.append({
                    "url": node['url'],
                    "summary": node['summary'],
                    "embedding": float_embedding
                })
            except Exception as e:
                print(f"Skipping node at {node.get('url')} due to invalid embedding values: {e}")
        else:
            print(f"Skipping node at: {node.get('url')}")
            if embedding is None:
                print("  Reason: Embedding is None")
            elif not isinstance(embedding, list):
                print("  Reason: Embedding is not a list")
            elif len(embedding) != embedding_dim:
                print(f"  Reason: Embedding length is {len(embedding)} (expected {embedding_dim})")

        for child in node.get('children', []):
            recurse(child)

    recurse(tree)
    print(f"✅ Total valid nodes with embeddings extracted: {len(nodes)}")
    return nodes

def build_faiss_index(nodes): 
    """
    Build a FAISS index from a list of nodes containing embeddings.
    """
    if not nodes:
        raise ValueError("No valid nodes with embeddings to index.")

    embeddings = np.array([node["embedding"] for node in nodes]).astype("float32")

    if embeddings.shape[1] != embedding_dim:
        raise ValueError(f"Embedding dimension mismatch. Expected {embedding_dim}, but got {embeddings.shape[1]}")

    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)
    print("✅ FAISS index built successfully.")
    return index, nodes

def search(query, index, nodes, top_k=5):
    """
    Perform semantic search using FAISS and Gemini embeddings.
    """
    response = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query"
    )
    query_embedding = response["embedding"]
    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)
    
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append({
            "url": nodes[idx]["url"],
            "summary": nodes[idx]["summary"],
            "score": float(1 - dist)  
        })

    return results

import faiss
import numpy as np
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer


data = Path(__file__).parent.parent.parent.parent / "data"


#SLM model 
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index 
INDEX_PATH = data / "vector_db" / "food_index_ivfpq.faiss"
index = faiss.read_index(str(INDEX_PATH))
METADATA_PATH = data / "embeddings" / "food_metadata.parquet"

food_metadata = pd.read_parquet(METADATA_PATH)

#query embedding function
def embed_query(query):

    vector = model.encode([query])

    return np.array(vector).astype("float32")


#search function 
def search_food(query, top_k=20):

    query_vector = embed_query(query)

    distances, indices = index.search(query_vector, top_k)

    results = food_metadata.iloc[indices[0]].copy()

    results["similarity_score"] = distances[0]

    return results

#generating the candidate
def generate_candidates(query, top_k=20):

    return search_food(query, top_k=top_k)
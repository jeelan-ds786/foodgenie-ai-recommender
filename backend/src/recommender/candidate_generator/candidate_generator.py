import faiss
import numpy as np
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer


DATA_DIR = Path(__file__).resolve().parents[4] / "data"

# Set FAISS to use single thread to avoid segmentation faults
faiss.omp_set_num_threads(1)

# --------------------------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------------------------

model = None


# --------------------------------------------------
# LOAD FAISS INDEX
# --------------------------------------------------

INDEX_PATH = DATA_DIR / "vector_db" / "food_index_ivfpq.faiss"
index = None

def get_index():
    global index
    if index is None:
        index = faiss.read_index(str(INDEX_PATH))
    return index
# --------------------------------------------------
# LOAD FOOD METADATA
# --------------------------------------------------

METADATA_PATH = DATA_DIR / "embeddings" / "food_metadata.parquet"
food_metadata = pd.read_parquet(METADATA_PATH)


# --------------------------------------------------
# QUERY EMBEDDING
# --------------------------------------------------

def embed_query(query):

    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    vector = model.encode([query])

    return np.array(vector).astype("float32")


# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-8)


# --------------------------------------------------
# FAISS SEARCH
# --------------------------------------------------

def search_food(query, top_k=300):

    query_vector = embed_query(query)

    index = get_index()
    distances, indices = index.search(query_vector, top_k)

    results = food_metadata.iloc[indices[0]].copy()

    # Convert distance → similarity
    results["similarity_score"] = 1 - distances[0]

    return results


# --------------------------------------------------
# HYBRID CANDIDATE GENERATION
# --------------------------------------------------

def generate_candidates(query, top_k=300):

    candidates = search_food(query, top_k)

    if len(candidates) == 0:
        return candidates

    # --------------------------------------------------
    # Popularity score
    # --------------------------------------------------

    candidates["rating_norm"] = normalize(candidates["rating_num"])
    candidates["popularity_norm"] = normalize(candidates["rating_count_num"])

    candidates["popularity_score"] = (
        0.6 * candidates["rating_norm"]
        + 0.4 * candidates["popularity_norm"]
    )

    # --------------------------------------------------
    # Hybrid score
    # --------------------------------------------------

    candidates["hybrid_score"] = (
        0.7 * candidates["similarity_score"]
        + 0.3 * candidates["popularity_score"]
    )

    candidates = candidates.sort_values("hybrid_score", ascending=False)

    return candidates.head(top_k)
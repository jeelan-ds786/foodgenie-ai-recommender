import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# load index 
# index = faiss.read_index("../data/vector_db/food_index.faiss")

# load IVF +PQ index
index = faiss.read_index("../data/vector_db/food_index_ivfpq.faiss")

# load metadata
metadata = pd.read_parquet("../data/embeddings/food_metadata.parquet")


def search_food(query, top_k=5):

    query_vector = model.encode([query])

    distances, indices = index.search(query_vector, top_k)

    results = metadata.iloc[indices[0]]

    return results[[
        "restaurant_name",
        "dish_name",
        "category",
        "price",
        "city"
    ]]


print(search_food("spicy idli"))
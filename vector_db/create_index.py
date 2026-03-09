import faiss
import numpy as np


embeddings = np.load("../data/embeddings/food_vectors.npy").astype("float32")

dimension = embeddings.shape[1]

print("Embeddings shape:", embeddings.shape)


nlist = 4096
m = 16
nbits = 8

3 
quantizer = faiss.IndexFlatL2(dimension)

index = faiss.IndexIVFPQ(
    quantizer,
    dimension,
    nlist,
    m,
    nbits
)

print("Training IVF index...")

index.train(embeddings)

print("Training complete")

print("Adding vectors to index...")

index.add(embeddings)

print("Total vectors indexed:", index.ntotal)

faiss.write_index(index, "../data/vector_db/food_index_ivfpq.faiss")

print("IVF + PQ index saved successfully!")
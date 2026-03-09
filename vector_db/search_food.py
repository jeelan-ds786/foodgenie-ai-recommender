import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('food_embedding_model')

dataFrame = pd.read_parquet("../../data/processed/dataPreprocessed_FoodGenie_Dataset.parquet")
  
# Create context-based search_text
dataFrame["search_text"] = (
    "dish: " + dataFrame["dish_name"] +
    " | category: " + dataFrame["category"] +
    " | cuisine: " + dataFrame["cuisine"] +
    " | type: " + dataFrame["veg_or_non_veg"] +
    " | restaurant: " + dataFrame["restaurant_name"]
)

search_text_feature = dataFrame["search_text"].tolist()

embeddings = model.encode(search_text_feature, batch_size=64, show_progress_bar=True)

print(dataFrame.shape)
print(embeddings.shape)

# Save embeddings
np.save("../../data/embeddings/food_vectors.npy", embeddings)

# Save metadata
dataFrame.to_parquet(
    "../../data/embeddings/food_metadata.parquet",
    index=False
)

print("Embeddings and metadata saved successfully")
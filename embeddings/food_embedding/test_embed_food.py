import unittest
from sentence_transformers import SentenceTransformer
import numpy as np


class TestEmbedFood(unittest.TestCase):
    """Test cases for food embedding functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Load the model once for all tests"""
        cls.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def test_model_loads_successfully(self):
        """Test that the model loads without errors"""
        self.assertIsNotNone(self.model)
        self.assertIsInstance(self.model, SentenceTransformer)
    
    def test_embedding_shape(self):
        """Test that embeddings have the correct shape (384 dimensions)"""
        text = "I love eating pizza on weekends."
        embedding = self.model.encode(text)
        self.assertEqual(len(embedding), 384)
    
    def test_embedding_type(self):
        """Test that embedding is a numpy array"""
        text = "I love eating pizza on weekends."
        embedding = self.model.encode(text)
        self.assertIsInstance(embedding, np.ndarray)
    
    def test_embedding_values_are_float(self):
        """Test that embedding values are floats"""
        text = "I love eating pasta."
        embedding = self.model.encode(text)
        self.assertTrue(np.issubdtype(embedding.dtype, np.floating))
    
    def test_different_texts_produce_different_embeddings(self):
        """Test that different texts produce different embeddings"""
        text1 = "I love eating pizza."
        text2 = "I hate eating vegetables."
        
        embedding1 = self.model.encode(text1)
        embedding2 = self.model.encode(text2)
        
        self.assertFalse(np.allclose(embedding1, embedding2))
    
    def test_same_text_produces_same_embedding(self):
        """Test that the same text produces identical embeddings"""
        text = "I love eating pizza on weekends."
        
        embedding1 = self.model.encode(text)
        embedding2 = self.model.encode(text)
        
    
        np.testing.assert_array_equal(embedding1, embedding2)
    
    def test_embedding_magnitude(self):
        """Test that embeddings are normalized (magnitude close to 1)"""
        text = "I love eating sushi."
        embedding = self.model.encode(text)
        
        magnitude = np.linalg.norm(embedding)
        # MiniLM embeddings are usually normalized to unit length
        self.assertAlmostEqual(magnitude, 1.0, places=5)
    
    def test_batch_encoding(self):
        """Test that batch encoding works correctly"""
        texts = [
            "I love eating pizza.",
            "I love eating pasta.",
            "I love eating salad."
        ]
        
        embeddings = self.model.encode(texts)
        
        # Should return 3 embeddings
        self.assertEqual(len(embeddings), 3)
        # Each should have 384 dimensions
        self.assertEqual(embeddings.shape, (3, 384))


if __name__ == '__main__':
    unittest.main()

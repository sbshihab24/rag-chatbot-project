import faiss
import numpy as np
import os
import pickle


class VectorStore:
    def __init__(self, dim: int, path: str, metadata_path: str):
        self.dim = dim
        self.path = path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []

        if os.path.exists(self.path) and os.path.exists(self.metadata_path):
            self.load()
        else:
            self.index = faiss.IndexFlatIP(dim)  # Inner product for cosine similarity (normalize embeddings)

    def add(self, embeddings: np.ndarray, metadatas: list):
        """
        Add embeddings and metadata to the index.
        embeddings: (n, dim)
        metadatas: list of dict with info like doc_id, chunk_id, text snippet
        """
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        """
        Search for top_k similar embeddings to query_embedding
        Returns list of (metadata, score)
        """
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))
        return results

    def save(self):
        faiss.write_index(self.index, self.path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(self.path)
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

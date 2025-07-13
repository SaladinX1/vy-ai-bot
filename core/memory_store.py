# core/memory_store.py

from sentence_transformers import SentenceTransformer
import json, os
import numpy as np

class MemoryStore:
    def __init__(self, path="data/memory.json"):
        self.path = path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)

    def _save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, text):
        embedding = self.model.encode(text).tolist()
        with open(self.path, "r") as f:
            data = json.load(f)
        data.append({"text": text, "embedding": embedding})
        self._save(data)

    def search(self, query, k=3):
        query_emb = self.model.encode(query)
        with open(self.path, "r") as f:
            data = json.load(f)
        sims = []
        for d in data:
            vec = np.array(d["embedding"])
            sim = np.dot(query_emb, vec) / (np.linalg.norm(query_emb) * np.linalg.norm(vec))
            sims.append((sim, d["text"]))
        return [text for _, text in sorted(sims, reverse=True)[:k]]

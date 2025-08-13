from core.embedder import BAAIEmbedder
from core.vector_store import VectorStore
from core.gemini_client import GeminiClient
# Import the centralized config object instead of yaml
from utils.config_loader import config


class RAGPipeline:
    # No need to pass config_path anymore
    def __init__(self):
        # Use the imported config object directly
        self.embedder = BAAIEmbedder() # Assuming BAAIEmbedder will also be updated to use the central config
        self.vector_store = VectorStore(
            dim=768,  # You might want to move this to config.yaml as well
            path=config["vector_store"]["path"],
            metadata_path=config["vector_store"]["metadata_path"],
        )
        self.gemini = GeminiClient() # No longer needs a config path
        self.top_k = config["query"]["top_k"]

    # The query method remains unchanged
    def query(self, question: str, history: list = None) -> str:
        query_emb = self.embedder.embed([question])
        results = self.vector_store.search(query_emb, self.top_k)
        context = "\n---\n".join([m["text"] for m, _ in results])
        answer = self.gemini.generate_answer(question, context, history)
        return answer
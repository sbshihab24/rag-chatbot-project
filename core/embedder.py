import yaml
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np


class BAAIEmbedder:
    def __init__(self, config_path="./config/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        model_name = config["baai_embedding_model_name"]

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def embed(self, texts: list[str]) -> np.ndarray:
        """
        Embed list of texts using the BAAI model.
        Returns numpy array of shape (len(texts), embedding_dim)
        """
        embeddings = []
        with torch.no_grad():
            for text in texts:
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                outputs = self.model(**inputs)
                # Use mean pooling on last hidden state
                last_hidden = outputs.last_hidden_state  # (1, seq_len, hidden_size)
                mask = inputs['attention_mask'].unsqueeze(-1).expand(last_hidden.size()).float()
                masked_hidden = last_hidden * mask
                summed = torch.sum(masked_hidden, dim=1)
                counts = torch.clamp(mask.sum(dim=1), min=1e-9)
                pooled = summed / counts
                embeddings.append(pooled.cpu().numpy()[0])
        return np.vstack(embeddings)

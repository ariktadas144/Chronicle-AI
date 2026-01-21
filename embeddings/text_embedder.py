import open_clip
import torch

class TextEmbedder:
    def __init__(self, model_name='ViT-B-32', pretrained='openai'):
        self.model, _, _ = open_clip.create_model_and_transforms(model_name, pretrained=pretrained)
        self.tokenizer = open_clip.get_tokenizer(model_name)

    def embed(self, text: str):
        text_input = self.tokenizer([text])
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
            return text_features.squeeze().tolist()

    def embed_batch(self, texts: list):
        text_input = self.tokenizer(texts)
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
            return text_features.tolist()
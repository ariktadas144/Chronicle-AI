import open_clip
import torch
from PIL import Image
import os

class ImageEmbedder:
    def __init__(self, model_name='ViT-B-32', pretrained='openai'):
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained)
        self.tokenizer = open_clip.get_tokenizer(model_name)

    def embed(self, image_path: str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        image = self.preprocess(Image.open(image_path)).unsqueeze(0)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            return image_features.squeeze().tolist()

    def embed_batch(self, image_paths: list):
        images = []
        for path in image_paths:
            if os.path.exists(path):
                images.append(self.preprocess(Image.open(path)))
            else:
                raise FileNotFoundError(f"Image file not found: {path}")
        image_input = torch.stack(images)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            return image_features.tolist()

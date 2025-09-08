import os
import numpy as np
import torch
from config import MODEL_PATHS
from typing import List

# --------------------------
# Preprocessing helper
# --------------------------
def preprocess_frame_for_model(frame_bgr, target_size=(224,224), framework="torch"):
    import cv2
    img = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype("float32") / 255.0
    if framework == "torch":
        # shape (C,H,W)
        img = np.transpose(img, (2,0,1))
    return img

# --------------------------
# Load PyTorch model from .pt state_dict
# --------------------------
def load_torch_model(path, arch="xception", device='cpu'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")

    import torch

    # Create model instance depending on architecture
    if arch == "xception" or arch == "ffpp_c23" or arch == "ffpp_c40":
        from xception import xception
        model = xception(pretrained=False)
    elif arch == "mesonet":
        from mesonet import MesoNet
        model = MesoNet()
    else:
        raise ValueError(f"Unknown architecture: {arch}")

    # Load state_dict
    state_dict = torch.load(path, map_location=device)
    # Remove "module." prefix if present
    new_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
    model.load_state_dict(new_state_dict)

    model.to(device)
    model.eval()
    return model

# --------------------------
# DeepfakeDetector class
# --------------------------
class DeepfakeDetector:
    """
    Deepfake detector supporting multiple PyTorch .pt models.
    Pass model_name='xception' / 'ffpp23' / 'ffpp40' / 'mesonet' when initializing.
    """
    def __init__(self, model_name="xception", device="cpu"):
        if model_name not in MODEL_PATHS:
            raise ValueError(f"Unknown model {model_name}. Available: {list(MODEL_PATHS.keys())}")
        self.model_name = model_name
        self.device = device
        self.path = MODEL_PATHS[model_name]
        self.framework = "torch"
        self.model = load_torch_model(self.path, arch=model_name, device=self.device)

    # --------------------------
    # Predict frames
    # --------------------------
    def predict_frames(self, frames: List[np.ndarray]) -> List[float]:
        """
        Predict deepfake scores for a list of BGR frames.
        Returns list of float scores per frame (0..1).
        """
        scores = []
        for f in frames:
            img = preprocess_frame_for_model(f, target_size=(224,224), framework="torch")
            tensor = torch.from_numpy(img).unsqueeze(0).to(self.device).float()
            with torch.no_grad():
                out = self.model(tensor)
                out = out.cpu().numpy()
            if out.ndim == 2 and out.shape[1] > 1:
                prob = float(out[0,1])
            else:
                prob = float(out.squeeze())
            scores.append(prob)
        return scores

    # --------------------------
    # Aggregate scores
    # --------------------------
    def aggregate(self, scores: List[float]) -> dict:
        arr = np.array(scores)
        mean_score = float(np.mean(arr)) if arr.size > 0 else 0.0
        median_score = float(np.median(arr)) if arr.size > 0 else 0.0
        majority_ratio = float((arr > 0.5).sum() / arr.size) if arr.size > 0 else 0.0
        return {"mean": mean_score, "median": median_score, "majority_ratio": majority_ratio}

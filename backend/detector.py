import os
import numpy as np
import torch
import torch.nn as nn
from typing import List

# --------------------------
# Preprocessing helper
# --------------------------
def preprocess_frame_for_model(frame_bgr, target_size=(224,224)):
    """
    Converts BGR frame to RGB, resizes, normalizes, and prepares for PyTorch.
    """
    import cv2
    img = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype("float32") / 255.0
    # shape (C,H,W)
    img = np.transpose(img, (2,0,1))
    return img


# --------------------------
# Load EfficientNet model
# --------------------------
def load_efficientnet(path, device="cpu"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")

    from torchvision.models import efficientnet_b0

    # Base model
    model = efficientnet_b0(weights=None)

    # Replace classifier (we'll adjust based on checkpoint later)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, 2)  # default 2-class

    # Load checkpoint
    state_dict = torch.load(path, map_location=device)

    # Check if mismatch between checkpoint and current classifier
    ckpt_out = state_dict.get("classifier.1.weight", None)
    if ckpt_out is not None:
        if ckpt_out.shape[0] == 1:  # checkpoint trained with 1 output
            model.classifier[1] = nn.Linear(in_features, 1)
        elif ckpt_out.shape[0] == 2:  # checkpoint trained with 2 outputs
            model.classifier[1] = nn.Linear(in_features, 2)

    # Remove DataParallel "module." prefix if present
    new_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

    # Load (ignore mismatch if last layer differs)
    model.load_state_dict(new_state_dict, strict=False)

    model.to(device)
    model.eval()
    return model


# --------------------------
# DeepfakeDetector class
# --------------------------
class DeepfakeDetector:
    """
    Deepfake detector using EfficientNet backbone.
    """
    def __init__(self, model_path, device="cpu"):
        self.device = device
        self.model_path = model_path
        self.model = load_efficientnet(self.model_path, device=self.device)

        # Detect classifier type
        self.num_outputs = self.model.classifier[1].out_features
        print(f"[INFO] Loaded EfficientNet with {self.num_outputs} output(s).")

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
            img = preprocess_frame_for_model(f, target_size=(224,224))
            tensor = torch.from_numpy(img).unsqueeze(0).to(self.device).float()
            with torch.no_grad():
                out = self.model(tensor)

                if self.num_outputs == 2:
                    # Softmax: probability of "fake"
                    prob = torch.softmax(out, dim=1)[0,1].item()
                else:
                    # Sigmoid: direct probability
                    prob = torch.sigmoid(out).item()

            scores.append(prob)
        return scores

    # --------------------------
    # Aggregate scores
    # --------------------------
    def aggregate(self, scores: List[float]) -> dict:
        """
        Aggregate frame-level predictions to video-level metrics.
        """
        arr = np.array(scores)
        mean_score = float(np.mean(arr)) if arr.size > 0 else 0.0
        median_score = float(np.median(arr)) if arr.size > 0 else 0.0
        majority_ratio = float((arr > 0.5).sum() / arr.size) if arr.size > 0 else 0.0
        return {"mean": mean_score, "median": median_score, "majority_ratio": majority_ratio}

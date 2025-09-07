# detector.py
import os
import numpy as np
from config import MODEL_PATHS
from typing import List, Tuple

# Load model depending on available file type. We support Keras, PyTorch, ONNX.
def detect_framework():
    if os.path.exists(MODEL_PATHS["keras"]):
        return "keras", MODEL_PATHS["keras"]
    if os.path.exists(MODEL_PATHS["torch"]):
        return "torch", MODEL_PATHS["torch"]
    if os.path.exists(MODEL_PATHS["onnx"]):
        return "onnx", MODEL_PATHS["onnx"]
    return None, None

# Keras loader
def load_keras_model(path):
    from tensorflow.keras.models import load_model
    model = load_model(path)
    return model

# PyTorch loader
def load_torch_model(path, device='cpu'):
    import torch
    # If the repo provides the model class, you'd import it. We assume a saved scripted or state_dict.
    try:
        model = torch.jit.load(path, map_location=device)
    except Exception:
        # try loading state_dict into a common architecture - user must adapt this
        model = None
    if model is None:
        raise RuntimeError("PyTorch model could not be loaded automatically. Use scripted model or update detector.py.")
    model.eval()
    return model

# ONNX loader
def load_onnx_model(path):
    import onnxruntime as ort
    sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    return sess

# Preprocessing helper — adapt to the model's expected input
def preprocess_frame_for_model(frame_bgr, target_size=(224,224), framework="keras"):
    import cv2
    img = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype("float32") / 255.0
    # expand dims for batch
    if framework == "torch":
        # shape (C,H,W)
        img = np.transpose(img, (2,0,1))
    else:
        # shape (H,W,C)
        pass
    return img

class DeepfakeDetector:
    def __init__(self):
        framework, path = detect_framework()
        if framework is None:
            raise RuntimeError("No model found. Place model.h5, model.pt, or model.onnx into backend/model/")
        self.framework = framework
        self.path = path
        self.model = None
        self.device = "cpu"
        self._load()

    def _load(self):
        if self.framework == "keras":
            self.model = load_keras_model(self.path)
        elif self.framework == "torch":
            self.model = load_torch_model(self.path, device=self.device)
        elif self.framework == "onnx":
            self.model = load_onnx_model(self.path)
        else:
            raise RuntimeError("Unsupported model framework.")

    def predict_frames(self, frames, batch_size=8):
        """
        frames: list of BGR frames (numpy arrays). Returns list of scores (float) per frame.
        Score interpretation: model output probability of 'deepfake' (0..1). 
        You may need to adapt threshold/interpretation to your model.
        """
        scores = []
        if self.framework == "keras":
            # assume model expects (N,H,W,C) normalized to [0,1]
            import numpy as np
            X = []
            for f in frames:
                img = preprocess_frame_for_model(f, target_size=(224,224), framework="keras")
                X.append(img)
            X = np.stack(X, axis=0)
            preds = self.model.predict(X, batch_size=batch_size)
            # preds shape depends on model; handle common shapes
            if preds.ndim == 2 and preds.shape[1] > 1:
                # assume second column is probability of class 1
                probs = preds[:,1]
            else:
                probs = preds.squeeze()
            scores = [float(p) for p in probs]

        elif self.framework == "onnx":
            import numpy as np
            sess = self.model
            input_name = sess.get_inputs()[0].name
            X = []
            for f in frames:
                img = preprocess_frame_for_model(f, target_size=(224,224), framework="keras")
                X.append(img)
            X = np.stack(X, axis=0).astype(np.float32)
            outputs = sess.run(None, {input_name: X})
            preds = outputs[0]
            if preds.ndim == 2 and preds.shape[1] > 1:
                probs = preds[:,1]
            else:
                probs = preds.squeeze()
            scores = [float(p) for p in probs]

        elif self.framework == "torch":
            import torch
            model = self.model
            device = torch.device(self.device)
            all_scores = []
            for f in frames:
                img = preprocess_frame_for_model(f, target_size=(224,224), framework="torch")
                tensor = torch.from_numpy(img).unsqueeze(0).to(device).float()
                with torch.no_grad():
                    out = model(tensor)
                    out = out.cpu().numpy()
                if out.ndim == 2 and out.shape[1] > 1:
                    prob = out[0,1]
                else:
                    prob = out.squeeze()
                all_scores.append(float(prob))
            scores = all_scores
        else:
            raise RuntimeError("Unsupported framework during prediction.")
        return scores

    def aggregate(self, scores):
        import numpy as np
        arr = np.array(scores)
        mean_score = float(np.mean(arr)) if arr.size>0 else 0.0
        median_score = float(np.median(arr)) if arr.size>0 else 0.0
        # majority: count above 0.5
        majority = float((arr > 0.5).sum() / arr.size) if arr.size>0 else 0.0
        return {"mean": mean_score, "median": median_score, "majority_ratio": majority}

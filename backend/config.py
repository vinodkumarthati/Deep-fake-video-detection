# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Put model file in backend/model/ as model.h5 or model.pt or model.onnx
MODEL_PATHS = {
    "keras": os.path.join(MODEL_DIR, "model.h5"),
    "torch": os.path.join(MODEL_DIR, "model.pt"),
    "onnx": os.path.join(MODEL_DIR, "model.onnx"),
}

ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}
SAMPLE_EVERY_N_FRAMES = 15   # lower -> more frames -> heavier compute
MAX_FRAMES = 40              # maximum frames to run inference on (saves time)
THUMBNAIL_SIZE = (256, 256)
os.makedirs(UPLOAD_DIR, exist_ok=True)

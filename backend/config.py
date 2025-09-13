import os

# Absolute path to backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

UPLOAD_DIR = os.path.join(BACKEND_DIR, "uploads")

# Folder containing .pt models
PT_MODELS_DIR = os.path.join(PROJECT_ROOT, "model", "pt_models")
PT_MODELS_DIR = os.path.abspath(PT_MODELS_DIR)

# Define models (only EfficientNet now)
MODEL_PATHS = {
    "efficientnet_ffpp": {
        "path": os.path.join(PT_MODELS_DIR, "efficientnet_ffpp.pt"),  # ✅ matches your file
        "arch": "efficientnet",
    }
}

ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}
SAMPLE_EVERY_N_FRAMES = 15
MAX_FRAMES = 40
BATCH_SIZE = 8
MODEL_NAMES = list(MODEL_PATHS.keys())  # ["efficientnet_ffpp"]

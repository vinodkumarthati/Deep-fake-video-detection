import os

# Absolute path to backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

UPLOAD_DIR = os.path.join(BACKEND_DIR, "uploads")

# Folder containing .pt models
PT_MODELS_DIR = os.path.join(PROJECT_ROOT, "model", "pt_models")
PT_MODELS_DIR = os.path.abspath(PT_MODELS_DIR)  # ensure absolute path

# List of available models (without .pt)
MODEL_NAMES = ["xception", "ffpp_c23", "ffpp_c40"]
MODEL_PATHS = {name: os.path.join(PT_MODELS_DIR, f"{name}.pt") for name in MODEL_NAMES}

ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}
SAMPLE_EVERY_N_FRAMES = 15
MAX_FRAMES = 40

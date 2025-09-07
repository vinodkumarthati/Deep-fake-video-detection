# video_utils.py
import cv2
import os
import base64
from PIL import Image
from io import BytesIO

def allowed_file(filename, allowed_ext):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

def sample_frames(video_path, every_n=15, max_frames=40, resize=(256,256)):
    """
    Sample frames from video_path every `every_n` frames up to max_frames.
    Returns list of frames in BGR (cv2) format.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    frames = []
    idx = 0
    saved = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % every_n == 0:
            if resize:
                frame = cv2.resize(frame, resize)
            frames.append(frame)
            saved += 1
            if saved >= max_frames:
                break
        idx += 1
    cap.release()
    return frames

def bgr_to_rgb_pil(bgr_img):
    import cv2
    from PIL import Image
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def pil_to_base64(pil_img, fmt="PNG"):
    buf = BytesIO()
    pil_img.save(buf, format=fmt)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/{fmt.lower()};base64,{encoded}"

def frame_to_base64_bgr(frame_bgr):
    pil = bgr_to_rgb_pil(frame_bgr)
    # optionally resize here
    return pil_to_base64(pil)

import torch

def convert_pkl_to_pt(pkl_path, pt_path):
    # Load the original checkpoint
    checkpoint = torch.load(pkl_path, map_location='cpu')

    # If checkpoint has a 'state_dict' key, extract it
    state_dict = checkpoint['state_dict'] if isinstance(checkpoint, dict) and 'state_dict' in checkpoint else checkpoint

    # Save directly as .pt (no model instantiation)
    torch.save(state_dict, pt_path)
    print(f"Converted {pkl_path} -> {pt_path}")

if __name__ == "__main__":
    convert_pkl_to_pt("deepfake_c0_xception.pkl", "xception.pt")

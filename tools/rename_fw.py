import os
from pathlib import Path

def rename_fw_files():
    base_dir = Path('../datasets/door')
    img_dir = base_dir / 'images' / 'train'
    lbl_dir = base_dir / 'labels' / 'train'
    
    # Get all FW files
    img_files = sorted([f for f in img_dir.glob('FW*')])
    lbl_files = sorted([f for f in lbl_dir.glob('FW*')])
    
    if len(img_files) != 30 or len(lbl_files) != 30:
        print(f"Warning: Expected 30 files, but found {len(img_files)} images and {len(lbl_files)} labels.")
        # Proceed anyway if they match
        if len(img_files) != len(lbl_files):
             print("Error: Image and label counts do not match!")
             return

    for i, (img_path, lbl_path) in enumerate(zip(img_files, lbl_files), start=31):
        new_name = str(i)
        
        # Rename image
        new_img_path = img_dir / f"{new_name}.jpeg"
        print(f"Renaming {img_path.name} -> {new_img_path.name}")
        img_path.rename(new_img_path)
        
        # Rename label
        new_lbl_path = lbl_dir / f"{new_name}.txt"
        print(f"Renaming {lbl_path.name} -> {new_lbl_path.name}")
        lbl_path.rename(new_lbl_path)
        
    print("Renaming completed successfully.")

if __name__ == "__main__":
    rename_fw_files()

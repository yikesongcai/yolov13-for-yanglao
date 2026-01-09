import os
import shutil
from pathlib import Path

def merge(src_root, dst_root, prefix, new_index):
    """
    src_root: datasets/door or datasets/aircondition
    dst_root: datasets/merged_data
    prefix: 'door' or 'aircondition'
    new_index: 81 or 82
    """
    for split in ['train', 'val']:
        src_img_dir = Path(src_root) / 'images' / split
        src_lbl_dir = Path(src_root) / 'labels' / split
        
        dst_img_dir = Path(dst_root) / 'images' / split
        dst_lbl_dir = Path(dst_root) / 'labels' / split
        
        dst_img_dir.mkdir(parents=True, exist_ok=True)
        dst_lbl_dir.mkdir(parents=True, exist_ok=True)
        
        if not src_img_dir.exists():
            print(f"Warning: {src_img_dir} does not exist. Skipping.")
            continue

        for img_path in src_img_dir.glob('*'):
            suffix = img_path.suffix.lower()
            if suffix not in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
                continue
            
            new_name = f"{prefix}_{img_path.name}"
            dst_img_path = dst_img_dir / new_name
            
            # Copy Image
            shutil.copy2(img_path, dst_img_path)
            
            # Process Label (trying to match the stem)
            lbl_path = src_lbl_dir / (img_path.stem + '.txt')
            if lbl_path.exists():
                dst_lbl_path = dst_lbl_dir / (f"{prefix}_{img_path.stem}.txt")
                with open(lbl_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) > 0:
                        parts[0] = str(new_index)
                        new_lines.append(" ".join(parts) + "\n")
                
                with open(dst_lbl_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
            else:
                print(f"Warning: Label not found for {img_path}")

if __name__ == '__main__':
    base_dir = r'E:\programming\PythonProject\yolov13'
    dst_dir = os.path.join(base_dir, 'datasets', 'merged_data')
    
    # 1. Process Door (Index 81)
    print("Processing Door dataset...")
    merge(os.path.join(base_dir, 'datasets', 'door'), dst_dir, 'door', 81)
    
    # 2. Process Aircondition (Index 82)
    print("Processing Aircondition dataset...")
    merge(os.path.join(base_dir, 'datasets', 'aircondition'), dst_dir, 'aircondition', 82)
    
    print(f"Successfully merged datasets into {dst_dir}")

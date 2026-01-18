import os
import shutil
import random

def merge_dataset(src_dir, dest_dir, mapping, train_ratio=0.8, is_split=False, prefix=None):
    """
    src_dir: path to the dataset to merge
    dest_dir: path to the merged_data directory (root)
    mapping: dict of {old_idx: new_idx}
    is_split: True if src_dir already has train/val/test structure
    prefix: prefix for destination filenames (if None, uses src_dir name)
    """
    img_dest_train = os.path.join(dest_dir, 'images', 'train')
    lbl_dest_train = os.path.join(dest_dir, 'labels', 'train')
    img_dest_val = os.path.join(dest_dir, 'images', 'val')
    lbl_dest_val = os.path.join(dest_dir, 'labels', 'val')

    os.makedirs(img_dest_train, exist_ok=True)
    os.makedirs(lbl_dest_train, exist_ok=True)
    os.makedirs(img_dest_val, exist_ok=True)
    os.makedirs(lbl_dest_val, exist_ok=True)

    file_prefix = prefix if prefix else os.path.basename(src_dir)

    if is_split:
        # Roboflow style or split style
        splits = ['train', 'valid', 'test']
        for split in splits:
            src_img_dir = os.path.join(src_dir, split, 'images')
            src_lbl_dir = os.path.join(src_dir, split, 'labels')
            
            # Map valid/test to val in our destination
            target_split = 'train' if split == 'train' else 'val'
            target_img_dir = img_dest_train if target_split == 'train' else img_dest_val
            target_lbl_dir = lbl_dest_train if target_split == 'train' else lbl_dest_val

            if not os.path.exists(src_img_dir): continue
            
            for img_file in os.listdir(src_img_dir):
                if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')): continue
                
                name_base = os.path.splitext(img_file)[0]
                lbl_file = name_base + '.txt'
                src_img_path = os.path.join(src_img_dir, img_file)
                src_lbl_path = os.path.join(src_lbl_dir, lbl_file)
                
                if os.path.exists(src_lbl_path):
                    # Process label
                    with open(src_lbl_path, 'r') as f:
                        lines = f.readlines()
                    
                    new_lines = []
                    valid_obj = False
                    for line in lines:
                        parts = line.split()
                        if not parts: continue
                        cls = int(parts[0])
                        if cls in mapping:
                            parts[0] = str(mapping[cls])
                            new_lines.append(" ".join(parts) + "\n")
                            valid_obj = True
                    
                    if valid_obj:
                        # Copy image
                        new_base = img_file
                        if file_prefix and not img_file.startswith(file_prefix):
                            new_base = file_prefix + "_" + img_file
                        
                        # Fix cleaning_agent -> clean_agent
                        new_base = new_base.replace("cleaning_agent", "clean_agent")
                        
                        dest_img_path = os.path.join(target_img_dir, new_base)
                        shutil.copy(src_img_path, dest_img_path)
                        
                        # Write new label
                        new_lbl_base = lbl_file.replace("cleaning_agent", "clean_agent")
                        if file_prefix and not lbl_file.startswith(file_prefix):
                            new_lbl_base = file_prefix + "_" + new_lbl_base
                            
                        dest_lbl_path = os.path.join(target_lbl_dir, new_lbl_base)
                        with open(dest_lbl_path, 'w') as f:
                            f.writelines(new_lines)
                    else:
                        print(f"  Warning: No valid objects with mapping {mapping} found in {src_lbl_path}")
    else:
        # Flat structure
        src_img_dir = os.path.join(src_dir, 'images')
        src_lbl_dir = os.path.join(src_dir, 'labels')
        
        if not os.path.exists(src_img_dir): return

        all_imgs = [f for f in os.listdir(src_img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(all_imgs)
        
        split_idx = int(len(all_imgs) * train_ratio)
        train_imgs = all_imgs[:split_idx]
        val_imgs = all_imgs[split_idx:]

        for img_list, target_img_dir, target_lbl_dir in [(train_imgs, img_dest_train, lbl_dest_train), (val_imgs, img_dest_val, lbl_dest_val)]:
            for img_file in img_list:
                name_base = os.path.splitext(img_file)[0]
                lbl_file = name_base + '.txt'
                src_img_path = os.path.join(src_img_dir, img_file)
                src_lbl_path = os.path.join(src_lbl_dir, lbl_file)
                
                if os.path.exists(src_lbl_path):
                    with open(src_lbl_path, 'r') as f:
                        lines = f.readlines()
                    
                    new_lines = []
                    valid_obj = False
                    for line in lines:
                        parts = line.split()
                        if not parts: continue
                        cls = int(parts[0])
                        if cls in mapping:
                            parts[0] = str(mapping[cls])
                            new_lines.append(" ".join(parts) + "\n")
                            valid_obj = True
                    
                    if valid_obj:
                        # Copy image
                        new_base = img_file
                        if file_prefix and not img_file.startswith(file_prefix):
                            new_base = file_prefix + "_" + img_file
                        
                        # Fix cleaning_agent -> clean_agent
                        new_base = new_base.replace("cleaning_agent", "clean_agent")
                            
                        dest_img_path = os.path.join(target_img_dir, new_base)
                        shutil.copy(src_img_path, dest_img_path)
                        
                        # Write new label
                        new_lbl_base = lbl_file.replace("cleaning_agent", "clean_agent")
                        if file_prefix and not lbl_file.startswith(file_prefix):
                            new_lbl_base = file_prefix + "_" + new_lbl_base
                                
                        dest_lbl_path = os.path.join(target_lbl_dir, new_lbl_base)
                        with open(dest_lbl_path, 'w') as f:
                            f.writelines(new_lines)
                    else:
                        print(f"  Warning: No valid objects with mapping {mapping} found in {src_lbl_path}")

if __name__ == "__main__":
    DATASETS_ROOT = r'E:\programming\PythonProject\yolov13\datasets'
    MERGED_ROOT = os.path.join(DATASETS_ROOT, 'merged_data')
    
    # 1. Glucometer: 0 -> 2
    print("Merging Glucometer...")
    merge_dataset(os.path.join(DATASETS_ROOT, 'Glucometer'), MERGED_ROOT, {0: 2}, is_split=True, prefix="glucometer")
    
    # 2. 剪刀标注: 11 -> 3
    print("Merging Scissors...")
    merge_dataset(os.path.join(DATASETS_ROOT, '剪刀标注'), MERGED_ROOT, {11: 3}, is_split=False, prefix="scissors")
    
    # 3. 指甲钳标注: 12 -> 4
    print("Merging Nail Clipper...")
    merge_dataset(os.path.join(DATASETS_ROOT, '指甲钳标注'), MERGED_ROOT, {12: 4}, is_split=False, prefix="nail_clipper")
    
    # 4. bucket&clean_agent: 9 -> 5, 10 -> 6
    # We use explicit prefixes based on the object
    # Since my merge_dataset copies the whole image, we'll just use a generic prefix "bucket_cleanup" for this folder
    # but the user wants "bucket" and "clean_agent". 
    # Actually, the user's files are already named bucket_x or cleaning_agent_x.
    # So if we use prefix="" or a logic to skip if exists, it's better.
    print("Merging Bucket & Clean Agent...")
    merge_dataset(os.path.join(DATASETS_ROOT, 'bucket&clean_agent'), MERGED_ROOT, {9: 5, 10: 6}, is_split=True, prefix="")
    
    print("Merge complete!")

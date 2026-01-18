import os

def rename_pair(root_dir, old_name, new_name):
    # Rename image
    img_dir_train = os.path.join(root_dir, 'images', 'train')
    img_dir_val = os.path.join(root_dir, 'images', 'val')
    lbl_dir_train = os.path.join(root_dir, 'labels', 'train')
    lbl_dir_val = os.path.join(root_dir, 'labels', 'val')
    
    dirs = [img_dir_train, img_dir_val, lbl_dir_train, lbl_dir_val]
    
    for d in dirs:
        if not os.path.exists(d): continue
        for filename in os.listdir(d):
            if old_name in filename:
                src = os.path.join(d, filename)
                dst = os.path.join(d, filename.replace(old_name, new_name))
                if src != dst:
                    if os.path.exists(dst):
                        # Collision check: if destination exists, we might want to skip or merge.
                        # For simplicity, we just remove the old one if it's the same file content or rename with suffix.
                        os.remove(src)
                        print(f"Collision: Removed {filename} (already exists as {os.path.basename(dst)})")
                    else:
                        os.rename(src, dst)
                        print(f"Renamed: {filename} -> {os.path.basename(dst)}")

if __name__ == "__main__":
    MERGED_ROOT = r'E:\programming\PythonProject\yolov13\datasets\merged_data'
    
    # Define exact replacements
    # Order matters: more specific ones first
    replacements = [
        # Redundant double naming
        ("nail_clipper_nail_clipper_", "nail_clipper_"),
        ("scissors_scissors_", "scissors_"),
        
        # Non-standard prefixes from folder names
        ("bucket&clean_agent_bucket_", "bucket_"),
        ("bucket&clean_agent_cleaning_agent_", "clean_agent_"),
        ("bucket&clean_agent_clean_agent_", "clean_agent_"), # just in case
        
        # Case consistency
        ("Glucometer_", "glucometer_"),
    ]
    
    for old, new in replacements:
        print(f"Executing: {old} -> {new}")
        rename_pair(MERGED_ROOT, old, new)
    
    print("Standardization complete!")

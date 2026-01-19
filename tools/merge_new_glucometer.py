import os
import shutil

def process_glucometer_merge(src_root, dest_root):
    # Glucometer prefix as standard
    prefix = "glucometer"
    
    # We only care about files with 'glucometer' in the name in the datasets/ root
    for split in ['train', 'val']:
        src_img_dir = os.path.join(src_root, 'images', split)
        src_lbl_dir = os.path.join(src_root, 'labels', split)
        
        dest_img_dir = os.path.join(dest_root, 'images', split)
        dest_lbl_dir = os.path.join(dest_root, 'labels', split)
        
        if not os.path.exists(src_img_dir): continue
        
        files = [f for f in os.listdir(src_img_dir) if 'glucometer' in f.lower() and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Processing {len(files)} new glucometer files in {split}")
        
        for img_file in files:
            name_base = os.path.splitext(img_file)[0]
            lbl_file = name_base + '.txt'
            
            src_img_path = os.path.join(src_img_dir, img_file)
            src_lbl_path = os.path.join(src_lbl_dir, lbl_file)
            
            if os.path.exists(src_lbl_path):
                # 1. Read and Re-index (0 -> 2)
                with open(src_lbl_path, 'r') as f:
                    lines = f.readlines()
                
                new_lines = []
                for line in lines:
                    parts = line.split()
                    if not parts: continue
                    cls = int(parts[0])
                    if cls == 0:
                        parts[0] = '2'
                        new_lines.append(" ".join(parts) + "\n")
                    else:
                        new_lines.append(line)
                
                # 2. Determine target filename (ensure no double prefix)
                target_name = img_file
                if not img_file.lower().startswith(prefix):
                    target_name = f"{prefix}_{img_file}"
                
                target_lbl_name = os.path.splitext(target_name)[0] + ".txt"
                
                # 3. Copy and Write
                shutil.copy(src_img_path, os.path.join(dest_img_dir, target_name))
                with open(os.path.join(dest_lbl_dir, target_lbl_name), 'w') as f:
                    f.writelines(new_lines)

if __name__ == "__main__":
    DATASETS_ROOT = r'E:\programming\PythonProject\yolov13\datasets'
    MERGED_ROOT = os.path.join(DATASETS_ROOT, 'merged_data')
    process_glucometer_merge(DATASETS_ROOT, MERGED_ROOT)
    print("Done!")

import os

def reindex_in_place(label_dir, prefix, old_idx, new_idx):
    if not os.path.exists(label_dir):
        print(f"Directory not found: {label_dir}")
        return

    count = 0
    for filename in os.listdir(label_dir):
        if filename.startswith(prefix) and filename.endswith('.txt'):
            filepath = os.path.join(label_dir, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            modified = False
            for line in lines:
                parts = line.split()
                if not parts:
                    new_lines.append(line)
                    continue
                
                if int(parts[0]) == old_idx:
                    parts[0] = str(new_idx)
                    new_lines.append(" ".join(parts) + "\n")
                    modified = True
                else:
                    new_lines.append(line)
            
            if modified:
                with open(filepath, 'w') as f:
                    f.writelines(new_lines)
                count += 1
                
    print(f"Modified {count} files in {label_dir}")

if __name__ == "__main__":
    LBL_TRAIN = r'E:\programming\PythonProject\yolov13\datasets\labels\train'
    reindex_in_place(LBL_TRAIN, "glucometer", 0, 2)

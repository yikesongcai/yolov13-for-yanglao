import os

def create_classes_txt(target_dir, nc, names_dict):
    classes_path = os.path.join(target_dir, 'classes.txt')
    with open(classes_path, 'w', encoding='utf-8') as f:
        for i in range(nc):
            name = names_dict.get(i, f'class_{i}')
            f.write(f"{name}\n")
    print(f"Created {classes_path}")

if __name__ == '__main__':
    base_path = r'E:\programming\PythonProject\yolov13\datasets\merged_data\labels'
    nc = 83
    names = {81: 'door', 82: 'aircondition'}
    
    for split in ['train', 'val']:
        target_dir = os.path.join(base_path, split)
        if os.path.exists(target_dir):
            create_classes_txt(target_dir, nc, names)

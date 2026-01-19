import os
import sys

# Add the project root to sys.path to allow importing the local 'ultralytics' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ultralytics import YOLO

def auto_label_person(datasets_root, model_path='yolov13n.pt', target_idx=7, conf=0.5):
    """
    datasets_root: path to datasets folder (contains images/train, labels/train etc.)
    model_path: path to pre-trained model (COCO)
    target_idx: the index for 'person' in our new schema
    conf: confidence threshold for detection
    """
    model = YOLO(model_path)
    
    # Exclude these prefixes as requested
    exclude_prefixes = ['bucket_', 'clean_agent_']
    
    for split in ['train', 'val']:
        img_dir = os.path.join(datasets_root, 'images', split)
        lbl_dir = os.path.join(datasets_root, 'labels', split)
        
        if not os.path.exists(img_dir):
            print(f"Directory not found: {img_dir}")
            continue
            
        img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Processing {len(img_files)} images in {split}...")
        
        count = 0
        labeled_count = 0
        for img_file in img_files:
            # Check exclusions
            exclude = False
            for p in exclude_prefixes:
                if img_file.lower().startswith(p):
                    exclude = True
                    break
            if exclude:
                continue
            
            img_path = os.path.join(img_dir, img_file)
            results = model.predict(img_path, conf=conf, verbose=False)
            
            person_boxes = []
            for result in results:
                # result.boxes.cls is the class index
                # COCO class 0 is person
                for i, c in enumerate(result.boxes.cls):
                    if int(c) == 0:
                        # Get bbox in YOLO format (normalized xywh)
                        # xywhn returns normalized center x, y, width, height
                        box = result.boxes.xywhn[i].tolist()
                        person_boxes.append(box)
            
            if person_boxes:
                # Map to labels file
                name_base = os.path.splitext(img_file)[0]
                lbl_path = os.path.join(lbl_dir, name_base + '.txt')
                
                # Create directory for label if it doesn't exist (though it should)
                os.makedirs(os.path.dirname(lbl_path), exist_ok=True)
                
                # Append to file
                with open(lbl_path, 'a') as f:
                    for box in person_boxes:
                        # box is [x, y, w, h]
                        line = f"{target_idx} {' '.join(f'{val:.6f}' for val in box)}\n"
                        f.write(line)
                labeled_count += 1
            
            count += 1
            if count % 100 == 0:
                print(f"  Processed {count}/{len(img_files)} images...")

        print(f"Finished {split}: Added 'person' labels to {labeled_count} files.")

if __name__ == "__main__":
    DATASETS_ROOT = r'E:\programming\PythonProject\yolov13\datasets'
    # Use yolov13n.pt for automated labeling
    auto_label_person(DATASETS_ROOT, model_path='yolov13n.pt', target_idx=7, conf=0.5)

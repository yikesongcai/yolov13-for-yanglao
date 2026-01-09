from ultralytics import YOLO
import os
import sys

def batch_predict(model_path, source_path, save_dir='E:\programming\PythonProject\yolov13\\runs\predict'):
    # 1. 加载模型
    model = YOLO(model_path)

    # 2. 进行预测
    # source 可以是文件夹路径
    results = model.predict(
        source=source_path, 
        conf=0.25, 
        save=True, 
        project=save_dir, 
        name='test',
        exist_ok=True
    )

    print(f"Prediction completed. Results are saved in {os.path.join(save_dir, 'test')}")

if __name__ == '__main__':
    model_weight = 'E:\programming\PythonProject\yolov13\yolov13n.pt'
    # 用户提供的路径
    test_dir = r"E:\programming\PythonProject\yolov13\datasets\for testing"
    
    if os.path.exists(test_dir):
        batch_predict(model_weight, test_dir)
    else:
        print(f"Error: Directory not found: {test_dir}")

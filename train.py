from ultralytics import YOLO

def main():
    # 1. 加载模型
    # 推荐使用 'yolov8n.pt' 或 'yolov10n.pt' 作为预训练权重（Transfer Learning）
    # 如果你的 yolov13 是自定义库，请替换为对应的类
    model = YOLO('tmp/yolov13n.pt')

    # 2. 训练模型
    results = model.train(
        data='data.yaml',   # 指向刚才创建的配置文件
        epochs=100,         # 训练轮数，通常 50-300 之间
        imgsz=640,          # 图片大小，必须是 32 的倍数
        batch=16,           # 显存不够就调小，如 8 或 4
        device=0,           # 使用 GPU 0，如果是 CPU 则填 'cpu'
        workers=4,          # 数据加载线程数
        name='my_yolo_exp'  # 实验名称，结果会保存在 runs/detect/my_yolo_exp
    )

if __name__ == '__main__':
    main()
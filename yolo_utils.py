from ultralytics import YOLO


model = YOLO("content/runs/detect/train/weights/best.pt")

def detect_image(image_path):
    
    results = model(image_path, save=True) 

    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb

def detect_video(video_path):
    results = model(video_path, save=True)

    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb
        
    


detect_image("test_data/test_img2.jpg")
detect_image("test_data/test_img3.jpeg")
detect_image("test_data/test_img4.jpg")

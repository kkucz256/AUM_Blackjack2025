from ultralytics import YOLO

model = YOLO("yolov8n.pt")  

# results = model("image.png") 

# # Process results list
# for result in results:
#     boxes = result.boxes  # 
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen
#     result.save(filename="result.png")  
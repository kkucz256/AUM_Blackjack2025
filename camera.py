from ultralytics import YOLO
import cv2
import time
import os

model = YOLO("content/best_11_04.pt")

last_seen_cards = set()
detected_time = None
screenshot_taken = False

output_folder = "screenshots"
os.makedirs(output_folder, exist_ok=True)

def detect_realtime():
    global last_seen_cards, detected_time, screenshot_taken


    cap = cv2.VideoCapture(0)


    if not cap.isOpened():
        print("Nie udało się otworzyć kamery")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Błąd podczas odczytu klatki")
            break

        results = model(frame)

        for result in results:
            annotated_frame = result.plot()

            height, width = annotated_frame.shape[:2]
            line_y = height // 2
            cv2.line(annotated_frame, (0, line_y), (width, line_y), (0, 0, 255), thickness=2)

            current_cards = set()
            boxes = result.boxes

            if boxes is not None and boxes.cls.numel() > 0:
                for cls_id in boxes.cls:
                    class_name = model.names[int(cls_id)]
                    current_cards.add(class_name)

            if current_cards and current_cards != last_seen_cards:
                last_seen_cards = current_cards
                detected_time = time.time()
                screenshot_taken = False
                print(f"\nNew cards detected: {current_cards}")

            if detected_time and not screenshot_taken:
                if time.time() - detected_time >= 2:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"{'_'.join(sorted(current_cards))}_{timestamp}.jpg"
                    filepath = os.path.join(output_folder, filename)
                    cv2.imwrite(filepath, annotated_frame)
                    screenshot_taken = True
                    print(f"📸 Screenshot saved as: {filepath}")

            cv2.imshow("YOLO Real-Time Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_realtime()
from ultralytics import YOLO
import cv2

model = YOLO("content/runs/detect/train/weights/best.pt")

def detect_realtime():
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

            cv2.imshow("YOLO Real-Time Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_realtime()

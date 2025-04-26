import cv2
import numpy as np

# Start camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 2: Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 3: Edge detection
    edged = cv2.Canny(blurred, 50, 150)

    # Step 4: Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        # If the polygon has 4 points, it could be a rectangle (paper)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            # Get bounding box
            x, y, w, h = cv2.boundingRect(approx)

            # Filter by size if needed (optional)
            if w > 100 and h > 100:  # adjust thresholds as needed
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display result
    cv2.imshow("Paper Detection", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

from ultralytics import YOLO
import cv2
import time
import os
import re
from collections import Counter

model = YOLO("content/best_12_04.pt")

last_seen_cards = set()
detected_time = None
log_entries = []
log_file = "detected_cards_log.txt"

player_deck = []
dealer_deck = []
player_seen = set()
dealer_seen = set()
new_cards_detected = False

detection_buffer = []
detection_start_time = None
MAX_BUFFER_SIZE = 90
CONFIRMATION_THRESHOLD = 0.9
LAST_SAVE_TIME = 0
SAVE_INTERVAL = 2

card_owner = {} 

class CardInfo:
    def __init__(self, raw_name, y_center, line_y):
        self.value = raw_name.lower() 
        self.rank = re.sub(r'[hdsc]', '', self.value)  
        self.suit = re.sub(r'[^hdsc]', '', self.value) 
        self.is_dealer = y_center < line_y

    def __hash__(self):
        return hash((self.value, self.is_dealer))

    def __eq__(self, other):
        return self.value == other.value and self.is_dealer == other.is_dealer

    def __repr__(self):
        return f"{self.value.upper()} - {'Dealer' if self.is_dealer else 'Player'}"

class CardsDetected:
    def __init__(self, boxes, class_names, line_y):
        self.cards_info = []
        if boxes is not None and boxes.cls.numel() > 0:
            for i, cls_id in enumerate(boxes.cls):
                raw_name = class_names[int(cls_id)]
                box = boxes.xyxy[i]
                y_center = (box[1] + box[3]) / 2
                card = CardInfo(raw_name, y_center, line_y)
                self.cards_info.append(card)

    def get_detected_cards(self):
        return set(self.cards_info)

    def __repr__(self):
        return "\n".join(str(card) for card in self.cards_info)

    def to_log_string(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        lines = [f"[{timestamp}]"]
        for card in self.cards_info:
            lines.append(f"{card.value.upper()} - {'Dealer' if card.is_dealer else 'Player'}")
        return "\n".join(lines) + "\n\n"

def detect_realtime():
    global last_seen_cards, detected_time, new_cards_detected, LAST_SAVE_TIME, SAVE_INTERVAL
    global detection_buffer, detection_start_time, player_deck, dealer_deck, card_owner


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
            cv2.line(annotated_frame, (0, line_y), (width, line_y), (0, 0, 0), thickness=2)

            boxes = result.boxes
            detected = CardsDetected(boxes, model.names, line_y)
            current_cards = detected.get_detected_cards()

            if current_cards and current_cards != last_seen_cards:
                last_seen_cards = current_cards
                detected_time = time.time()
                log_entries.append(detected.to_log_string())
                print(f"\nNew cards detected:\n{detected}")

                if not detection_buffer:
                    detection_start_time = time.time()

                if len(detection_buffer) >= MAX_BUFFER_SIZE:
                    detection_buffer.pop(0)

                detection_buffer.append(current_cards)

            if detection_buffer and (time.time() - detection_start_time) < 3:
                if len(detection_buffer) >= MAX_BUFFER_SIZE:
                    detection_buffer.pop(0)
                detection_buffer.append(current_cards)

            if detection_buffer and (time.time() - detection_start_time) >= 3:
                all_cards = [card for frame in detection_buffer for card in frame]
                card_counts = Counter([card.value for card in all_cards])

                frame_count = len(detection_buffer)
                confirmed_card_values = {val for val, count in card_counts.items() if count >= int(frame_count * CONFIRMATION_THRESHOLD)}
                confirmed_cards = set()

                for frame_cards in detection_buffer:
                    for card in frame_cards:
                        if card.value in confirmed_card_values:
                            confirmed_cards.add(card)

                if confirmed_cards:
                    log_entries.append(f"Confirmed cards: {', '.join([card.value.upper() for card in confirmed_cards])}\n")

                    for card in confirmed_cards:
                        if card.value not in card_owner:
                            card_owner[card.value] = card.is_dealer

                        is_dealer_card = card_owner[card.value]

                        if is_dealer_card:
                            if card.value not in dealer_seen:
                                dealer_deck.append(card.value)
                                dealer_seen.add(card.value)
                                new_cards_detected = True
                                print(f"Added {card.value.upper()} to Dealer deck (locked to Dealer)")
                        else:
                            if card.value not in player_seen:
                                player_deck.append(card.value)
                                player_seen.add(card.value)
                                new_cards_detected = True
                                print(f"Added {card.value.upper()} to Player deck (locked to Player)")

                detection_buffer.clear()
                detection_start_time = None
                
            cv2.imshow("YOLO Real-Time Detection", annotated_frame)

        current_time = time.time()
        if new_cards_detected and (current_time - LAST_SAVE_TIME) >= SAVE_INTERVAL:
            with open("final_decks.txt", "w") as f:
                f.write(f"D:{', '.join(dealer_deck)}\n")
                f.write(f"P:{', '.join(player_deck)}\n")
            LAST_SAVE_TIME = current_time
            print("Decks updated in 'final_decks.txt'")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if log_entries:
        with open(log_file, "w") as f:
            f.writelines(log_entries)
        print(f"\nLog file saved with {len(log_entries)} entries at: {log_file}")

    print(f"\nFinal Dealer Deck: {dealer_deck}")
    print(f"Final Player Deck: {player_deck}")

    with open("final_decks.txt", "w") as f:
        f.write("")

detect_realtime()

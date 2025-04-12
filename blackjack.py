import time

cards = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def hand_value(hand):
    value = sum(cards.get(card.upper(), 0) for card in hand)
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(name, hand):
    print(f"{name}'s Hand: {hand} -> {hand_value(hand)}")

def read_hands_from_file():
    try:
        with open("final_decks.txt", "r") as f:
            lines = f.readlines()
            dealer_line = next((line for line in lines if line.startswith("D:")), "D:").strip()
            player_line = next((line for line in lines if line.startswith("P:")), "P:").strip()
            dealer_hand = dealer_line[2:].replace(" ", "").split(",") if dealer_line[2:] else []
            player_hand = player_line[2:].replace(" ", "").split(",") if player_line[2:] else []
            return dealer_hand, player_hand
    except FileNotFoundError:
        print("Waiting for final_decks.txt to appear...")
        return [], []

def blackjack_ai():
    print("=== AI Blackjack ===")
    print("Waiting for player and dealer hands...")

    # Wait for valid hands (loop until at least 2 cards per hand)
    while True:
        dealer_hand, player_hand = read_hands_from_file()
        if len(player_hand) >= 2 and len(dealer_hand) >= 1:
            break
        time.sleep(1)

    display_hand("Dealer", dealer_hand)
    display_hand("Player", player_hand)

    # AI plays as the player
    while hand_value(player_hand) < 17 and len(player_hand) < 5:
        print("🧠 AI chooses to hit.")
        time.sleep(1)
        _, player_hand = read_hands_from_file()
        display_hand("Player", player_hand)

    if hand_value(player_hand) > 21:
        print("AI busts! Dealer wins.")
        return
    elif len(player_hand) == 5:
        print("🎉 AI got 5 cards without busting! AI wins (5-Card Charlie)!")
        return
    else:
        print("🛑 AI stands.")

    # Wait for dealer to draw
    print("Waiting for dealer to finish...")
    while True:
        new_dealer_hand, _ = read_hands_from_file()
        if len(new_dealer_hand) > len(dealer_hand):
            dealer_hand = new_dealer_hand
            display_hand("Dealer", dealer_hand)
        elif hand_value(dealer_hand) >= 17:
            break
        time.sleep(1)

    dealer_score = hand_value(dealer_hand)
    player_score = hand_value(player_hand)

    # Outcome
    if dealer_score > 21:
        print("Dealer busts! AI wins.")
    elif dealer_score > player_score:
        print("Dealer wins.")
    elif dealer_score < player_score:
        print("AI wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    blackjack_ai()


import time

cards = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

dealer_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']

strategy_table = {
    "hard": {
        5:  ['H'] * 10, 6:  ['H'] * 10, 7:  ['H'] * 10, 8:  ['H'] * 10,
        9:  ['H'] * 10,
        10: ['H'] * 10,
        11: ['H'] * 10,
        12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        17: ['S'] * 10, 18: ['S'] * 10, 19: ['S'] * 10, 20: ['S'] * 10, 21: ['S'] * 10,
    },
    "soft": {
        17: ['H'] * 10,
        18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H'],
        19: ['S'] * 10,
        20: ['S'] * 10,
    }
}

def extract_rank(card_with_suit):
    return ''.join(filter(str.isdigit, card_with_suit)) or card_with_suit[0].upper()

def hand_value(hand):
    value = sum(cards.get(card.upper(), 0) for card in hand)
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def is_soft(hand):
    return 'A' in hand and hand_value(hand) <= 21

def get_ai_decision(player_hand, dealer_upcard):
    total = hand_value(player_hand)
    soft = is_soft(player_hand)
    col = dealer_cards.index(dealer_upcard)

    if soft and total in strategy_table["soft"]:
        return strategy_table["soft"][total][col]
    elif not soft and total in strategy_table["hard"]:
        return strategy_table["hard"][total][col]
    elif total <= 11:
        return 'H'
    else:
        return 'S'

def display_hand(name, hand):
    print(f"{name}'s Hand: {hand} -> {hand_value(hand)}")

def read_hands_from_file():
    try:
        with open("final_decks.txt", "r") as f:
            lines = f.readlines()
            dealer_line = next((line for line in lines if line.startswith("D:")), "D:").strip()
            player_line = next((line for line in lines if line.startswith("P:")), "P:").strip()
            dealer_hand_full = dealer_line[2:].replace(" ", "").split(",") if dealer_line[2:] else []
            player_hand_full = player_line[2:].replace(" ", "").split(",") if player_line[2:] else []

            dealer_hand = [extract_rank(card) for card in dealer_hand_full if card]
            player_hand = [extract_rank(card) for card in player_hand_full if card]
            return dealer_hand, player_hand
    except FileNotFoundError:
        print("Waiting for final_decks.txt to appear...")
        return [], []

def blackjack_ai():
    print("=== AI Blackjack ===")
    print("Waiting for player and dealer hands...")

    while True:
        dealer_hand, player_hand = read_hands_from_file()
        if len(player_hand) >= 2 and len(dealer_hand) >= 1:
            break
        time.sleep(1)

    display_hand("Dealer", dealer_hand)
    display_hand("Player", player_hand)

    while len(player_hand) < 5:
        dealer_upcard = dealer_hand[0]
        decision = get_ai_decision(player_hand, dealer_upcard)
        if decision == 'H':
            print("Player chooses to hit.")
            time.sleep(1)
            _, player_hand = read_hands_from_file()
            display_hand("Player", player_hand)
            if hand_value(player_hand) > 21:
                break
        else:
            print("Player stands.")
            break

    if hand_value(player_hand) > 21:
        print("Player busts! Dealer wins.")
        return
    elif len(player_hand) == 5:
        print("Player got 5 cards without busting! AI wins (5-Card Charlie)!")
        return

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

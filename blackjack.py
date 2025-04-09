import random

cards = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
deck = list(cards.keys()) * 4

def draw_card():
    return random.choice(deck)

def hand_value(hand):
    value = sum(cards[card] for card in hand)
    aces = hand.count('A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(name, hand, hide_first=False):
    if hide_first:
        print(f"{name}'s Hand: ['?', '{hand[1]}']")
    else:
        print(f"{name}'s Hand: {hand} -> {hand_value(hand)}")

def blackjack():
    print("=== Welcome to Blackjack ===")
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]

    # Initial hands
    display_hand("Dealer", dealer_hand, hide_first=True)
    display_hand("Player", player_hand)

    # Player's turn
    while hand_value(player_hand) < 21:
        if len(player_hand) == 5:
            print("🎉 Player drew 5 cards without busting! Player wins (5-Card Charlie)!")
            return
        move = input("Hit or Stand? (h/s): ").lower()
        if move == 'h':
            player_hand.append(draw_card())
            display_hand("Player", player_hand)
        elif move == 's':
            break
        else:
            print("Invalid input, type 'h' or 's'.")

    player_score = hand_value(player_hand)
    if player_score > 21:
        print("Player busts! Dealer wins.")
        return

    if len(player_hand) == 5:
        print("🎉 Player drew 5 cards without busting! Player wins (5-Card Charlie)!")
        return

    # Dealer's turn
    display_hand("Dealer", dealer_hand)
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(draw_card())
        display_hand("Dealer", dealer_hand)

    dealer_score = hand_value(dealer_hand)

    if dealer_score > 21:
        print("Dealer busts! Player wins.")
    elif dealer_score > player_score:
        print("Dealer wins.")
    elif dealer_score < player_score:
        print("Player wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    blackjack()

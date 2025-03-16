


def dealCardToPlayer(playerCards, deck):
    playerCards.append(deck.deck[0])
    deck.deck.pop(0)
    return playerCards, deck

def dealCardToDealer(dealerCards, deck):
    dealerCards.append(deck.deck[0])
    deck.deck.pop(0)
    return dealerCards, deck
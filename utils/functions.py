


def dealCardToPlayer(playerCards, deck):
    playerCards.append(deck.deck[0])
    deck.deck.pop()
    return playerCards, deck

def dealCardToDealer(dealerCards, deck):
    dealerCards.append(deck.deck[0])
    deck.deck.pop()
    return dealerCards, deck
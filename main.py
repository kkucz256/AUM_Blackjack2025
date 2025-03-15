from Cards import CARDS
from Deck import Deck
from Player import Player
from utils import dealCardToPlayer, dealCardToDealer

def main():
    deck1 = Deck()
    deck1.shuffleDeck()
    
    player = Player()
    print(deck1.deck)
    playerHand, newDeck=dealCardToPlayer(player.hand, deck1)
    print(playerHand)
    print(newDeck.deck)
    
    # dealCardToDealer()
 
if __name__ == "__main__":
    main()
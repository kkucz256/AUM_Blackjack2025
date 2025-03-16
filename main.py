from Cards import CARDS
from Deck import Deck
from Player import Player
from utils import dealCardToPlayer, dealCardToDealer

def main():
    deck1 = Deck()
    deck1.shuffleDeck()

    player = Player()
    dealer = Player()
    print(f"Initial deck:\n{deck1.deck}\n")
    playerHand, newDeck=dealCardToPlayer(player.hand, deck1)
    dealerHand, newDeck=dealCardToDealer(dealer.hand, newDeck)
    playerHand, newDeck=dealCardToPlayer(player.hand, newDeck)
    
    print(f"Deck after initial dealing:\n{newDeck.deck}\n")
    print(f"Player's hand:\n{playerHand}\n")
    print(f"Dealer's hand:\n{dealerHand}")
    
        
    # player = Player()
    # player.hand = [('ACE', (1, 11)), ('KING', 10)]
    # print(player.totalHandValue())

    # player.hand = [('ACE', (1, 11)), ('NINE', 9)]
    # print(player.totalHandValue())

    # player.hand = [('ACE', (1, 11)), ('NINE', 9), ('TWO', 2)]
    # print(player.totalHandValue())

    # player.hand = [('ACE', (1, 11)), ('ACE', (1, 11)), ('NINE', 9)]
    # print(player.totalHandValue())
    
    # player.hand = [('ACE', (1, 11)) for i in range(0,11)]
    # print(player.totalHandValue())
    
    

 
if __name__ == "__main__":
    main()
from blackjack import Blackjack


def main():
    hit = True
    
    blackjack = Blackjack()
    blackjack.shuffleCards()
    print(blackjack.deck)
    blackjack.dealCardToPlayer()
    blackjack.dealCardToDealer()
    blackjack.dealCardToPlayer()
    # print(blackjack.deck)
    
    print(f"Player's starting hand:\n{blackjack.player_cards}")
    cards_of_player = blackjack.totalHandValue(blackjack.player_cards)
    print(f"Dealer's starting hand:\n{blackjack.dealer_cards}")
    cards_of_dealer = blackjack.totalHandValue(blackjack.dealer_cards)
    
    while hit:
        play = input("Type h for hit or s for stand:\n")
        if play == 's':
            break
        else:
            print(f"Player's hand:\n{blackjack.player_cards}")
            blackjack.dealCardToPlayer()
            cards_of_player = blackjack.totalHandValue(blackjack.player_cards)
            if cards_of_player > 21:
                print(blackjack.drawWinner(cards_of_player, cards_of_dealer))
                return
                
    # print(blackjack.deck)
    
    
    
    while cards_of_dealer < 17:
        print(f"Dealer's hand before drawing:{blackjack.dealer_cards}")
        blackjack.dealCardToDealer()
        cards_of_dealer = blackjack.totalHandValue(blackjack.dealer_cards)
        
    print(blackjack.deck)
    print(blackjack.drawWinner(cards_of_player, cards_of_dealer))
    

    
        
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
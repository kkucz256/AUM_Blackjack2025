import random

CARDS = {
    'ACE': 1,
    'TWO': 2,
    'THREE': 3,
    'FOUR': 4,
    'FIVE': 5,
    'SIX': 6,
    'SEVEN': 7,
    'EIGHT': 8,
    'NINE': 9,
    'TEN': 10,
    'JACK': 10,
    'QUEEN': 10,
    'KING': 10 
    }

class Blackjack():
    def __init__(self):
        self.deck = []
        for key in CARDS:
            for _ in range(0,4):
                self.deck.append((key, CARDS[key]))
        
        self.player_cards = []
        self.dealer_cards = []
        
    def shuffleCards(self):
        random.shuffle(self.deck) 
        
    def dealCardToPlayer(self):
        self.player_cards.append(self.deck.pop())    
    
    def dealCardToDealer(self):
        self.dealer_cards.append(self.deck.pop())
        
    def drawWinner(self, player_value, dealer_value):
        if player_value > 21:
            return 'd'
        elif dealer_value > 21:
            return 'p'
        elif dealer_value > player_value:
            return 'd'
        elif player_value > dealer_value:
            return 'p'
        else:
            return 't'
          
    def totalHandValue(self, hand):
        total_value = 0
        aces = 0
        
        for card in hand:
            if card[0] == 'ACE':
                aces += 1
                total_value += 1
            else:
                total_value += card[1]  
                
        while aces > 0 and total_value + 10 <= 21:
            total_value += 10
            aces -= 1
            
        # print(total_value) 
            
        return total_value
    
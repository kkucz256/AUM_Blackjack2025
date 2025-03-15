from Cards import CARDS
import random


class Deck():
    def __init__(self):
        self.deck = [] 
        for key in CARDS:
            for _ in range(0,4):
                self.deck.append((key, CARDS[key]))  
                  
    def shuffleDeck(self):
        return random.shuffle(self.deck)
        
    # def popCard(self):
    #     return self.deck.pop()

        
        
        
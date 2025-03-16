
class Player():
    def __init__(self):
        self.hand = []
        self.hand_value = self.totalHandValue()
        
    def printHand(self):
        print(self.hand)
        
    def totalHandValue(self):
        total_value = 0
        aces = 0
        
        for card in self.hand:
            if card[0] == 'ACE':
                aces += 1
                total_value += 1
            else:
                total_value += card[1]  
                
        while aces > 0 and total_value + 10 <= 21:
            total_value += 10
            aces -= 1
            
        return total_value
    
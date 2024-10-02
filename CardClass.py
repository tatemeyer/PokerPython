class Card:
    def __init__(self, value, suit):
        self.value = value # '2' 'King' 'Ace'
        self.suit = suit # 'Hearts' 'Spades'
    def __repr__(self):
        return f"{self.value} of {self.suit}"
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    def recieve_cards(self,cards):
        self.hand.extend(cards)
    def show_hand(self):
        return f"{self.name}'s hand: {self.hand}"
    def clear_hand(self):
        self.hand = []

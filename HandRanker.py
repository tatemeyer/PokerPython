from collections import Counter

class HandRanker:
    def __init__(self, player_cards, community_cards):
        self.all_cards = player_cards + community_cards

    def card_value(self, card):
        # Convert card values to integers for comparison
        value_map = {
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'JACK': 11, 'QUEEN': 12,
            'KING': 13, 'ACE': 14
        }
        return value_map[card.value]

    def rank_count(self):
        # Count the occurrences of each card rank
        values = [self.card_value(card) for card in self.all_cards]
        return Counter(values)

    def is_flush(self):
        # Check if all cards have the same suit
        suits = [card.suit for card in self.all_cards]
        suit_count = {suit: suits.count(suit) for suit in suits}
        return max(suit_count.values()) >= 5

    def is_straight(self):
        # Check for consecutive card values
        values = sorted({self.card_value(card) for card in self.all_cards})
        for i in range(len(values) - 4):
            if values[i:i+5] == list(range(values[i], values[i] + 5)):
                return True
        # Special case: A-2-3-4-5
        if {14, 2, 3, 4, 5}.issubset(values):
            return True
        return False

    def evaluate_hand(self):
        # Combine the hand ranking checks to evaluate the hand
        card_ranks = self.rank_count()

        if self.is_flush() and self.is_straight():
            return 'Straight Flush'
        elif 4 in card_ranks.values():
            return 'Four of a Kind'
        elif 3 in card_ranks.values() and 2 in card_ranks.values():
            return 'Full House'
        elif self.is_flush():
            return 'Flush'
        elif self.is_straight():
            return 'Straight'
        elif 3 in card_ranks.values():
            return 'Three of a Kind'
        elif list(card_ranks.values()).count(2) == 2:
            return 'Two Pair'
        elif 2 in card_ranks.values():
            return 'One Pair'
        else:
            return 'High Card'
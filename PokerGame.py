import requests
import random 
from collections import Counter 

class Card:
    def __init__(self, value, suit):
        self.value = value # '2' 'King' 'Ace'
        self.suit = suit # 'Hearts' 'Spades'
    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck_id = self.create_deck()
    def create_deck(self):
        response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/')
        data = response.json()
        return data['deck_id']
    def draw_cards(self, count):
        response = requests.get(f'https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count={count}')
        cards_data = response.json()['cards']
        return [Card(card['value'], card['suit']) for card in cards_data]

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

class PokerGame:
    def __init__(self, players):
        self.deck = Deck()
        self.players = [Player(name) for name in players]
        self.community_cards = []

    def deal_hands(self):
        for player in self.players:
            player.recieve_cards(self.deck.draw_cards(2))

    def deal_community_cards(self):
        self.community_cards.extend(self.deck.draw_cards(5))
        print(f"Community Cards: {self.community_cards}")

    def evaluate_hands(self):
        hand_ranks = {}
        
        # Display the community cards
        print(f"Community Cards: {', '.join([str(card) for card in self.community_cards])}")
        
        for player in self.players:
            # Use HandRanker to evaluate the player's hand combined with the community cards
            ranker = HandRanker(player.hand, self.community_cards)
            hand_rank = ranker.evaluate_hand()
            hand_ranks[player.name] = hand_rank
            
            # Convert player's hand to a string format
            player_hand = ', '.join([str(card) for card in player.hand])
            
            # Display player's hand and their hand rank
            print(f"{player.name} has: {player_hand} -> {hand_rank}")
        
        return hand_ranks

    def determine_winner(self):
        hand_ranks = self.evaluate_hands()
        ranked_hands = ['High Card', 'One Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush']
        winner = max(hand_ranks, key=lambda player: ranked_hands.index(hand_ranks[player]))
        print(f"The winner is {winner} with a {hand_ranks[winner]}")

    def play_round(self):
        self.deal_hands()
        self.deal_community_cards()
        self.determine_winner()

    def reset_game(self):
        for player in self.players:
            player.clear_hand()
        self.community_cards = []

# Entry point
if __name__ == "__main__":
    game = PokerGame(['Tate', 'Andy', 'Jacob'])
    game.play_round()
    game.reset_game()

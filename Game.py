from Deck import Deck
from player import Player
from HandRanker import HandRanker

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
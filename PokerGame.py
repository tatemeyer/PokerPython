import requests 
import random 
from collections import Counter 
from CardClass import Card
from Game import PokerGame


# Entry point
if __name__ == "__main__":
    game = PokerGame(['Tate', 'Andy', 'Jacob'])
    game.play_round()
    game.reset_game()

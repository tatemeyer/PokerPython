import requests
from CardClass import Card

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
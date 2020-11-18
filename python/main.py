from player import Player
from environment import Environment

cards = [
    ('4', '5', 0),
    ('5', '6', 0.1),
    ('6', '7', 0.2),
    ('7', 'Q', 0.3),
    ('Q', 'J', 0.4),
    ('J', 'K', 0.5),
    ('K', 'A', 0.6),
    ('A', '2', 0.7),
    ('2', '3', 0.8),
    ('3', '4', 0.9),
]

playerHuman = Player(False, 'João')
playerIA = Player(False, 'Seu Zé')

env = Environment(cards, playerHuman, playerIA)

env.begin_game()

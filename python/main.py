from player import Player
from environment import Environment

cards = [
    ('4', '5', -0.6),
    ('5', '6', -0.5),
    ('6', '7', -0.4),
    ('7', 'Q', -0.3),
    ('Q', 'J', -0.2),
    ('J', 'K', 0.1),
    ('K', 'A', 0.0),
    ('A', '2', 0.1),
    ('2', '3', 0.2),
    ('3', '4', 0.3),
]

playerHuman = Player(False, 'João')
playerIA = Player(True, 'Seu Zé')

env = Environment(cards, playerHuman, playerIA)

env.begin_game()

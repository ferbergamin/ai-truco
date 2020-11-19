from player import Player
from environment import Environment

cards = [
    ('4', '5', -0.5),
    ('5', '6', -0.4),
    ('6', '7', -0.3),
    ('7', 'Q', -0.2),
    ('Q', 'J', -0.1),
    ('J', 'K', 0.0),
    ('K', 'A', 0.1),
    ('A', '2', 0.2),
    ('2', '3', 0.3),
    ('3', '4', 0.4),
]

playerHuman = Player(False, 'João')
playerIA = Player(True, 'Seu Zé')

env = Environment(cards, playerHuman, playerIA)

env.begin_game()

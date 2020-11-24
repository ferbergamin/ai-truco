from numpy.lib.utils import who
from neuron import Neuron

class Player:
    def __init__(self, isIA, name):
        self.points = 0
        self.cards_in_hand = []
        self.isIA = isIA
        self.playerIA = PlayerIA(name)
        self.last_card_played = None
        self.name = name
        self.can_trucar = True

    def set_points(self, incoming_points):
        self.points += incoming_points

    # Sensores
    def receive_cards(self, card):
        self.cards_in_hand.append(card)
        if self.isIA:
            self.playerIA.cards_in_hand = self.cards_in_hand

    def set_can_trucar(self, can_trucar):
        if self.isIA:
            self.playerIA.set_can_trucar(can_trucar)
        else:
            self.can_trucar = can_trucar

    # Atuadores
    def play(self, trucado, can_trucar = True, card_opponent = None, hand = 1, who_made_first = 0):
        self.can_trucar = can_trucar

        if trucado:
            return self.accept_trucada(hand)
        
        card_choice = None
        if self.isIA:
            if(card_opponent):
                self.playerIA.set_opponent_cards_played(card_opponent)
    
            card_choice = self.playerIA.play(hand, card_opponent[2], who_made_first)

        else:
            valid_choice = False
            valid_choices = [card for card in range(len(self.cards_in_hand))]

            if can_trucar:
                valid_choices.append(9)

            while not valid_choice:
                print(self.name+', escolha uma carta para jogar: ')
                self.see_cards()
                if can_trucar:
                    print("9 - trucar")
                card_choice = input()
                print(card_choice)
                if card_choice != '':
                    card_choice = int(card_choice)
                    valid_choice = card_choice in valid_choices
                if not valid_choice:
                    print('Por favor, escolha um entrada válida')

        if card_choice == 9 and can_trucar:
            return self.trucar()

        card_played = self.cards_in_hand.pop(card_choice)

        self.set_last_card_move(card_played)
        return card_played

    def set_last_card_move(self, card):
        self.last_card_played = card

    def trucar(self):
        self.set_can_trucar(False)
        return ('t', '')

    def accept_trucada(self, hand = None):
        if self.isIA:
            return self.playerIA.decide_trucada(hand)
        else:
            print('Suas cartas: ')
            self.see_cards()
            print(self.name+", você recebeu uma trucada na orelha!: \n(1) - Aceitar\n(2) - Recusar")
            if self.can_trucar:
                print("(3) - Aumentar")
            card_choice = int(input())
            return ('r', card_choice)

    def see_cards(self):
        for card in range(len(self.cards_in_hand)):
                card_name = self.card_name(self.cards_in_hand[card][1])
                print("{} - {} de {}".format(card, self.cards_in_hand[card][0], card_name))
    # Helpers

    def card_name(self, card):
        if card == 'g':
            return "ouro"
        elif card == 's':
            return "espadas"
        elif card == 'h':
            return "copas"
        elif card == 'z':
            return "paus"


class PlayerIA:
    def __init__(self, name, memory = []):
        self.name = name
        self.cards_in_hand = []
        self.who_made_first = 0
        self.opponent_cards_played = []
        self.memory = memory
        self.can_trucar = True

    # Atuadores
    def play(self, hand, opponent_card_weigth, who_made_first):
        self.who_made_first = who_made_first
        cards_in_hand_weights = [k[2] for k in self.cards_in_hand]
        cards_in_hand_mean = sum(cards_in_hand_weights)/len(cards_in_hand_weights)

        neuron_entries = [[who_made_first, opponent_card_weigth, cards_in_hand_mean, hand]]
        neuron_value = Neuron(neuron_entries).exec()


        have_major_card = False
        for card in self.cards_in_hand:
            if card[2] >= opponent_card_weigth:
                have_major_card = True
        if not have_major_card:
            return cards_in_hand_weights.index(min(cards_in_hand_weights))

        if round(neuron_value) == 1:
            if self.can_trucar:
                return self.trucar()

        k = 0

        for card_in_hand in self.cards_in_hand:
            entries_choice = [[who_made_first, self.cards_weight(self.opponent_cards_played), card_in_hand[2], hand]]
            choice_neuron = Neuron(entries_choice).exec()
            if round(choice_neuron) == 1:
                return k
            k+=1
        return 0

    def trucar(self):
        self.set_can_trucar(False)
        return 9

    def decide_trucada(self, hand):
        cards_in_hand_weight = self.cards_weight(self.cards_in_hand)
        cards_in_hand_mean = cards_in_hand_weight/len(self.cards_in_hand)
        entries_choice = [[self.who_made_first, self.cards_weight(self.opponent_cards_played), cards_in_hand_mean, hand]]
        choice_neuron = Neuron(entries_choice).exec()
        if round(choice_neuron) == 1:
            return ('r', 1)
        else:
            return ('r', 2)

    # Sensores
    def set_opponent_cards_played(self, card):
        self.opponent_cards_played.append(card)

    def clear_opponent_cards_played(self):
        self.opponent_cards_played = []

    def memory_positive_or_negative(self, memory):
        if memory['result'] == 'win':
            return 1
        return 0

    def set_can_trucar(self, can_trucar):
        self.can_trucar = can_trucar

    # Helpers
    def cards_weight(self, cards):
        return sum([k[2] for k in cards])

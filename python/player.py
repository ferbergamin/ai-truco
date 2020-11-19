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

    # Atuadores
    def play(self, trucado, can_trucar = True, card_opponent = None, hand = 1):
        self.can_trucar = can_trucar

        if trucado:
            return self.accept_trucada(hand)
        
        card_choice = None
        if self.isIA:
            if(card_opponent):
                self.playerIA.set_opponent_cards_played(card_opponent)
    
            card_choice = self.playerIA.play(hand, card_opponent[2])

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
                card_choice = int(input())
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
        self.who_made_first = None
        self.opponent_cards_played = []
        self.memory = memory

    # Atuadores
    def play(self, hand, opponent_card_weigth):

        cards_in_hand_weight = sum(k[2] for k in self.cards_in_hand)

        have_major_card = False
        for card in self.cards_in_hand:
            if card[2] >= opponent_card_weigth:
                have_major_card = True
        if not have_major_card:
            return cards_in_hand_weight.index(min(cards_in_hand_weight))

        entries_trucar = [self.who_made_first, self.opponent_cards_played, cards_in_hand_weight, hand]
       
        trucar_neuron = Neuron(entries_trucar, self.consult_memory(entries_trucar, 'trucar')).decider_step_func()
        if trucar_neuron():
            return self.trucar()

        k = 0
        for card_in_hand in self.cards_in_hand:
            entries_choice = [self.who_made_first, self.opponent_cards_played, card_in_hand[2], hand]
            choice_neuron = Neuron(entries_choice, self.consult_memory(entries_choice, 'choice')).decider_step_func()
            if choice_neuron():
                return k
            k+=1

        return 0

    def trucar(self):
        return 9

    def decide_trucada(self, hand):
        cards_in_hand_weight = sum(k[2] for k in self.cards_in_hand)
        entries_trucada = [self.who_made_first, self.opponent_cards_played, cards_in_hand_weight, hand]
        decide_trucada_neuron = Neuron(entries_trucada, self.consult_memory(entries_trucada, 'decide_trucada')).decider_step_func()
        if (decide_trucada_neuron):
            return ('r', 1)
        else:
            return ('r', 2)

    # Sensores
    def set_who_made_first(self):
        pass

    def set_opponent_cards_played(self, card):
        self.opponent_cards_played.append(card)

    def cards_in_hand_weight(self):
        pass

    def memory_positive_or_negative(self, memory):
        if memory['result'] == 'win':
            return 1
        return 0

    # Desempenho
    def increment_memory(self, context):
        self.memory.append(context)

    def consult_memory(self, entries, what):
        value = 0
        memory_size = 0
        for k in self.memory:
            if k['action'] == what:
                value += int(self.memory_positive_or_negative(k))
                memory_size += 1

        return [value/memory_size]*len(entries)

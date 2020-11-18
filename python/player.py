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

    # Atuadores
    def play(self, trucado, can_trucar = True, card_opponent = None):
        self.can_trucar = can_trucar

        if trucado:
            if self.isIA:
                self.accept_trucada = self.playerIA.decide_trucada
            return self.accept_trucada()
        
        card_choice = None
        if self.isIA:
            if(card_opponent):
                self.playerIA.set_opponent_cards_played(card_opponent)
    
            card_choice = self.playerIA.play(self.cards_in_hand)

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

    def accept_trucada(self):
        if self.isIA:
            return self.playerIA.decide_trucada()
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
    def play(self, cards_in_hand):
        self.cards_in_hand = cards_in_hand

        return 

    def trucar(self):
        return 9

    def decide_trucada(self):
        return ('r', 1)

    # Sensores
    def set_who_made_first(self):
        pass

    def set_opponent_cards_played(self, card):
        self.opponent_cards_played.append(card)

    def cards_in_hand_weight(self):
        pass

    def memory_positive_or_negative(self, memory):
        return True

    # Desempenho
    def increment_memory(self, context):
        self.memory.append(context)

    def consult_memory(self, what):
        for k in self.memory:
            if what in k:
                return self.memory_positive_or_negative(k)
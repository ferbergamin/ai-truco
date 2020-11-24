from player import Player
from numpy.random import choice
import os
import time

class Environment:
    def __init__(self, cards: list, Player1: Player, Player2: Player):
        self.cards = cards
        self.nipes = ['g', 's', 'h', 'z']
        self.card_fall = None
        self.manilas = []
        self.player_last_card_move = None
        self.current_hand = 0
        self.p1 = Player1
        self.p2 = Player2
        self.hand_win_history = []
        self.round_truco = False
        self.initiator_player = self.p1
        self.finisher_player = self.p2
        self.round_points_value = 1
        
    ### Game Begin
    def begin_game(self):
        winner: Player = False
        game_over = False
        while not game_over:
            self.round_builder()
            game_over, winner = self.game_over()

        if winner:
            print(winner.name +" venceu!")

    ### Round begin
    def round_builder(self):
        self.p1.set_can_trucar(True)
        self.p2.set_can_trucar(True)
        self.p1.playerIA.clear_opponent_cards_played()
        self.p2.playerIA.clear_opponent_cards_played()
        self.get_random_card_fall()
        manila = self.find_manila(self.card_fall)
        self.set_manilas(manila)
        self.give_cards()
        self.current_hand += 1
        print("================================================================")
        print('Três cartas é jogo marreco!')
        print("================================================================")

        self.play_round()
        time.sleep(2)
        os.system("cls")
        print("================================================================")
        print("Pontuação: \n{} {} \n{} {}".format(self.p1.name, self.p1.points, self.p2.name, self.p2.points))
        print("================================================================")

        self.hand_win_history = []
        self.manilas = []
        self.p1.cards_in_hand = []
        self.p2.cards_in_hand = []
        self.round_points_value = 1

    def set_card_fall(self, card):
        self.card_fall = card

    def find_manila(self, card):
        for card_from_deck in self.cards:
            if card_from_deck[0] == card:
                return card_from_deck[1]

    def set_manilas(self, manila):
        for nipe in self.nipes:
            self.manilas.append((manila, nipe))
            
    
    def give_cards(self):
        deck = []
        # Mount deck
        for card in self.cards:
            peso = card[2]
            
            for nipe in self.nipes:
                if card[0] in [i[0] for i in self.manilas]:
                    if nipe == 'g':
                        peso = 0.4
                    elif nipe == 's':
                        peso = 0.5
                    elif nipe == 'h':
                        peso = 0.6
                    elif nipe == 'z':
                        peso = 0.7
                    deck.append((card[0], nipe, peso))
                else:
                    deck.append((card[0], nipe, peso))

        # Select a card position in the deck to give it to the player
        for card_gived in range(6):
            # Alternating between them to give one card each till got six cards in the game
            card_to_give = choice([i for i in range(len(deck))])
            if card_gived%2 == 0:
                # Accessing the random position selected in the deck and giving it to the player
                self.p1.receive_cards(deck[card_to_give])
            else:
                self.p2.receive_cards(deck[card_to_give])

                # Remove the card of the deck
            deck.pop(card_to_give)

    ### Round Play
    def play_round(self):
        round_over = False
        hand = 1
        while not round_over:
            print("================================================================")
            print('O tombo é '+self.card_fall+ ' e a manilha é '+self.manilas[0][0])
            print("================================================================")

            if len(self.hand_win_history) == 1:
                print(self.hand_win_history[0].name+ " fez a primeira")

            context_player_initiator = self.initiator_player.play(self.round_truco, True, self.finisher_player.last_card_played, hand, self.get_who_made_first_value(self.initiator_player))

            round_context = self.define_player_play(self.initiator_player, context_player_initiator, self.finisher_player, hand)

            round_over = round_context == True
            if round_over: break

            if not round_over:
                context_player_finisher = self.finisher_player.play(self.round_truco, True, self.initiator_player.last_card_played, hand, self.get_who_made_first_value(self.finisher_player))

                round_context = self.define_player_play(self.finisher_player, context_player_finisher, self.initiator_player, hand)
                round_over = round_context == True
                if round_over: break
            
            if round_context != 't':
                round_over = self.define_hand_winner()
                hand += 1
            time.sleep(3)
            os.system("cls")


    def define_player_play(self, player: Player, context, opponent: Player, hand):
        if context[0] == 't':
            print("TRUCADA: "+player.name + " trucou!")
            self.round_truco = True
            player.can_trucar = False
            return 't'
        elif context[0] == 'r':
            if context[1] == 1:
                self.round_points_value +=3
                print("TRUCADA: "+player.name + " aceitou a trucada!")
                self.round_truco = False
                return 't'

            elif context[1] == 2:
                print("AMARELOU!! "+player.name + " recusou a trucada!")
                self.round_truco = False

                self.hand_win_history = []
                self.give_points_to_winner(opponent)
                return True

            elif context[1] == 3:
                self.round_points_value +=3

                print("ENTÃO VEM MARRECO! "+player.name + " aumentou a trucada!")
                return 't'
        else:
            print("\nJOGADA: {} jogou {} de {}".format(player.name , player.last_card_played[0], player.card_name(player.last_card_played[1])))
            if self.initiator_player.last_card_played == None:
                return self.define_player_play(self.initiator_player, self.initiator_player.play(self.round_truco, True, self.finisher_player.last_card_played, hand, self.get_who_made_first_value(self.initiator_player)), self.finisher_player)
   
    def define_hand_winner(self):
        weight_player_initiator = self.initiator_player.last_card_played[2]
        weight_player_finisher = self.finisher_player.last_card_played[2]
        if (weight_player_initiator > weight_player_finisher):
            self.hand_win_history.append(self.initiator_player)
            print("MÃO: "+self.initiator_player.name + " fez a mão!")

        elif (weight_player_initiator < weight_player_finisher):
            self.hand_win_history.append(self.finisher_player)
            print("MÃO: "+self.finisher_player.name + " fez a mão!")
            self.set_order_players(self.finisher_player)
        else:
            self.hand_win_history.append(self.finisher_player)
            self.hand_win_history.append(self.initiator_player)
            print("VISH: Empachou")

        if len(self.hand_win_history) > 1:
            winner = self.verify_round_winner()
            if winner:
                self.hand_win_history = []
                self.give_points_to_winner(winner)
                return True
            else:
                if(len(self.initiator_player.cards_in_hand) == 0 and len(self.finisher_player.cards_in_hand) == 0):
                    print("DEU NEGA! Ninguém venceu a rodada")
                    return True
        return False

  
    def set_order_players(self, player: Player = None):
        if player:
            self.initiator_player = player
            if player == self.p1:
                self.finisher_player = self.p2
            else:
                self.finisher_player = self.p1
        else:
            if(self.initiator_player == self.p1):
                self.initiator_player = self.p2
                self.finisher_player = self.p1
            else:
                self.initiator_player = self.p1
                self.finisher_player = self.p2
    
    def get_who_made_first_value(self, player):
        if len(self.hand_win_history) == 0:
            return 0
        elif player == self.hand_win_history[0]:
            return 1
        else:
            return -1

    ### Round Over

    def give_points_to_winner(self, winner: Player):
        if self.round_points_value > 1:
            self.round_points_value -= 1
        winner.set_points(self.round_points_value)

    def verify_round_winner(self):
        counterp1 = 0
        counterp2 = 0
        for history in self.hand_win_history:
            if history == self.p1:
                counterp1 += 1
            else:
                counterp2 +=1
        
        if counterp1 == counterp2:
            return False
        elif counterp1 == 2:
            print("OLHA O OMI AÍ! "+self.p1.name + " venceu esse round")
            return self.p1
        elif counterp2 == 2:
            print("OLHA O OMI AÍ! "+self.p2.name + " venceu esse round")
            return self.p2
        else:
            return False

    ### Game end
    def game_over(self):
        return (self.p1.points >= 12 or self.p2.points >=12, self.pick_winner() )

    def pick_winner(self):
        if (self.p1.points < 12 and self.p2.points < 12): return None
        if (self.p1.points >= 12 ): return self.p1
        if (self.p2.points >= 12 ): return self.p2


    ### Helpers
    def get_random_card_fall(self):
        card_fall = choice([i[0] for i in self.cards])
        return self.set_card_fall(card_fall)

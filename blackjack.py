# BlackJack en Consola
# Práctica del libro "Python Tkinter GUI Programming by Example"

import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return " de ".join((self.value, self.suit))


class Deck:
    def __init__(self):
        # List Comprehension (crea una lista a partir de otra)
        self.cards = [Card(s, v)
                      for s in ["Spades", "Clubs",
                                "Hearts", "Diamonds"]
                      for v in ["A", "2", "3",
                                          "4", "5", "6",
                                          "7", "8", "9",
                                          "10", "J", "Q",
                                          "K"]]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)


class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        if self.dealer:
            print("- Carta oculta -")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            print("\n --- Valor total:", self.get_value())


class Game:
    def __init__(self):
        playing = True

        while playing:
            # Creamos un deck
            self.deck = Deck()
            self.deck.shuffle()

            # Creamos las manos del jugador y del dealer
            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print("-- Su mano es: --")
            self.player_hand.display()
            print()
            print("-- La mano del crupier es: --")
            self.dealer_hand.display()

            game_over = False

            while not game_over:
                # Chequeamos si alguno tiene BlackJack (21)
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results(
                        player_has_blackjack, dealer_has_blackjack)
                    continue

                # Le damos la oportunidad al jugador de pedir o quedarse
                choice = input("Por favor, elija [Pedir / Quedarse] ").lower()
                while choice not in ["p", "q", "pedir", "quedarse"]:
                    choice = input(
                        "Por favor, ingrese 'pedir' or 'quedarse' (o p/q) ").lower()

                if choice in ['pedir', 'p']:
                    # Si pidió carta, le damos una y mostramos su mano
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display()
                    if self.player_is_over():
                        print("--- Usted perdió! ---")
                        game_over = True

                # Cuando decide quedarse (Stick)
                else:
                    print("---- Resultados finales ----")
                    print("-- Su mano:", self.player_hand.get_value())
                    print("-- Mano del crupier:", self.dealer_hand.get_value())

                    if self.player_hand.get_value() > self.dealer_hand.get_value():
                        print("--- Usted gana! ---")
                    elif self.player_hand.get_value() == self.dealer_hand.get_value():
                        print("--- Empate! ---")
                    else:
                        print("--- Gana el crupier! ---")

                    # Termina el juego
                    game_over = True

            # Game Over = True
            again = input("Quiere jugar de nuevo? [S/N]").lower()
            while again not in ["si", "no", "s", "n"]:
                again = input("Por favor, ingrese 'Y' or 'N'").lower()

            if again in ["n", "no"]:
                print("Gracias por jugar!")
                playing = False
            else:
                game_over = False

    def check_for_blackjack(self):
        player = False
        dealer = False

        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer = True

        return player, dealer

    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            print("Ambos tienen BlackJack! Empate!")
        elif player_has_blackjack:
            print("Usted tiene BlackJack! Usted ganó!")
        elif dealer_has_blackjack:
            print("El crupier tiene BlackJack! La casa gana!")

    def player_is_over(self):
        # True si se pasó de 21
        return self.player_hand.get_value() > 21


# Main loop
# Página 37 del libro (48 del PDF)
if __name__ == "__main__":
    game = Game()

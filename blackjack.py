# libraries of cards and suits

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

import random

# creating a card class
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    # define string property for each card
    def __str__(self):
        return self.rank + ' of ' + self.suit

# create deck class
class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            # deck contains 1 of each card
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        # deck shuffler using random lib
        random.shuffle(self.all_cards)

    def draw(self):
        # draw 1 card
        return self.all_cards.pop(0)

# create player class
class Player:
    def __init__(self, name):
        # players have a name, a hand (list of card classes from card.draw()), and a balance
        self.name = name
        self.hand = []
        self.balance = 0

    def deposit(self, amount):
        # add to balance
        self.balance = self.balance + int(amount)

    def bet(self, amount):
        # if player bet size too high, they must increase balance until >= bet size
        while int(amount) > self.balance:
            print(f'Bet too high. Your balance is {str(self.balance)}')
            self.deposit(amount=input('How much would you like to deposit?\n'))
        return amount

    def player_card(self, new_card):
        # deal player 1 card
        self.hand.append(new_card)

    def __str__(self):
        # determining string value for player
        for card in self.hand:
            return str(card)

    def total_value(self):
        # calling dictionary values to determine value of hands
        total = 0
        for card in self.hand:
            total = total + card.value
        
        # creating exceptions for Aces = 1 or 11
        if total > 21:
            total = 0
            for card in self.hand:
                if card.rank == 'Ace': # if ace in hand
                    card.value = 1 # aces = 1
                total = total + card.value
        return total

def print_hand(player):
    # show a player's hand
    print(f"{player.name}'s cards:")
    for card in player.hand:
        print(card)


def blackjack(player):
    # creating blackjack rule
    if len(player.hand) == 2 and player.total_value() == 21:
        return True
    else:
        return False

def game_on():
    # if player wants new hand, game is on and continues loop
    if input('Deal new hand?\n').lower == 'yes':
        return True
    else:
        return False

def check_winner(player,dealer):
    # checks for winner
    if player.total_value() == dealer.total_value():
        return 'push'
    elif player.total_value() < dealer.total_value():
        return 'dealer'
    else:
        return 'player'

def check_bust(player):
    # checks for bust for either player or dealer
    if player.total_value() > 21:
        return True
    else:
        return False

def bust(player):
    # shows player their hand, total, and notifies of bust
    # settles balance

    print_hand(player)
    print(f'PLAYER AT: {player.total_value()}')
    print('BUST') # else, bust
    player.balance = player.balance - bet
    print(f'Your balance is {player.balance}.')

def reset():
    # game reset, new deck, and shuffles
    deck = Deck()
    deck.shuffle()
    player.hand = []
    dealer.hand = []

def board_state():
    # prints board state
    print('')
    print_hand(dealer)
    print(f'DEALER AT: {dealer.total_value()}')
    print('')
    print_hand(player)
    print(f'PLAYER AT: {player.total_value()}')

player = Player('Player 1')
dealer = Player('Dealer')  # Create players

player.deposit(amount=input('How much do you you want to deposit?\n'))

# reset and shuffle deck

# place bet
deck = Deck()
deck.shuffle()
player.hand = []
dealer.hand = []

# draw starting hands
while input('New hand?\n').lower() == 'yes':
    reset()
    bet = player.bet(amount=int(input('Bet size?\n')))
    dealer.player_card(deck.draw())
    player.player_card(deck.draw())
    player.player_card(deck.draw())

    board_state()




    game_on = True
    while game_on:
        # check for blackjack
        if blackjack(player):
            if dealer.total_value() == 10:
                # if the dealer has a blackjack
                print('Blackjack?')
                dealer.player_card(deck.draw())
                # check for push
                if blackjack(dealer):
                    board_state()
                    print('PUSH')
                    break
                else:
                    # else, pay player bet * 1.5
                    player.balance = player.balance + (bet * 1.5)
                    print('PLAYER BLACKJACK WINS!')
                    print(f'Your balance is {player.balance}.')
                    break
            else:
                player.balance = player.balance + (bet * 1.5)
                print('PLAYER BLACKJACK WINS!')
                print(f'Your balance is {player.balance}.')
                break


        answer = input("Hit or stand?\n").lower()
        if answer == 'hit':
            player.player_card(deck.draw()) 
            # draw from deck
            print_hand(player)
            print(f'PLAYER AT: {player.total_value()}')
            if check_bust(player): # check to see if player bust
                bust(player)
                break
            else:
                board_state()
        elif answer == 'stand':
            # deal dealer hands until bust or 17-21, compare hand and settle balances appropriately
            while dealer.total_value() not in range(17, 28): 
                # while dealer not inbetween 17 and 21, draw
                dealer.player_card(deck.draw())
                print('')
                print_hand(dealer)
                print(f'DEALER AT: {dealer.total_value()}')
            if blackjack(dealer):
                print('DEALER BLACKJACK WINS!')
                player.balance = player.balance - bet
                print(f'Your balance is {player.balance}.')
                break
            elif dealer.total_value() > 21: # if dealer over 21
                player.balance = player.balance + bet
                print('PLAYER WINS!')
                print(f'Your balance is {player.balance}.')
                break
            elif check_winner(player, dealer) == 'push':
                print('PUSH')
                print(f'Your balance is {player.balance}.')
                break
            elif check_winner(player, dealer) == 'player':
                player.balance = player.balance + bet
                print('PLAYER WINS!')
                print(f'Your balance is {player.balance}.')
                break
            else:
                print('DEALER WINS!')
                player.balance = player.balance - bet
                print(f'Your balance is {player.balance}.')
                break
    reset()

print(f'You have ended with a balance of {player.balance}.')


# to add: splitting, doubling, a system in which you are not FORCED to update your balance to keep playing
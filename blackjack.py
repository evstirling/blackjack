import random
import time

# Version Number

version = '1.4.0'

# Cardset

cards = [
    ['Ace', 'Hearts', 1, 11], ['Ace', 'Spades', 1, 11], ['Ace', 'Diamonds', 1, 11], [ 'Ace', 'Clubs', 1, 11],
    ['Two', 'Hearts', 2], ['Two', 'Spades', 2], ['Two', 'Diamonds', 2], ['Two', 'Clubs', 2],
    ['Three', 'Hearts', 3], ['Three', 'Spades', 3], ['Three', 'Diamonds', 3], ['Three', 'Clubs', 3],
    ['Four', 'Hearts', 4], ['Four', 'Spades', 4], ['Four', 'Diamonds', 4], ['Four', 'Clubs', 4],
    ['Five', 'Hearts', 5], ['Five', 'Spades', 5], ['Five', 'Diamonds', 5], ['Five', 'Clubs', 5],
    ['Six', 'Hearts', 6], ['Six', 'Spades', 6], ['Six', 'Diamonds', 6], ['Six', 'Clubs', 6],
    ['Seven', 'Hearts', 7], ['Seven', 'Spades', 7], ['Seven', 'Diamonds', 7], ['Seven', 'Clubs', 7],
    ['Eight', 'Hearts', 8], ['Eight', 'Spades', 8], ['Eight', 'Diamonds', 8], ['Eight', 'Clubs', 8],
    ['Nine', 'Hearts', 9], ['Nine', 'Spades', 9], ['Nine', 'Diamonds', 9], ['Nine', 'Clubs', 9],
    ['Ten', 'Hearts', 10], ['Ten', 'Spades', 10], ['Ten', 'Diamonds', 10], ['Ten', 'Clubs', 10],
    ['Jack', 'Hearts', 10], ['Jack', 'Spades', 10], ['Jack', 'Diamonds', 10], ['Jack', 'Clubs', 10],
    ['Queen', 'Hearts', 10], ['Queen', 'Spades', 10], ['Queen', 'Diamonds', 10], ['Queen', 'Clubs', 10],
    ['King', 'Hearts', 10], ['King', 'Spades', 10], ['King', 'Diamonds', 10], ['King', 'Clubs', 10],
    ]

# Variable inits

auto_deck = 1
auto_mode = False
auto_test_counter = 0
card_record = []
discard = []
final_shuffle = False
play_again = True
record = []
record_auto_params = []
session_record = []
session_card_record = []

# Classes

class Player:

    def __init__(self):
        self.ace_selector = 0
        self.bust = False
        self.cards_drawn = 0
        self.double_down = False
        self.draw = False
        self.first_card = []
        self.hit_or_stick = 'Hit'
        self.second_card = []
        self.score = 0
        self.turn = False
        self.win = False
        self.bet = ''
        self.stick = 0
        self.all_in_counter = 0
        self.bust_counter = 0
        self.chips = 100
        self.counter = 0
        self.hands_drawn = 0
        self.hands_played = 0
        self.hands_to_play = 0
        self.hands_won = 0
        self.net_change = 0
        self.total_cards_drawn = 0

    def auto_params(self): # Auto mode parameter settings
        global auto_deck
        global live_deck
        global record_auto_params
        
        # auto_stick

        stick_value = False
        while stick_value == False:
            auto.stick = input('Enter stick value: ')
            if auto.stick.isdigit() == True and int(auto.stick) > 0 and int(auto.stick) <= 21:
                auto.stick = int(auto.stick)
                break
            else: 
                print('Invalid input. Please input a whole number greater than zero but less than 21.')

        # auto_hands
                
        hands_value = False
        while hands_value == False:
            auto.hands_to_play = input('Enter number of games to run: ')
            if auto.hands_to_play.isdigit() == True and int(auto.hands_to_play) > 0:
                auto.hands_to_play = int(auto.hands_to_play)
                break
            else: 
                print('Invalid input. Please input a whole number greater than zero.')
        
        # auto_deck

        deck_value = False
        while deck_value == False:
            auto_deck = input('Enter number of decks of cards (max 4): ')
            if auto_deck.isdigit() == True and int(auto_deck) > 1 and int(auto_deck) < 5:
                auto_deck = int(auto_deck)
                break
            elif auto_deck.isdigit() == True and int(auto_deck) == 1:
                break
            else: 
                print('Invalid input. Please input a whole number between 1 and 4.')

        # auto_ace

        ace_value = False
        while ace_value == False:
            auto.ace_selector = input('Enter Ace breakpoint (default is 10): ')
            if auto.ace_selector.isdigit() == True and int(auto.ace_selector) > 0 and int(auto.ace_selector) <= 21:
                auto.ace_selector = int(auto.ace_selector)
                break
            else: 
                print('Invalid input. Please input a whole number greater than zero but less than 21.')

        # auto_bet

        take_bets()

        auto.bet = player.bet

        record_auto_params = [auto.stick, auto.hands_to_play, auto.ace_selector, auto.bet]

    def compare_scores(self):
        if auto_mode == False: time.sleep(1)

        # 5 card draw

        if self.cards_drawn >= 5 and self.bust == False:
            if self != auto: 
                print('5 card draw. You win!')
            else:
                print('You win game {}.'.format(self.hands_played)) 
            self.win = True
            self.hands_won += 1

        # Dealer's 5 card draw

        elif dealer.cards_drawn >= 5 and dealer.bust == False:
            if self != auto:
                print('Dealer has 5 cards. The house wins.')
            else:
                print('Dealer wins game {}.'.format(self.hands_played))

        # Win by points / Dealer bust

        elif (self.score > dealer.score and self.bust == False) or (self.score < dealer.score and dealer.bust == True):
            if self != auto:
                print('You win!')
            else:
                print('You win game {}.'.format(self.hands_played))
            self.win = True
            self.hands_won += 1

        # Dealer wins by points

        elif self.score < dealer.score and dealer.bust == False:
            if self != auto:
                print('The house wins.')
            else:
                print('Dealer wins game {}.'.format(self.hands_played))

        # Game tied

        elif self.score == dealer.score and self.bust == False:
            if self != auto:
                print('Draw.')
            else:
                 print('Tied game {}.'.format(self.hands_played))
            self.draw = True
            self.hands_drawn += 1

        # Player bust

        elif self.bust == True:
            if self != auto:
                print("You've gone bust...")
            else:
                print('You went bust game {}.'.format(self.hands_played))

        # Error message

        else:
            print('Error calculating winner.')

        if auto_mode == False:
            time.sleep(1)
            print('')
        self.pay_out()

    def hand(self):
         
        # Human controlled turn

        if auto_mode == False and self != dealer:

            # Show dealers first card

            if self == player:
                if player.cards_drawn == 2 and split.score == 0:
                    dealer.hit()
                self.turn = True
                while self.turn == True:

                # Check bust

                    if self.score > 21 and split.first_card != split.second_card:
                        time.sleep(1)
                        self.bust = True
                        self.bust_counter += 1
                        break

                    # Check double down

                    if self.double_down == True:
                        break

                    # Check 5 cards

                    if self.cards_drawn == 5:
                        break

                    # Check 21 points

                    if self.score == 21:
                        print('You have 21 points!')
                        time.sleep(1)
                        break

                    # Hit, stick, double down, split?

                    if player.cards_drawn == 2 and player.chips >= int(player.bet) * 2 and split.first_card[0] == split.second_card[0] and split.turn == False:
                        player.hit_or_stick = input('Hit, stick, double down, or split? ')
                    elif player.cards_drawn == 2 and player.chips >= int(player.bet) * 2 and split.turn == False:
                        player.hit_or_stick = input('Hit, stick, or double down? ')
                    else:
                        self.hit_or_stick = input('Hit or stick? ') 

                    # Player and split options

                    if self.score < 21 and self.hit_or_stick == str.casefold('Hit') or self.hit_or_stick == str.casefold('h'):
                        print('Hit.')
                        time.sleep(1)
                        self.hit()
                    elif self.score <= 21 and self.hit_or_stick == str.casefold('Stick') or self.hit_or_stick == str.casefold('s'):
                        print('Stuck. You have {} points.'.format(self.score))
                        time.sleep(1)
                        break

                    # Player exclusive options

                    elif player.score <= 21 and (player.hit_or_stick == str.casefold('double down') or player.hit_or_stick == str.casefold('dd')) and player.cards_drawn == 2 and player.chips >= player.bet * 2:
                        player.bet = int(player.bet) * 2
                        player.double_down = True
                        print('Bet increased to ${}.'.format(player.bet))
                        time.sleep(1)
                        player.hit()
                    elif player.score <= 21 and player.hit_or_stick == str.casefold('split') and player.cards_drawn == 2 and player.chips >= int(player.bet) * 2 and split.first_card[0] == split.second_card[0]:
                        print('Splitting hand.')
                        time.sleep(1)
                        print('')
                        print('Hand 1:')
                        split_hand()
                    else:
                        print("Invalid input. Please enter a valid option.")
                
        # Automated turn

        elif self == auto or self == dealer:
            dealer.stick = 17

            # Dealer's print

            if self == dealer and auto_mode == False:
                print('')
                time.sleep(1)
                print("Dealer's turn:")
                time.sleep(1)
                print("The dealer's first card is the {} of {}. They have {} points.".format(dealer.first_card[0], dealer.first_card[1], dealer.score))
                time.sleep(1)
                dealer.hit()

            # Check score, stick at 17, bust at 21

            self.turn = True
            while self.turn == True:
                if auto_mode == False: time.sleep(1)
                if self.score > 21:
                    self.bust = True
                    self.bust_counter += 1
                    if auto_mode == False: print('Dealer has gone bust.')
                    break
                elif self.score >= self.stick:
                    if auto_mode == False: print('Dealer sticks.')
                    break
                elif self.score < self.stick:
                    self.hit()

        self.hands_played += 1

    def hit(self):

        # Draw Card

        draw_card()
        self.cards_drawn += 1
        self.total_cards_drawn += 1

        # Assign cards

        if self.cards_drawn == 1:
            self.first_card = drawn_card
        elif self.cards_drawn == 2:
            self.second_card = drawn_card
        
        if self == player or self == split and auto_mode == False:
            print('You received the {} of {}.'.format(drawn_card[0], drawn_card[1]))
            time.sleep(1)
        elif self == dealer and auto_mode == False:
            if self.cards_drawn >= 1:
                print('The dealer received the {} of {}.'.format(drawn_card[0], drawn_card[1]))
                time.sleep(1)

        # Show dealer's face up card

            else:
                self.first_card = drawn_card
                time.sleep(1)
                print("The dealer's face up card is the {} of {}.".format(self.first_card[0], self.first_card[1]))
                time.sleep(1)

        # Ace Selection for player 

        if (self == player or self == split) and drawn_card[0] == 'Ace':
            while self.ace_selector != 1 or self.ace_selector != 11:
                self.ace_selector = (input('Count this Ace as 1 or 11? '))
                if self.ace_selector == '1':
                    self.score += drawn_card[2]
                    break
                elif self.ace_selector == '11':
                    self.score += drawn_card[3]
                    break
                else:
                    print("Invalid response. Please enter either 1 or 11.")

        # Ace selection for cpu

        elif (self == auto or self == dealer) and drawn_card[0] == 'Ace':
            dealer.ace_selector = 10
            if self.score > self.ace_selector:
                self.score += drawn_card[2]
            elif self.score <= self.ace_selector:
                self.score += drawn_card[3]

        # Point Tally

        else:
            self.score += int(drawn_card[2])

        # Card draw tally

        if self == player and self.cards_drawn > 1: 
            print('You have {} cards, worth {} points.'.format(self.cards_drawn, self.score))
        if self == dealer and auto_mode == False and self.cards_drawn > 1:
            print('The dealer has {} cards, worth {} points.'.format(self.cards_drawn, self.score))

    def refresh(self):
        self.bust = False
        self.cards_drawn = 0
        self.double_down = False
        self.draw = False
        self.first_card = []
        self.hit_or_stick = 'Hit'
        self.second_card = []
        self.score = 0
        self.turn = False
        self.win = False
        if self == player or self == split:
            self.ace_selector = 0
            self.bet = ''
            
    def pay_out(self): 
        if self.win == True:
            if self != auto: print('Your chip stack has increased by ${}!'.format(self.bet))
            self.chips += self.bet
            self.net_change += self.bet
        elif self.draw == True:
            if self != auto: print('Bets returned.')
        else:
            if self != auto: print('Better luck next time!')
            self.chips -= self.bet
            self.net_change -= self.bet

    def view_stats(self): # Calculate and view session stats
        global auto_test_counter
        global card_record
        global final_shuffle
        global record
        global record_auto_params
        global session_record

        # Final shuffle

        final_shuffle = True
        shuffle()
        final_shuffle = False

        # Calc Stats

        win_rate = int((self.hands_won/self.hands_played) * 100)
        net_change_rate = round(self.net_change/self.hands_played, 2)
        avg_cards = round(self.total_cards_drawn/self.hands_played, 2)
        tie_rate = int((self.hands_drawn/self.hands_played) * 100)
        bust_rate = int((self.bust_counter/self.hands_played) * 100)

        record_stats = [self.hands_played, win_rate, net_change_rate, win_rate, self.bet, avg_cards, tie_rate, bust_rate] 

        # Save stats to session records, clear temp records

        record = [auto_test_counter] + record_auto_params + record_stats
        session_record.append(record.copy())
        session_card_record.append(card_record.copy())
        record = []
        record_auto_params = []
        record_stats = [] 
        card_record = []

        # Ask to, then display stats 

        view_stats_confirmation = False
        while view_stats_confirmation == False:
            open_stats = input("View session stats? [Yes/No] ")
            if open_stats == str.casefold('Yes') or open_stats == str.casefold('Y'):

                # (rude) Win rate

                if self.hands_played == 1 and self.hands_won == 1: 
                    print('You won the only hand you played.')
                elif self.hands_played == 1 and self.hands_won == 0 and self.hands_drawn == 0:
                    print('You lost the only hand you played. Way to go, champ.')
                elif self.hands_played == 1 and self.hands_drawn == 1:
                    print('You tied the only hand you played.') 
                else:
                    print('You won {} hands out of {} games played, for a win rate of {}%.'.format(self.hands_won, self.hands_played, win_rate))
                    time.sleep(0.5)
                    if self.net_change > 0:
                        print("You made ${} in net profit! That's ${} per game.".format(self.net_change, net_change_rate))
                    elif self.net_change < 0:
                        print("You lost a total of -${}. That's -${} per game.".format(abs(self.net_change), abs(net_change_rate)))
                    else:
                        print('You broke even.')
                time.sleep(1)

                # Avg cards

                if self.total_cards_drawn == 69:
                    print("You've drawn {} cards this session. Nice.".format(self.total_cards_drawn))
                else:
                    print("You've drawn a total of {} cards, for an average of {} cards per game.".format(self.total_cards_drawn, avg_cards))
                time.sleep(1)

                # Hands drawn

                if self.hands_drawn == 1:
                    print('You had {} tie during your session for a tie rate of {}%.'.format(self.hands_drawn, tie_rate))
                    time.sleep(1)
                elif self.hands_drawn > 0:
                    print('You had {} ties during your session for a tie rate of {}%.'.format(self.hands_drawn, tie_rate))
                    time.sleep(1)

                # Bust count

                if self.bust_counter == 1:
                    print('You went bust {} time for a bust rate of {}%.'.format(self.bust_counter, bust_rate))
                    time.sleep(1)
                elif self.bust_counter > 0:
                    print('You went bust {} times for a bust rate of {}%.'.format(self.bust_counter, bust_rate))
                    time.sleep(1)

                # All in counter

                if self.all_in_counter == 1 and auto_mode == False:
                    print('You went all in {} time.'.format(self.all_in_counter))
                    time.sleep(1) 
                elif self.all_in_counter > 0 and auto_mode == False:
                    print('You went all in {} times.'.format(self.all_in_counter))
                    time.sleep(1) 

                # Split counter
                
                if split.counter == 1:
                    print('You split {} hand.'.format(split.counter))
                elif split.counter > 0:
                    print('You split {} hands.'.format(split.counter))
            
                break
            elif open_stats == str.casefold('No') or open_stats == str.casefold('N'):
                break
            else:
                print('Invalid input. Please input yes or no.')

player = Player()
split = Player()
auto = Player()
dealer = Player()

# Functions

def core_game_loop(): # Main sequence of standard game function

    # Game number

    print('  +=============+')
    print(' /  Game #{}:  /'.format(player.hands_played))
    print('+=============+')

    # Opening Hand

    player.hit()
    split.first_card = drawn_card
    player.hit()
    split.second_card = drawn_card
    player.hand()

    # If player busts, game ends. If player has drawn 5 cards, they win

    if player.bust == False and player.cards_drawn < 5:
        dealer.hand()
    elif player.bust == True and split.bust == False and split.turn == True:
        dealer.hand()

    if split.turn == True:
        print("Hand 1:")
        time.sleep(1)
        split.compare_scores()
        time.sleep(1)
        print('')
        print('Hand 2:')
        time.sleep(1)
    player.compare_scores()

def draw_card(): # Pull card from deck, add to discard pile
    global discard
    global drawn_card
    global live_deck

    number = random.randint(0, (len(live_deck)-1))
    drawn_card = live_deck[number]
    live_deck.pop(number)
    discard.append(drawn_card)

def intro(): # Introductory text
    global version

    title_text = """  
        __   __         __     _          __              
       / /  / /__ _____/ /__  (_)__ _____/ /__  ___  __ __
      / _ \/ / _ `/ __/  '_/ / / _ `/ __/  '_/ / _ \/ // /
     /_.__/_/\_,_/\__/_/\_\_/ /\_,_/\__/_/\_(_) .__/\_, / 
                         |___/               /_/   /___/  
                                                  v{}
""".format(version)
    print(title_text)
    time.sleep(1.5)
    intro_text = """
     +===================+
    /   House Rules :   /               
    +=====================================================+
    |   Win back what you bet, bets returned in a draw.   | 
    |       Dealer sticks on 17 and evaluates Aces.       |
    |   5 card draw wins. Double down on first turn only. |    
    +=====================================================+
                                        /  Buy in : $100  /
                                       +=================+

    """
    print(intro_text)   
    time.sleep(1)

def keep_playing(): # Loop the game until user exits or runs out of $$$
    global play_again

    # Buy back in if out of funds

    if player.chips == 0:
        buy_in_confirmation = False
        while buy_in_confirmation == False:
            buy_in = input("You're out of funds. Buy back in? [Yes/No] ") 
            if buy_in == str.casefold('Yes') or buy_in == str.casefold('Y'):
                player.chips += 100
                play_again = True
                break
            elif buy_in == str.casefold('No') or buy_in == str.casefold('N'):
                play_again = False
                print("You're right, walking away is sometimes the best option.")
                time.sleep(1)
                print('Thanks for playing! Goodbye!')
                break
            else:
                print('Invalid update. Please input yes or no.')
   
    # Continue?

    else:
        play_again_confirmation = False
        while play_again_confirmation == False:
            continue_game = input("Play one more hand? [Yes/No] ")
            if continue_game == str.casefold('Yes') or continue_game == str.casefold('Y'):
                play_again = True
                break
            elif continue_game == str.casefold('No') or continue_game == str.casefold('N'):
                play_again = False
                time.sleep(0.7)
                print('Your end total is ${}! Thanks for playing!'.format(player.chips))
                time.sleep(0.7)
                break
            else:
                print('Invalid input. Please input yes or no.')

def mode_auto(): # Auto mode complete game loop
    global auto_mode
    global auto_test_counter
    global live_deck

    # Auto mode selected

    auto_mode = True
    continue_sim = True
    while continue_sim == True:
        auto_test_counter += 1
        time.sleep(0.5)
        print('  +=============+')
        print(' /  Test #{}:  /'.format(auto_test_counter))
        print('+=============+')
        auto.auto_params()
        while auto.hands_played < auto.hands_to_play:
            shuffle()
            auto.hit()
            dealer.hit()
            auto.hit()
            auto.hand()
            dealer.hit() 
            dealer.hand()
            auto.compare_scores()
            if auto.hands_to_play <= 100: time.sleep(0.02)
        auto.view_stats()

        # Run another test, reset test variables

        continue_game = input("Run another test? [Yes/No] ")
        if continue_game == str.casefold('Yes') or continue_game == str.casefold('Y'):
                continue_sim = True
                auto.bust_counter = 0
                auto.hands_drawn = 0
                auto.hands_played = 0
                auto.hands_won = 0 
                auto.net_change = 0
                auto.chips = 100
                auto.total_cards_drawn = 0
        elif continue_game == str.casefold('No') or continue_game == str.casefold('N'):
                continue_sim = False
                print('Thanks for testing the sim! Goodbye!')
                break
        else:
            print('Invalid input. Please input yes or no.')

def mode_selection(): # Select and load game mode (either mode_auto or mode_standard)
    mode_select = False
    while mode_select == False:
        mode = input('Please select your game mode [Standard/Auto]: ')
        if mode == str.casefold('auto') or mode == str.casefold('a'):
            print('Auto mode selected.')
            time.sleep(1)
            mode_auto()
            break
        elif mode == str.casefold('standard') or mode == str.casefold('s'):
            print('Standard mode selected.')
            time.sleep(1)
            mode_standard()
            break
        else:
            print('Invalid input. Please input auto or standard.')
            time.sleep(1)

def mode_standard(): # Standard mode complete game loop
    global play_again

    while play_again == True:
        shuffle()
        take_bets()
        core_game_loop()
        keep_playing()
    player.view_stats()

def populate_deck():
    global live_deck

    for deck in range(0, int(auto_deck)):
        for card in range(len(cards)):
            live_deck.append(cards[card])
         
def shuffle(): # Shuffle the deck, refresh the variables
    global card_record
    global discard
    global final_shuffle
    global live_deck
    
    # Main deck shuffle
    player.refresh()
    dealer.refresh()
    split.refresh()
    auto.refresh()
    live_deck = []
    if auto_mode == False and final_shuffle == False : 
        print('Shuffling the deck.')

    # Add discard back to deck, and to record

    populate_deck()
    card_record += discard
    discard = []

    if auto_mode == False and final_shuffle == False:
        for i in range(8):
            time.sleep(0.1)
            print('~', end='\r')
            time.sleep(0.1)
            print('/', end='\r')
            time.sleep(0.1)
            print('|', end='\r')
            time.sleep(0.1)
            print('\ ', end='\r')
        
def split_hand(): # Split hand function, player's 'first' hand

    split.bet = 0
   
    # Split hand into two

    if split.first_card[0] == 'Ace' and player.score > 11:
        player.score -= split.first_card[3]
        split.score += split.first_card[3]
    else:
        player.score -= split.first_card[2]
        split.score += split.first_card[2]
    player.cards_drawn -= 1
    split.cards_drawn += 1
    split.bet += player.bet
    split.counter += 1

    # Split turn
    print('Your first card is the {} of {}. You have {} points.'.format(split.first_card[0], split.first_card[1], split.score))
    time.sleep(1)
    split.hand()
    print("")
    print('Hand 2:')
    time.sleep(1)
    print('Your first card is the {} of {}. You have {} points.'.format(split.second_card[0], split.second_card[1], player.score))
 
def take_bets(): # Receive and process bet input from user
    global auto_mode

    # Show player.chips

    if auto_mode == False:
        print('You have ${}.'.format(player.chips))
        time.sleep(1.2)

    # Bet validation

    bet_confirmation = False
    while bet_confirmation == False:
        player.bet = input('Place your bets: $')
        if  player.bet.isdigit() == False:
            print('Invalid input, please enter a whole number.')
            time.sleep(1)
        elif player.bet.isdigit() == True and int(player.bet) > player.chips and auto_mode == False:
            print('Insufficient funds.')
            player.bet = 0
        elif player.bet.isdigit() == True:
            if int(player.bet) == player.chips:
                print('All in!')
                player.all_in_counter += 1
            else:
                print('Your bet is ${}. Good luck!'.format(player.bet))
            time.sleep(1)
            break

    player.bet = int(player.bet) 

# Game sequence

intro()
mode_selection()
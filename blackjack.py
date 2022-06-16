import random
import time

# Version Number

version = '1.3.3'

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

ace_selector = 0
all_in_counter = 0
auto_ace = 0
auto_deck = 1
auto_hands = 0
auto_mode = False
auto_stick = 0
auto_test_counter = 0
bet = ''
bust_counter = 0
cards_drawn = 0
card_record = []
dealer_bust = False
dealer_cards_drawn = 0
dealer_first_value = 0
dealer_score = 0
discard = []
double_down = False
draw = False
hands_drawn = 0
hands_played = 0
hands_won = 0
hit_or_stick = 'Hit'
live_deck = cards
net_change = 0
play_again = True
player_bust = False
player_chips = 100
player_score = 0
player_win = False
record = []
session_record = []
split_bet = 0
split_cards_drawn = 0
split_counter = 0
split_draw = False
split_first_card = []
split_hand_score = 0
split_second_card = []
split_win = False
timer = 0
total_cards_drawn = 0

# Functions

def auto_compare():
    global bust_counter
    global cards_drawn
    global dealer_bust
    global dealer_cards_drawn
    global dealer_score
    global draw
    global hands_drawn
    global hands_won
    global net_change
    global player_score
    global player_bust
    global player_chips
    global player_win
    global play_again

    # Win conditions

    if cards_drawn >= 5 and player_bust == False:
        print('You win game {}.'.format(hands_played)) 
        player_win = True
        hands_won += 1
    elif dealer_cards_drawn >= 5 and dealer_bust == False:
        print('Dealer wins game {}.'.format(hands_played))
    elif player_score > dealer_score and player_bust == False:
        print('You win game {}.'.format(hands_played)) 
        player_win = True
        hands_won += 1
    elif player_score < dealer_score and dealer_bust == True:
        print('You win game {}.'.format(hands_played)) 
        player_win = True
        hands_won += 1
    elif player_score < dealer_score and dealer_bust == False:
        print('Dealer wins game {}.'.format(hands_played))
    elif player_score == dealer_score and player_bust == False:
        print('Tied game {}.'.format(hands_played))
        draw = True
        hands_drawn += 1
    elif player_bust == True:
        print('You went bust game {}.'.format(hands_played))
        bust_counter += 1
    else:
        print('Error calculating winner.')

    # Pay out

    if player_win == True:
        player_chips += int(bet)
        net_change += int(bet)
    elif player_win == False:
        player_chips -= int(bet)
        net_change -= int(bet)

def auto_dealer_hit():
    global dealer_cards_drawn
    global dealer_score
    global discard
    global drawn_card
    global live_deck

    # Draw Card

    draw_card()

    # Ace Determination

    if drawn_card[0] == 'Ace':
        if dealer_score > 10:
            dealer_score += drawn_card[2]
        elif dealer_score <= 10:
            dealer_score += drawn_card[3]

    # Point Tally

    else:
        dealer_score += int(drawn_card[2])
    dealer_cards_drawn += 1

def auto_dealer_turn():
    global dealer_bust
    global dealer_score

    # Check score, stick at 17, bust at 21

    dealers_turn = True
    while dealers_turn == True:
        if dealer_score > 21:
            dealer_bust = True
            break
        elif dealer_score >= 17:
            break
        elif dealer_score < 17:
            auto_dealer_hit()

def auto_hit():
    global auto_ace
    global cards_drawn
    global discard
    global drawn_card
    global player_score
    global total_cards_drawn

    # Draw Card

    draw_card()

    # Ace Determination

    if drawn_card[0] == 'Ace':
        if player_score > auto_ace:
            player_score += drawn_card[2]
        elif player_score <= auto_ace:
            player_score += drawn_card[3]

    # Point Tally

    else:
        player_score += int(drawn_card[2])
    cards_drawn += 1
    total_cards_drawn += 1

def auto_params():
    global auto_ace
    global auto_deck
    global auto_hands
    global auto_mode 
    global auto_stick
    global live_deck
    
    # auto_stick

    stick_value = False
    while stick_value == False:
        auto_stick = input('Enter stick value: ')
        if auto_stick.isdigit() == True and int(auto_stick) > 0 and int(auto_stick) <= 21:
            auto_stick = int(auto_stick)
            break
        else: 
            print('Invalid input. Please input a whole number greater than zero but less than 21.')

    # auto_hands
            
    hands_value = False
    while hands_value == False:
        auto_hands = input('Enter number of games to run: ')
        if auto_hands.isdigit() == True and int(auto_hands) > 0:
            auto_hands = int(auto_hands)
            break
        else: 
            print('Invalid input. Please input a whole number greater than zero.')
    
    # auto_deck

    deck_value = False
    while deck_value == False:
        auto_deck = input('Enter number of decks of cards (max 4): ')
        if auto_deck.isdigit() == True and int(auto_deck) > 1 and int(auto_deck) < 5:
            for i in (range(int(auto_deck) - 1)):
                live_deck += live_deck
                auto_deck = int(auto_deck)
            break
        elif auto_deck.isdigit() == True and int(auto_deck) == 1:
            break
        else: 
            print('Invalid input. Please input a whole number greater than zero.')

    # auto_ace

    ace_value = False
    while ace_value == False:
        auto_ace = input('Enter Ace breakpoint (default is 10): ')
        if auto_ace.isdigit() == True and int(auto_ace) > 0 and int(auto_ace) <= 21:
            auto_ace = int(auto_ace)
            break
        else: 
            print('Invalid input. Please input a whole number greater than zero but less than 21.')

    # auto_bet

    take_bets()

def auto_turn():
    global auto_stick
    global live_deck
    global player_bust
    global player_score

    # Check score, stick at auto_stick, bust at 21

    auto_turn = True
    while auto_turn == True:
        if player_score > 21:
            player_bust = True
            break
        elif player_score >= auto_stick:
            break
        elif player_score < auto_stick:
            auto_hit()

def compare_scores(): # Score comparison and pay_out call
    global cards_drawn
    global dealer_bust
    global dealer_cards_drawn
    global dealer_score
    global draw
    global hands_drawn
    global hands_won
    global player_score
    global player_bust
    global player_win
    global play_again
    global split_bet
    global split_bust
    global split_cards_drawn
    global split_draw
    global split_hand_score
    global split_turn
    global split_win

    print('')
    time.sleep(1)

    # Win conditions, if split
        
    if split_turn == True:
        print("Hand 1:")
        time.sleep(1)
        if split_cards_drawn >= 5 and split_bust == False:
            print('You have 5 cards. You win!') 
            split_win = True
            hands_won += 1
        elif dealer_cards_drawn >= 5 and dealer_bust == False:
            print('Dealer has 5 cards. The house wins.')
        elif split_hand_score > dealer_score and split_bust == False:
            print('You win!')
            split_win = True
            hands_won += 1
        elif split_hand_score < dealer_score and dealer_bust == True:
            print('You win!')
            split_win = True
            hands_won += 1
        elif split_hand_score < dealer_score and dealer_bust == False:
            print('The house wins.')
        elif split_hand_score == dealer_score and player_bust == False:
            print('Draw.')
            split_draw = True
            hands_drawn += 1
        elif split_bust == True:
            print('You went bust.')
        time.sleep(1)
        pay_out()
        time.sleep(1)
        print('')
        print('Hand 2:')
        time.sleep(1)
        
    # Win conditions

    if cards_drawn >= 5 and player_bust == False:
        print('You have 5 cards. You win!') 
        player_win = True
        hands_won += 1
    elif dealer_cards_drawn >= 5 and dealer_bust == False:
        print('Dealer has 5 cards. The house wins.')
        time.sleep(1)
    elif player_score > dealer_score and player_bust == False:
        print('You win!')
        player_win = True
        hands_won += 1
    elif player_score < dealer_score and dealer_bust == True:
        print('You win!')
        player_win = True
        hands_won += 1
    elif player_score < dealer_score and dealer_bust == False:
        print('The house wins.')
        time.sleep(1)
    elif player_score == dealer_score and player_bust == False:
        print('Draw.')
        draw = True
        hands_drawn += 1
    elif player_bust == True and split_turn == True:
        print('You went bust.')

    pay_out()

def core_game_loop(): # Main sequence of game functions
    global cards_drawn
    global hands_played
    global split_first_card
    global split_second_card

    # Game number

    print('===============')
    print('   Game #{}:'.format(hands_played))
    print('===============')

    # Opening Hand

    hit()
    split_first_card = drawn_card
    hit()
    split_second_card = drawn_card
    player_turn()

    # If player busts, game ends. If player has drawn 5 cards, they win

    if player_bust == False and cards_drawn < 5:
        dealer_turn()

    compare_scores()

def dealer_hit(): # Dealer's draw phase
    global dealer_score
    global dealer_cards_drawn
    global dealer_first_value
    global discard
    global drawn_card
    global live_deck

    # Draw Card

    draw_card()
    if dealer_cards_drawn >= 1:
        print('The dealer received the {} of {}.'.format(drawn_card[0], drawn_card[1]))
        time.sleep(1)

    # Show dealer's face up card

    else:
        time.sleep(1)
        print("The dealer's face up card is the {} of {}.".format(drawn_card[0], drawn_card[1]))
        time.sleep(1)

    # Ace Determination

    if drawn_card[0] == 'Ace':
        if dealer_score >= 11:
            dealer_score += drawn_card[2]
        elif dealer_score <= 10:
            dealer_score += drawn_card[3]

    # Point Tally

    else:
        dealer_score += int(drawn_card[2])

    if dealer_cards_drawn >= 1:
        if dealer_score == 1:
            print('The dealer has {} point.'.format(dealer_score))
        else:
            print('The dealer has {} points.'.format(dealer_score))

    # Dealer first card value (for future algos)

    else:
        dealer_first_value += dealer_score

    # Card count

    dealer_cards_drawn += 1

def dealer_turn(): # Dealer's turn sequence
    global dealer_bust
    global dealer_score
    global live_deck

    # Start turn

    print('')
    time.sleep(0.5)
    print("Dealer's turn:")
    time.sleep(1)
    dealer_hit()

    # Check score, stick at 17, bust at 21

    dealers_turn = True
    while dealers_turn == True:
        time.sleep(1)
        if dealer_score > 21:
            dealer_bust = True
            print('Dealer has gone bust.')
            break
        elif dealer_score >= 17:
            print('Dealer sticks.')
            break
        elif dealer_score < 17:
            dealer_hit()

def draw_card():
    global discard
    global drawn_card
    global live_deck

    number = random.randint(0, (len(live_deck)-1))
    drawn_card = live_deck[number]
    live_deck.pop(number)
    discard.append(drawn_card)

def hit():  # Hit me babey
    global ace_selector
    global cards_drawn
    global player_score
    global total_cards_drawn

    # Draw Card

    draw_card()
    print('You received the {} of {}.'.format(drawn_card[0], drawn_card[1]))
    time.sleep(1)

    # Ace Selection

    if drawn_card[0] == 'Ace':
        while ace_selector != 1 or ace_selector != 11:
            ace_selector = (input('Count this Ace as 1 or 11? '))
            if ace_selector == '1':
                player_score += drawn_card[2]
                break
            elif ace_selector == '11':
                player_score += drawn_card[3]
                break
            else:
                print("Invalid response. Please enter either 1 or 11.")

    # Point Tally

    else:
        player_score += int(drawn_card[2])

    # Card draw tally

    cards_drawn += 1
    total_cards_drawn += 1
    if cards_drawn > 1: print('You have {} cards, worth {} points.'.format(cards_drawn, player_score))

def intro(): # Introductory text
    global version

    print('Welcome to Blackjack.py v{}.'.format(version))
    time.sleep(1)
    print('Thanks for checking it out!')
    time.sleep(1)
    intro_text = """
    +===================+
    |   House Rules :   |               
    +=====================================================+
    |   Win back what you bet, bets returned in a draw.   | 
    |       Dealer sticks on 17 and evaluates Aces.       |
    |   5 card draw wins. Double down on first turn only. |    
    +=====================================================+
                                        |  Buy in : $100  |
                                        +=================+
    """
    print(intro_text)   
    time.sleep(1)

def keep_playing(): # Loop the game until user exits or runs out of $$$
    global hands_won
    global play_again
    global player_chips

    # Buy back in if out of funds

    if player_chips == 0:
        buy_in_confirmation = False
        while buy_in_confirmation == False:
            buy_in = input("You're out of funds. Buy back in? [Yes/No] ") 
            if buy_in == str.casefold('Yes') or buy_in == str.casefold('Y'):
                player_chips += 100
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
                print('Your end total is ${}! Thanks for playing!'.format(player_chips))
                time.sleep(0.7)
                break
            else:
                print('Invalid input. Please input yes or no.')

def mode_auto():
    global auto_mode
    global auto_test_counter
    global bust_counter
    global hands_drawn
    global hands_played
    global hands_won
    global net_change
    global player_chips
    global total_cards_drawn

    # Auto mode selected

    auto_mode = True
    continue_sim = True
    while continue_sim == True:
        auto_test_counter += 1
        time.sleep(0.5)
        print('===============')
        print('   Test #{}:'.format(auto_test_counter))
        print('===============')
        auto_params()
        while hands_played < auto_hands:
            shuffle()
            auto_turn() 
            auto_dealer_turn()
            auto_compare()
            if auto_hands <= 100: time.sleep(0.02)
        view_stats()

        # Run another test, reset test variables

        continue_game = input("Run another test? [Yes/No] ")
        if continue_game == str.casefold('Yes') or continue_game == str.casefold('Y'):
                continue_sim = True
                bust_counter = 0
                hands_drawn = 0
                hands_played = 0
                hands_won = 0 
                net_change = 0
                player_chips = 100
                total_cards_drawn = 0
                for entry in range(len(record)): record.pop()
                print('')
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

def mode_standard():
    global play_again

    while play_again == True:
        shuffle()
        take_bets()
        core_game_loop()
        keep_playing()
    view_stats()

def pay_out(): # Modify player_chips depending on game result
    global bet
    global draw
    global net_change
    global player_chips
    global player_win
    global split_bet
    global split_draw
    global split_turn
    global split_win

    # Split conditions
    
    if split_turn == True:
        if split_win == True:
            print('Congrats! You win ${}!'.format(bet))
            player_chips += split_bet
            net_change += split_bet
        elif split_draw == True:
            print('Bets returned.')
        else:
            print('Better luck next time!')
            player_chips -= split_bet
            net_change -= split_bet
        split_turn = False

    # Win/Draw/Lose

    else:
        if player_win == True:
            print('Congrats! You win ${}!'.format(bet))
            player_chips += int(bet)
            net_change += int(bet)
        elif draw == True:
            print('Bets returned.')
        else:
            print('Better luck next time!')
            player_chips -= int(bet)
            net_change -= int(bet)
        time.sleep(1)

def player_turn(): # Player's turn sequence
    global bet
    global bust_counter
    global cards_drawn
    global double_down
    global hit_or_stick
    global live_deck
    global player_bust
    global player_chips
    global player_score
    global split_first_card
    global split_second_card

    players_turn = True

        # Show dealers first card

    if cards_drawn == 2 and split_hand_score == 0:
        dealer_hit()

    while players_turn == True:

        # Check bust

        if player_score > 21 and split_first_card != split_second_card:
            time.sleep(1)
            player_bust = True
            bust_counter += 1
            print("You've gone bust...")
            time.sleep(1)
            break

        # Check double down

        if double_down == True:
            break

        # Check 5 cards

        if cards_drawn == 5:
            break

        # Check 21 points

        if player_score == 21:
            time.sleep(1)
            print('You have 21 points!')
            break

        # Hit, stick, double down, split?

        if cards_drawn == 2 and player_chips >= int(bet) * 2 and split_first_card[0] == split_second_card[0] and split_turn == False:
            hit_or_stick = input('Hit, stick, double down, or split? ')
        elif cards_drawn == 2 and player_chips >= int(bet) * 2 and split_turn == False:
            hit_or_stick = input('Hit, stick, or double down? ')
        else:
            hit_or_stick = input('Hit or stick? ') 

        # Player options

        if player_score < 21 and hit_or_stick == str.casefold('Hit'):
            print('Hit.')
            time.sleep(1)
            hit()
        elif player_score <= 21 and hit_or_stick == str.casefold('Stick'):
            print('Stuck. You have {} points.'.format(player_score))
            time.sleep(1)
            break
        elif player_score <= 21 and hit_or_stick == str.casefold('double down') and cards_drawn == 2 and player_chips >= int(bet) * 2:
            bet = int(bet) * 2
            double_down = True
            print('Bet increased to ${}.'.format(bet))
            time.sleep(1)
            hit()
        elif player_score <= 21 and hit_or_stick == str.casefold('split') and cards_drawn == 2 and player_chips >= int(bet) * 2 and split_first_card[0] == split_second_card[0]:
            print('Splitting hand.')
            time.sleep(1)
            print('')
            print('Hand 1:')
            split()
        else:
            print("Invalid input. Please enter a valid option.")

def shuffle(): # Shuffle the deck, refresh the variables
    global ace_selector
    global bet
    global cards_drawn
    global card_record
    global dealer_bust
    global dealer_cards_drawn
    global dealer_first_value
    global dealer_score
    global discard
    global double_down
    global draw
    global hands_played
    global hit_or_stick
    global live_deck
    global player_bust
    global player_score
    global player_win
    global split_bet
    global split_bust
    global split_cards_drawn
    global split_draw
    global split_first_card
    global split_hand_score
    global split_second_card
    global split_turn

    # Main deck shuffle

    if auto_mode == False: 
        print('Shuffling the deck.')
        ace_selector = 0
        bet = ''
    cards_drawn = 0
    dealer_bust = False
    dealer_cards_drawn = 0
    dealer_first_value = 0
    dealer_score = 0
    double_down = False
    draw = False
    hands_played += 1
    hit_or_stick = 'Hit'
    player_bust = False
    player_score = 0
    player_win = False
    split_bet = 0
    split_bust = False
    split_cards_drawn = 0
    split_draw = False
    split_first_card = []
    split_hand_score = 0
    split_second_card = []
    split_turn = False

    # Add discard back to deck, and to record

    live_deck += discard
    card_record += discard
    for entry in range(len(discard)):
        discard.pop()

    if auto_mode == False:
        for i in range(3):
            time.sleep(0.7)
            print('.')
def split():
    global bet
    global bust_counter
    global cards_drawn
    global player_score
    global split_bet
    global split_bust
    global split_cards_drawn
    global split_counter
    global split_first_card
    global split_hand_score
    global split_second_card
    global split_turn

    # Split hand into two

    if split_first_card[0] == 'Ace' and player_score > 11:
        player_score -= split_first_card[3]
        split_hand_score += split_first_card[3]
    else:
        player_score -= split_first_card[2]
        split_hand_score += split_first_card[2]
    cards_drawn -= 1
    split_cards_drawn += 1
    split_bet += bet
    split_counter += 1

    # Split turn

    split_turn = True
    while split_turn == True:

        # Check bust

        if split_hand_score > 21:
            time.sleep(1)
            split_bust = True
            bust_counter += 1
            print("You've gone bust...")
            time.sleep(1)
            break

        # Check 5 cards

        if split_cards_drawn == 5:
            break

        # Check 21 points

        if split_hand_score == 21:
            time.sleep(1)
            print('You have 21 points!')
            break

        # Hit or stick

        hit_or_stick = input('Hit or stick? ') 
        if split_hand_score < 21 and hit_or_stick == str.casefold('Hit'):
            print('Hit.')
            time.sleep(1)
            split_hit()
        elif split_hand_score <= 21 and hit_or_stick == str.casefold('Stick'):
            print('Stuck. You have {} points.'.format(split_hand_score))
            time.sleep(1)
            break
        else:
            print('Invalid input. Please enter a valid option.')  

    print("")
    print('Hand 2:')
    time.sleep(1)
    print('Your first card is the {} of {}. You have {} points.'.format(split_second_card[0], split_second_card[1], player_score))

def split_hit():
    global ace_selector
    global split_cards_drawn
    global split_hand_score
    global total_cards_drawn

    # Draw Card

    draw_card()
    print('You received the {} of {}.'.format(drawn_card[0], drawn_card[1]))
    time.sleep(1)

    # Ace Selection

    if drawn_card[0] == 'Ace':
        while ace_selector != 1 or ace_selector != 11:
            ace_selector = (input('Count this Ace as 1 or 11? '))
            if ace_selector == '1':
                split_hand_score += drawn_card[2]
                break
            elif ace_selector == '11':
                split_hand_score += drawn_card[3]
                break
            else:
                print("Invalid response. Please enter either 1 or 11.")

    # Point Tally

    else:
        split_hand_score += int(drawn_card[2])

    # Card draw tally

    split_cards_drawn += 1
    total_cards_drawn += 1
    if split_cards_drawn > 1: print('You have {} cards, worth {} points.'.format(split_cards_drawn, split_hand_score))

    
def take_bets(): # Receive and process bet input from user
    global all_in_counter
    global auto_mode
    global bet
    global player_chips

    if auto_mode == False:
        print('You have ${}.'.format(player_chips))
        time.sleep(1.2)
    bet_confirmation = False
    while bet_confirmation == False:
        bet = input('Place your bets: $')
        if  bet.isdigit() == False:
            print('Invalid input, please enter a whole number.')
            time.sleep(1)
        elif bet.isdigit() == True and int(bet) > player_chips and auto_mode == False:
            print('Insufficient funds.')
            bet = 0
        elif bet.isdigit() == True:
            if int(bet) == player_chips:
                print('All in!')
                all_in_counter += 1
            else:
                print('Your bet is ${}. Good luck!'.format(bet))
            time.sleep(1)
            break
    bet = int(bet) 

def view_stats():
    global auto_test_counter
    global all_in_counter
    global bust_counter
    global hands_drawn
    global hands_played
    global hands_won
    global net_change
    global record
    global session_record
    global split_counter
    global total_cards_drawn

    # Calc Stats

    win_rate = int((hands_won/hands_played) * 100)
    net_change_rate = round(net_change/hands_played, 2)
    avg_cards = round(total_cards_drawn/hands_played, 2)
    tie_rate = int((hands_drawn/hands_played) * 100)
    bust_rate = int((bust_counter/hands_played) * 100)

    # Save stats to records

    record = [auto_test_counter, auto_hands, auto_stick, auto_deck, auto_ace, hands_played, win_rate, net_change, avg_cards, tie_rate, bust_rate]
    session_record.append(record.copy())
    for entry in range(len(record)):
        record.pop()

    # Ask to, then display stats 

    view_stats_confirmation = False
    while view_stats_confirmation == False:
        open_stats = input("View session stats? [Yes/No] ")
        if open_stats == str.casefold('Yes') or open_stats == str.casefold('Y'):

            # (rude) Win rate

            if hands_played == 1 and hands_won == 1: 
                print('You won the only hand you played.')
            elif hands_played == 1 and hands_won == 0 and hands_drawn == 0:
                print('You lost the only hand you played. Way to go, champ.')
            elif hands_played == 1 and hands_drawn == 1:
                print('One game, one draw. But you knew that already.') 
            else:
                print('You won {} hands out of {} games played, for a win rate of {}%.'.format(hands_won, hands_played, win_rate))
                time.sleep(0.5)
                if net_change > 0:
                    print("You made ${} in net profit! That's ${} per game.".format(net_change, net_change_rate))
                elif net_change < 0:
                    print("You lost a total of -${}. That's -${} per game.".format(abs(net_change), abs(net_change_rate)))
                else:
                    print('You broke even.')
            time.sleep(1)

            # Avg cards

            if total_cards_drawn == 69:
                print("You've drawn {} cards this session. Nice.".format(total_cards_drawn))
            else:
                print("You've drawn a total of {} cards, for an average of {} cards per game.".format(total_cards_drawn, avg_cards))
            time.sleep(1)

            # Other stats

            if hands_drawn == 1:
                print('You had {} tie during your session for a tie rate of {}%.'.format(hands_drawn, tie_rate))
                time.sleep(1)
            elif hands_drawn > 0:
                print('You had {} ties during your session for a tie rate of {}%.'.format(hands_drawn, tie_rate))
                time.sleep(1)

            if bust_counter == 1:
                print('You went bust {} time for a bust rate of {}%.'.format(bust_counter, bust_rate))
                time.sleep(1)
            elif bust_counter > 0:
                print('You went bust {} times for a bust rate of {}%.'.format(bust_counter, bust_rate))
                time.sleep(1)

            if all_in_counter == 1 and auto_mode == False:
                print('You went all in {} time.'.format(all_in_counter))
                time.sleep(1) 
            elif all_in_counter > 0 and auto_mode == False:
                print('You went all in {} times.'.format(all_in_counter))
                time.sleep(1) 
            
            if split_counter == 1:
                print('You split {} hand.'.format(split_counter))
            elif split_counter > 0:
                print('You split {} hands.'.format(split_counter))
        
            break
        elif open_stats == str.casefold('No') or open_stats == str.casefold('N'):
            break
        else:
            print('Invalid input. Please input yes or no.')


# Game sequence

intro()
mode_selection()
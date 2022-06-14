import random
import time

# Version Number

version = '1.2.1'

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
bet = ''
cards_drawn = 0
dealer_bust = False
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
timer = 0
total_cards_drawn = 0

# Timer
while play_again == True:
    time.sleep(1)
    timer += 1
    

# Functions

def compare_scores(): # Score comparison and pay_out call
    global player_score
    global dealer_score
    global player_bust
    global dealer_bust
    global cards_drawn
    global player_win
    global draw
    global play_again
    global hands_won
    global hands_drawn

    # Win conditions
    time.sleep(1)
    print('')
    if cards_drawn >= 5 and player_bust == False:
        print('You drew 5 cards. You win!') 
        player_win = True
        hands_won += 1
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

    pay_out()

def core_game_loop(): # Main sequence of game functions
    global cards_drawn

    # Opening Hand
    hit()
    hit()
    
    player_turn()

    # If player busts, game ends. If player has drawn 5 cards, they win
    if player_bust == False and cards_drawn < 5:
        dealer_turn()

    compare_scores()

def dealer_hit(): # Dealer's draw phase
    global dealer_score
    global live_deck
    global discard
    global drawn_card

    # Draw Card

    draw_card()
    print('The dealer received the ' + drawn_card[0] + ' of ' + drawn_card[1] + '.')
    time.sleep(1)

    # Point Tally (Dealer treats all Aces as 1)
    dealer_score += int(drawn_card[2])
    if dealer_score == 1:
        print('The dealer has ' + str(dealer_score) + ' point.')
    else:
        print('The dealer has ' + str(dealer_score) + ' points.')

def dealer_turn(): # Dealer's turn sequence
    global dealer_score
    global dealer_bust
    global live_deck

    print('')
    time.sleep(0.5)
    print("Dealer's turn:")
    time.sleep(1)
    dealer_hit()

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
    global drawn_card
    global live_deck
    global discard

    number = random.randint(0, (len(live_deck)-1))
    drawn_card = live_deck[number]
    live_deck.pop(number)
    discard.append(drawn_card)

def hit():  # Hit me babey

    # Draw Card
    draw_card()
    print('You received the ' + drawn_card[0] + ' of ' + drawn_card[1] + '.')
    time.sleep(1)

    # Ace Selection + Point Tally
    global player_score
    global ace_selector
    global cards_drawn
    global total_cards_drawn

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
    else:
        player_score += int(drawn_card[2])
    cards_drawn += 1
    total_cards_drawn += 1
    if cards_drawn > 1: print('You have ' + str(player_score) + ' points with ' + str(cards_drawn) + ' cards.')

def intro(): # Introductory text
    global version

    print('Welcome to Blackjack v ' + version + '. This is a project I aim to grow as I learn new skills.')
    time.sleep(1)
    print('Thanks for checking it out!')
    time.sleep(2)
    intro_text = """
    +===================+
    |   House Rules :   |               
    +=====================================================+
    |   Win back what you bet, bets returned in a draw.   | 
    |    Dealer sticks on 17 and treats all Aces as 1.    |
    |   5 card draw wins. Double down on first turn only. |    
    +=====================================================+
                                        |  Buy in : $100  |
                                        +=================+
    """
    print(intro_text)   
    time.sleep(1)


def keep_playing(): # Loop the game until user exits or runs out of $$$
    global play_again
    global player_chips
    global hands_played
    global hands_won

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
                print('Your end total is $' + str(player_chips) + '!')
                time.sleep(0.7)
                break
            else:
                print('Invalid input. Please input yes or no.')

def pay_out(): # Modify player_chips depending on game result
    global bet
    global player_chips
    global player_win
    global draw
    global net_change

    # Win/Draw/Lose
    if player_win == True:
        print('Congrats! You win $' + str(bet) + '!')
        player_chips += int(bet)
        net_change += int(bet)
    elif draw == True:
        print('Bets returned.')
    else:
        print('Better luck next time!')
        player_chips -= int(bet)
        net_change -= int(bet)

    time.sleep(2)

def player_turn(): # Player's turn sequence
    global player_score
    global player_bust
    global hit_or_stick
    global live_deck
    global bet
    global cards_drawn
    global double_down
    global player_chips

    players_turn = True
    while players_turn == True:

        # Check bust
        if player_score > 21:
            time.sleep(1)
            player_bust = True
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
            print('You have 21 points! Stuck.')
            break

        # Hit, stick or double down?
        if cards_drawn == 2 and player_chips >= int(bet) * 2:
            hit_or_stick = input('Hit, stick, or double down? ')
        else:
            hit_or_stick = input('Hit or stick? ') 

        # Player options
        if player_score < 21 and hit_or_stick == str.casefold('Hit'):
            print('Hit.')
            time.sleep(1)
            hit()
        elif player_score <= 21 and hit_or_stick == str.casefold('Stick'):
            print('Stuck. You have ' + str(player_score)  + ' points.')
            time.sleep(1)
            break
        elif player_score <= 21 and hit_or_stick == str.casefold('double down') and cards_drawn == 2 and player_chips >= int(bet) * 2:
            bet = int(bet) * 2
            double_down = True
            print('Bet increased to $' + str(bet) + '.')
            time.sleep(1)
            hit()
        else:
            print("Invalid input. Please type either hit or stick.")

def shuffle(): # Shuffle the deck, refresh the variables
    global live_deck
    global player_score
    global player_bust
    global dealer_score
    global dealer_bust
    global ace_selector
    global hit_or_stick
    global cards_drawn
    global bet
    global player_win
    global draw
    global hands_played
    global double_down
    global discard

    print('Shuffling the deck.')
    player_score = 0
    player_bust = False
    dealer_score = 0
    dealer_bust = False
    ace_selector = 0
    hit_or_stick = 'Hit'
    cards_drawn = 0
    bet = ''
    player_win = False
    draw = False
    hands_played += 1
    double_down = False

    # Add discard back to deck
    live_deck = live_deck + discard
    for entry in range(len(discard)):
        discard.pop()

    for i in range(3):
        time.sleep(0.7)
        print('.')
    
    
def take_bets(): # Receive and process bet input from user
    global bet
    global all_in_counter
    global player_chips

    print('You have $' + str(player_chips) + '.')
    time.sleep(1.2)
    bet_confirmation = False
    while bet_confirmation == False:
        bet = input('Place your bets: $')
        if  bet.isdigit() == False:
            print('Invalid input, please enter a whole number.')
            time.sleep(1)
        elif bet.isdigit() == True and int(bet) > player_chips:
            print('Insufficient funds.')
            bet = 0
        elif bet.isdigit() == True:
            if int(bet) == player_chips:
                print('All in!')
                all_in_counter += 1
            else:
                print('Your bet is $' + str(bet) + '. Good luck!')
            time.sleep(1)
            break

def view_stats():
    global all_in_counter
    global hands_drawn
    global hands_won
    global hands_played
    global net_change
    global total_cards_drawn
    global timer

    # Calc Stats
    win_rate = int((hands_won/hands_played) * 100)
    avg_cards = round(total_cards_drawn/hands_played, 1)

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
                print('You won ' + str(hands_won) + ' hands out of ' + str(hands_played) + ' games played, for a win rate of ' + str(win_rate) + '%.')
                time.sleep(0.5)
                if net_change > 0:
                    print("You made $" + str(net_change) + " in net profit!")
                elif net_change < 0:
                    print("You lost a total of $" + str(abs(net_change)) + ".")
                else:
                    print('You broke even.')
            time.sleep(1)

            # Avg cards

            if total_cards_drawn == 69:
                print("You've drawn " + str(total_cards_drawn) + " cards this session. Nice.")
            else:
                print("You've drawn a total of " + str(total_cards_drawn) + " cards, for an average of " + str(avg_cards) + " cards per game.")
            time.sleep(1)

            # Timer

            if timer > 60:
                timer = timer/60
                print('Session length: {} minutes.'.format(timer))

            # Other stats

            if hands_drawn == 1:
                print('You had ' + str(hands_drawn) + ' draw during your session.')
                time.sleep(1)
            elif hands_drawn > 0:
                print('You had ' + str(hands_drawn) + ' draws during your session.')
                time.sleep(1)

            if all_in_counter == 1:
                print('You went all in ' + str(all_in_counter) + ' time.')
                time.sleep(1) 
            elif all_in_counter > 0:
                print('You went all in ' + str(all_in_counter) + ' times.')
                time.sleep(1) 
        
            break
        elif open_stats == str.casefold('No') or open_stats == str.casefold('N'):
            break
        else:
            print('Invalid update. Please input yes or no.')
    
    print('Thanks for playing. Goodbye!')

# Game sequence
intro()
while play_again == True:
    shuffle()
    take_bets()
    core_game_loop()
    keep_playing()
view_stats()
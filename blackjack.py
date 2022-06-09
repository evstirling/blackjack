import random
import time

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
live_deck = cards
player_score = 0
player_bust = False
dealer_score = 0
dealer_bust = False
ace_selector = 0
hit_or_stick = 'Hit'
cards_drawn = 0

# Functions
def shuffle(): # Shuffle the deck, refresh the variables
    live_deck = cards
    player_score = 0
    player_bust = False
    dealer_score = 0
    dealer_bust = False
    ace_selector = 0
    hit_or_stick = 'Hit'
    cards_drawn = 0

def hit():  # Hit me babey
    # Draw Card
    number = random.randint(0, len(live_deck))
    drawn_card = live_deck[number]
    live_deck.pop(number)
    print('You received the ' + drawn_card[0] + ' of ' + drawn_card[1] + '.')

    # Ace Selection + Point Tally
    global player_score
    global ace_selector
    global cards_drawn
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
    print('You have ' + str(player_score) + ' points with ' + str(cards_drawn) + ' cards.')

def player_turn():
    global player_score
    global player_bust
    global hit_or_stick
    global live_deck

    # Hit or stick
    for cards in live_deck:
        if player_score > 21:
            player_bust = True
            print("You're busted!")
            break
        hit_or_stick = input('Hit or Stick? ') 
        if player_score <= 21 and hit_or_stick == str.casefold('Hit'):
            hit()
        elif player_score <= 21 and hit_or_stick == str.casefold('Stick'):
            break
        else:
            print("Invalid input. Please type either Hit or Stick")

def dealer_hit():
    global dealer_score
    global live_deck

    # Draw Card
    number = random.randint(0, len(live_deck))
    drawn_card = live_deck[number]
    live_deck.pop(number)
    print('The dealer drew ' + drawn_card[0] + ' of ' + drawn_card[1] + '.')

    # Point Tally (Dealer treats all Aces as 1)
    dealer_score += int(drawn_card[2])
    print('The dealer has ' + str(dealer_score) + ' points.')

def dealer_turn():
    global dealer_score
    global dealer_bust
    global live_deck

    dealer_hit()
    for cards in live_deck:
        time.sleep(0.7)
        if dealer_score > 21:
            dealer_bust = True
            print('Dealer has busted.')
            break
        elif dealer_score >= 17:
            break
        elif dealer_score < 17:
            dealer_hit()

def compare_scores():
    global player_score
    global dealer_score
    global player_bust
    global dealer_bust

    if player_score > dealer_score and player_bust == False:
        print('You win!')
    elif player_score < dealer_score and dealer_bust == True:
        print('You win!')
    elif player_score < dealer_score and dealer_bust == False:
        print('The house wins.')
    elif player_score == dealer_score and player_bust == False:
        print('Draw.')

# ACTUAL GAME SEQUENCE

# Shuffle Deck
shuffle()

# Opening Hand
hit()
hit()

player_turn()

# If player busts, game ends
if player_bust == False:
    dealer_turn()

if cards_drawn >= 5:
    print('You win!')
else:
    compare_scores()
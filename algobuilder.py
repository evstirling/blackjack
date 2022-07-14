from curses.ascii import isdigit
import time
import json

# Version number

version = '1.0.0'

# Functions

def build_dict():

    # Create potential values

    point_values = [i for i in range(2, 22)]
    dealer_values = [i for i in range(2, 12)]
    new_dict = {}

    # Combine values in a tuple, then dictionary

    for key in range(len(point_values)):
        for value in range(len(dealer_values)):
            new_key = (point_values[key], dealer_values[value])
            new_dict.update({new_key: ''})
        
    return(new_dict)

def add_values(dictionary):

    # Make dict keys iterable

    new_dict = {}
    keys = list(dictionary.keys())

    # Set hit below/stick over

    while True:
        hit_below = input('Hit for all point values below and including: ')
        if hit_below.isdigit() == True and 1 < int(hit_below) <= 21:
            hit_below = int(hit_below)
            break
        else:
            print('Invalid input. Please enter a whole number that is 21 or below.') 
    
    while True:
        stick_over = input('Stick for all point values above and including: ')
        if stick_over.isdigit() == True and 1 < int(stick_over) <= 21:
            stick_over = int(stick_over)
            break
        else:
            print('Invalid input. Please enter a whole number that is 21 or below.') 

    print('Hitting at {} and below, sticking at {} and above.'.format(hit_below, stick_over), end='\n')
    time.sleep(1)
    print('')

    # Guide text

    print("Enter action given player points and dealer's face up card.")
    print("| h = hit | s = stick | dd = double down | b = go back one stage |")
    time.sleep(1)

    # Take and process input

    key = 0
    while key < (len(keys)):
        if keys[key][0] <= hit_below:
            value = 'h'
        elif keys[key][0] >= stick_over:
            value = 's'
        else:
            while True:
                value = input("You have {} points, the dealer has {}: ".format(keys[key][0], keys[key][1]))
                print('\033[1A' + '\033[K', end='')
                if value == str.casefold('h') or value == str.casefold('s') or value == str.casefold('dd'):
                    break
                elif value == str.casefold('b'):
                    key -= 1
                else:
                    print('Please enter a valid command. ', end='')
        converted_key = ''.join(str(keys[key]))
        new_dict.update({converted_key: value})
        key += 1

    return(new_dict)

def name_file():
    while True:
        filename = input("Enter desired algo name: ")
        if len(filename) >= 64:
            print("Entered name is too long. Max character length is 64")
        else:
            filename = filename.replace(" ", "_")
            break

    filename += '.json' 
    return(filename)

# Main program

print('algobuilder.py for blackjack.py, v{}.'.format(version))
params = build_dict()
params = add_values(params)
filename = name_file()

with open(filename, 'w') as json_file:
    json.dump(params, json_file)
print('{} created in current directory.'.format(filename))
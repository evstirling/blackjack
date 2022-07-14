                                    #########################
                                    [   B L A C K J A C K   ]
                                    #########################
                                    |   by Evan Stirling    |
                                    |  Updated: July 13/22  |
                                    #########################

## Repository Description:

    This repository acts to measure my progress as I grow as a programmer and build a portfolio.
    I plan to expand and recreate this project in different languages as I expand my skill set.
    Feel free to fork this repo and try the games out for yourself!

## File Descriptions:

blackjack.py: 
    Command line game of blackjack. The first independent project I have created.

    Modes:
        Standard - A standard game of Blackjack. Get as close to 21 points as possible and try to beat the dealer.
        Auto - Simulate large volumes of games and view statistics on wins/draws/busts etc.
             - Build custom algorithms using algobuilder.py to test new strategies.

    Future features:
        Export stats as .csv
        Multiplayer mode
        Data visulaization

algobuilder.py:
    Algorithm builder for auto mode in blackjack.py.
    Export custom algorithms in .json format.
    Algos currently include hit/stick/double down values for each player point value and dealer's face up card value.
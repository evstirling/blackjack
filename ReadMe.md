# Blackjack

Last updated: Aug 31th, 2022

## Repository Description:

This repository acts to measure my progress as I grow as a programmer and build a portfolio.
I plan to expand and recreate this project in different languages as I expand my skill set.
Feel free to fork this repo and try the games out for yourself!

---

## File Descriptions:

### ***Python***

**blackjack.py:** 
    Command line game of blackjack.

*Modes:* 

1. Standard 
   - A standard game of Blackjack. Get as close to 21 points as possible and try to beat the dealer.
2.  Auto 
    - Simulate large volumes of games and view statistics on wins/draws/busts etc.
    - Build custom algorithms using algobuilder.py to test new strategies.

*Future features:*
- Export stats as .csv
- Multiplayer mode
- Data visulaization

**algobuilder.py:**
Algorithm builder for auto mode in blackjack.py.
Export custom algorithms in .json format.
Algos currently include hit/stick/double down values for each player point value and dealer's face up card value.

### ***Rust***

**blackjack.exe:**
    Most recent build of the Rust version of blackjack. Further details below.

**src**/*main.rs:*
    Command line game of blackjack, this time written in Rust. 
    Currently only includes standard mode, but future versions will include an auto mode as well.
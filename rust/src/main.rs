use rand::Rng;
use std::io;
use std::io::Write;
use std::{thread, time::Duration};

fn main() {
    // player / dealer inits
    let mut player = Player {
        id: 1,
        ..Default::default()
    };
    let mut dealer = Player {
        id: 2,
        ..Default::default()
    };

    // Main game loop
    loop {
        let mut deck = build_deck();
        player.turn(&mut deck, &mut dealer);
        // Dealer turn only happens if necessary
        match player.bust {
            true => (),
            false => match player.drawn_cards.len() {
                5 => (),
                _ => dealer.dealer_turn(&mut deck),
            },
        }
        player.compare_scores(&dealer);
        player.reset();
        dealer.reset();
        let play_again: bool = continue_game(&mut player);
        match play_again {
            true => continue,
            false => {
                view_stats(&mut player);
                break;
            }
        }
    }
}
// Player creation and functions
struct Stats {
    wins: u32,
    draws: u32,
    losses: u32,
    games_played: u32,
    cards_drawn: u32,
    net_change: i64,
    busts: u32,
    double_down: u32,
    all_in: u32,
}
impl Default for Stats {
    fn default() -> Self {
        Stats {
            wins: 0,
            draws: 0,
            losses: 0,
            games_played: 0,
            cards_drawn: 0,
            net_change: 0,
            busts: 0,
            double_down: 0,
            all_in: 0,
        }
    }
}
struct Player {
    id: u8, //  0 for default / 1 for human controlled player / 2 for dealer
    score: u8,
    bet: i32,
    chips: i32,
    bust: bool,
    turn: bool,
    double_down: bool,
    drawn_cards: Vec<Card>,
    stats: Stats,
}
impl Default for Player {
    fn default() -> Self {
        Player {
            id: 0,
            score: 0,
            bet: 0,
            chips: 100,
            bust: false,
            turn: false,
            double_down: false,
            drawn_cards: Vec::new(),
            stats: Default::default(),
        }
    }
}
impl Player {
    fn compare_scores(&mut self, dealer: &Player) {
        // Print scores (if dealer has had a turn)
        if self.bust == false && self.drawn_cards.len() < 5 && dealer.drawn_cards.len() < 5 {
            header(String::from("Score Comparison"));
            println!("You have {} points.", self.score);
            wait();
            match dealer.bust {
                true => println!("The dealer has bust."),
                false => println!("The dealer has {} points.", dealer.score),
            }
            wait();
        }
        // Who wins?
        if self.score > dealer.score && self.bust == false
            || dealer.bust == true
            || self.drawn_cards.len() == 5
        {
            println!("Congrats, you win ${}!", self.bet);
            self.stats.wins += 1;
            self.chips += self.bet;
            self.stats.net_change += self.bet as i64;
        } else if self.score < dealer.score && dealer.bust == false
            || self.bust == true
            || dealer.drawn_cards.len() == 5
        {
            println!("You lose. Better luck next time.");
            self.stats.losses += 1;
            self.chips -= self.bet;
            self.stats.net_change -= self.bet as i64;
        } else if self.score == dealer.score && self.bust == false && dealer.bust == false {
            println!("Draw. Bets returned.");
            self.stats.draws += 1;
        } else {
            println!("Error calculating winner. Bets returned.")
        }
        wait();
        self.stats.games_played += 1;
    }

    fn hit(&mut self, deck: &mut Vec<Card>) {
        // Draw card, save to cards_drawn
        let drawn_card = draw_card(deck);
        let save_card = drawn_card.clone();
        self.drawn_cards.push(save_card);
        self.stats.cards_drawn += 1;

        match self.id {
            // Player's hit
            1 => {
                if self.drawn_cards.len() >= 1 {
                    println!("You drew the {} of {}.", drawn_card.name, drawn_card.suit);
                    wait();
                }
                self.score += drawn_card.point_value.unpack(self);
            }
            // Dealer's hit
            2 => {
                match self.drawn_cards.len() {
                    1 => {
                        println!(
                            "The dealer's face up card is the {} of {}.",
                            drawn_card.name, drawn_card.suit
                        );
                        wait();
                    }
                    _ => {
                        println!(
                            "The dealer drew the {} of {}.",
                            drawn_card.name, drawn_card.suit
                        );
                        wait();
                    }
                }
                self.score += drawn_card.point_value.unpack(self);
            }
            _ => {
                println!("An unexpected error occured :(");
                wait();
            }
        }

        // Print point total and cards drawn
        if self.drawn_cards.len() > 1 {
            match self.id {
                1 => {
                    println!(
                        "You have {} cards worth {} points.",
                        self.drawn_cards.len(),
                        self.score
                    );
                    wait();
                }
                2 => {
                    println!(
                        "The dealer has {} cards worth {} points.",
                        self.drawn_cards.len(),
                        self.score
                    );
                    wait();
                }
                _ => {
                    println!("An unexpected error occured :(");
                    wait();
                }
            }
        }
    }

    fn take_bets(&mut self) {
        println!("You have ${}.", self.chips);
        wait();
        loop {
            // Take bet input
            let mut input = String::new();
            print!("Place your bets: $");
            let _ = io::stdout().flush();
            io::stdin()
                .read_line(&mut input)
                .expect("Please enter a valid number.");
            let val_input = input.trim().parse::<i32>();

            // Print confirmation
            match val_input {
                Ok(val_input) => {
                    if self.chips < val_input {
                        println!("Insufficient funds.");
                        wait();
                    } else {
                        println!("Bets placed! Good luck!");
                        self.bet = val_input;
                        if self.bet == self.chips {
                            self.stats.all_in += 1
                        };
                        wait();
                        break;
                    }
                }
                Err(_e) => {
                    println!("Please enter a valid number.");
                    wait();
                }
            }
        }
    }

    fn turn(&mut self, deck: &mut Vec<Card>, dealer: &mut Player) {
        let mut game_count = String::from("Game #");
        let game_counter = (self.stats.games_played + 1).to_string();
        game_count += &game_counter;
        header(String::from(game_count));
        self.turn = true;
        self.take_bets();
        self.hit(deck);
        self.hit(deck);
        dealer.hit(deck);
        loop {
            // Check bust
            if self.score > 21 {
                println!("You've gone bust.");
                self.bust = true;
                self.stats.busts += 1;
                wait();
                break;
            }
            // Check double down
            if self.double_down == true {
                break;
            }
            // Check 5 card draw
            if self.drawn_cards.len() >= 5 {
                println!("You have five cards!");
                wait();
                break;
            }
            // Take action
            let mut input = String::new();
            if self.drawn_cards.len() == 2 && self.bet <= self.chips / 2 {
                print!("Hit, stick, or double down? ");
            } else {
                print!("Hit or stick? ")
            }
            let _ = io::stdout().flush();
            io::stdin()
                .read_line(&mut input)
                .expect("Error taking input, please try again.");
            match input.to_lowercase().trim() {
                "h" | "hit" => self.hit(deck),
                "s" | "stick" => {
                    println!("Stuck.");
                    wait();
                    break;
                }
                "dd" | "double down" => {
                    if self.drawn_cards.len() == 2 {
                        self.double_down = true;
                        self.bet += self.bet;
                        println!("Bet increased to ${}.", self.bet);
                        self.stats.double_down += 1;
                        wait();
                        self.hit(deck);
                    } else {
                        println!("You can only double down on your first turn of the game.");
                        wait();
                    }
                }
                _ => {
                    println!("Please enter a valid input.");
                    wait();
                }
            }
        }
        self.turn = false;
    }
    fn dealer_turn(&mut self, deck: &mut Vec<Card>) {
        header(String::from("Dealer's turn."));
        self.turn = true;
        loop {
            // Check bust
            if self.score > 21 {
                println!("The dealer has bust.");
                wait();
                self.bust = true;
                break;
            }
            // Check 5 card draw
            if self.drawn_cards.len() >= 5 {
                println!("The dealer has five cards.");
                wait();
                break;
            }
            // Hit or stick
            if self.score >= 17 {
                println!("Dealer sticks.");
                wait();
                break;
            } else {
                self.hit(deck);
            }
        }
        self.turn = false;
    }
    fn reset(&mut self) {
        self.bet = 0;
        self.drawn_cards.clear();
        self.bust = false;
        self.double_down = false;
        self.score = 0;
    }
}

// Deck creation and functions
#[derive(Clone, Copy)]
enum PointValue {
    Ace(u8, u8),
    NotAce(u8),
}
impl PointValue {
    fn unpack(&self, player: &mut Player) -> u8 {
        match *self {
            PointValue::Ace(one, eleven) => match player.id {
                // Ace selection for player
                1 => loop {
                    let mut input = String::new();
                    print!("Count this ace as 1 or 11? ");
                    let _ = io::stdout().flush();
                    io::stdin()
                        .read_line(&mut input)
                        .expect("Line could not be read. Please try again.");
                    match input.to_lowercase().trim() {
                        "1" | "one" => return one,
                        "11" | "eleven" => return eleven,
                        _ => {
                            println!("Please enter either one or eleven.");
                            wait();
                        }
                    }
                },
                // Ace selection for dealer
                2 => match player.score {
                    0..=10 => return eleven,
                    _ => return one,
                },
                _ => {
                    println!("An error occured.");
                    return 255;
                }
            },
            PointValue::NotAce(x) => x,
        }
    }
}

#[derive(Clone)]
struct Card {
    name: String,
    suit: String,
    point_value: PointValue,
}
fn build_deck() -> Vec<Card> {
    println!("Shuffling deck...");
    wait();
    // S P A D E S
    let ace_spades = Card {
        name: String::from("Ace"),
        suit: String::from("Spades"),
        point_value: PointValue::Ace(1, 11),
    };
    let two_spades = Card {
        name: String::from("Two"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(2),
    };
    let three_spades = Card {
        name: String::from("Three"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(3),
    };
    let four_spades = Card {
        name: String::from("Four"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(4),
    };
    let five_spades = Card {
        name: String::from("Five"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(5),
    };
    let six_spades = Card {
        name: String::from("Six"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(6),
    };
    let seven_spades = Card {
        name: String::from("Seven"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(7),
    };
    let eight_spades = Card {
        name: String::from("Eight"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(8),
    };
    let nine_spades = Card {
        name: String::from("Nine"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(9),
    };
    let ten_spades = Card {
        name: String::from("Ten"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(10),
    };
    let jack_spades = Card {
        name: String::from("Jack"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(10),
    };
    let queen_spades = Card {
        name: String::from("Queen"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(10),
    };
    let king_spades = Card {
        name: String::from("King"),
        suit: String::from("Spades"),
        point_value: PointValue::NotAce(10),
    };
    // D I A M O N D S
    let ace_diamonds = Card {
        name: String::from("Ace"),
        suit: String::from("Diamonds"),
        point_value: PointValue::Ace(1, 11),
    };
    let two_diamonds = Card {
        name: String::from("Two"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(2),
    };
    let three_diamonds = Card {
        name: String::from("Three"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(3),
    };
    let four_diamonds = Card {
        name: String::from("Four"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(4),
    };
    let five_diamonds = Card {
        name: String::from("Five"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(5),
    };
    let six_diamonds = Card {
        name: String::from("Six"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(6),
    };
    let seven_diamonds = Card {
        name: String::from("Seven"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(7),
    };
    let eight_diamonds = Card {
        name: String::from("Eight"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(8),
    };
    let nine_diamonds = Card {
        name: String::from("Nine"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(9),
    };
    let ten_diamonds = Card {
        name: String::from("Ten"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(10),
    };
    let jack_diamonds = Card {
        name: String::from("Jack"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(10),
    };
    let queen_diamonds = Card {
        name: String::from("Queen"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(10),
    };
    let king_diamonds = Card {
        name: String::from("King"),
        suit: String::from("Diamonds"),
        point_value: PointValue::NotAce(10),
    };
    // C L U B S
    let ace_clubs = Card {
        name: String::from("Ace"),
        suit: String::from("Clubs"),
        point_value: PointValue::Ace(1, 11),
    };
    let two_clubs = Card {
        name: String::from("Two"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(2),
    };
    let three_clubs = Card {
        name: String::from("Three"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(3),
    };
    let four_clubs = Card {
        name: String::from("Four"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(4),
    };
    let five_clubs = Card {
        name: String::from("Five"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(5),
    };
    let six_clubs = Card {
        name: String::from("Six"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(6),
    };
    let seven_clubs = Card {
        name: String::from("Seven"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(7),
    };
    let eight_clubs = Card {
        name: String::from("Eight"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(8),
    };
    let nine_clubs = Card {
        name: String::from("Nine"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(9),
    };
    let ten_clubs = Card {
        name: String::from("Ten"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(10),
    };
    let jack_clubs = Card {
        name: String::from("Jack"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(10),
    };
    let queen_clubs = Card {
        name: String::from("Queen"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(10),
    };
    let king_clubs = Card {
        name: String::from("King"),
        suit: String::from("Clubs"),
        point_value: PointValue::NotAce(10),
    };
    // H E A R T S
    let ace_hearts = Card {
        name: String::from("Ace"),
        suit: String::from("Hearts"),
        point_value: PointValue::Ace(1, 11),
    };
    let two_hearts = Card {
        name: String::from("Two"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(2),
    };
    let three_hearts = Card {
        name: String::from("Three"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(3),
    };
    let four_hearts = Card {
        name: String::from("Four"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(4),
    };
    let five_hearts = Card {
        name: String::from("Five"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(5),
    };
    let six_hearts = Card {
        name: String::from("Six"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(6),
    };
    let seven_hearts = Card {
        name: String::from("Seven"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(7),
    };
    let eight_hearts = Card {
        name: String::from("Eight"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(8),
    };
    let nine_hearts = Card {
        name: String::from("Nine"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(9),
    };
    let ten_hearts = Card {
        name: String::from("Ten"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(10),
    };
    let jack_hearts = Card {
        name: String::from("Jack"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(10),
    };
    let queen_hearts = Card {
        name: String::from("Queen"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(10),
    };
    let king_hearts = Card {
        name: String::from("King"),
        suit: String::from("Hearts"),
        point_value: PointValue::NotAce(10),
    };
    let deck = vec![
        ace_spades,
        two_spades,
        three_spades,
        four_spades,
        five_spades,
        six_spades,
        seven_spades,
        eight_spades,
        nine_spades,
        ten_spades,
        jack_spades,
        queen_spades,
        king_spades,
        ace_diamonds,
        two_diamonds,
        three_diamonds,
        four_diamonds,
        five_diamonds,
        six_diamonds,
        seven_diamonds,
        eight_diamonds,
        nine_diamonds,
        ten_diamonds,
        jack_diamonds,
        queen_diamonds,
        king_diamonds,
        ace_clubs,
        two_clubs,
        three_clubs,
        four_clubs,
        five_clubs,
        six_clubs,
        seven_clubs,
        eight_clubs,
        nine_clubs,
        ten_clubs,
        jack_clubs,
        queen_clubs,
        king_clubs,
        ace_hearts,
        two_hearts,
        three_hearts,
        four_hearts,
        five_hearts,
        six_hearts,
        seven_hearts,
        eight_hearts,
        nine_hearts,
        ten_hearts,
        jack_hearts,
        queen_hearts,
        king_hearts,
    ];
    return deck;
}

// Generic Functions
fn draw_card(deck: &mut Vec<Card>) -> Card {
    let mut rng = rand::thread_rng();
    let draw_number = rng.gen_range(0..deck.len());
    let drawn_card = deck[draw_number].clone();
    deck.remove(draw_number);
    return drawn_card;
}

fn continue_game(player: &mut Player) -> bool {
    match player.chips {
        // Buy back in if out of chips
        0 => loop {
            let mut input = String::new();
            print!("Buy back in? [Yes/No] ");
            let _ = io::stdout().flush();
            io::stdin()
                .read_line(&mut input)
                .expect("Error reading line, please try again.");
            match input.to_lowercase().trim() {
                "yes" | "y" => {
                    player.chips += 100;
                    return true;
                }
                "no" | "n" => return false,
                _ => {
                    println!("Invalid input, please try again.");
                    wait();
                }
            }
        },
        // Standard continue loop
        _ => loop {
            let mut input = String::new();
            print!("Play another hand? [Yes/No] ");
            let _ = io::stdout().flush();
            io::stdin()
                .read_line(&mut input)
                .expect("Error reading line, please try again.");
            match input.to_lowercase().trim() {
                "yes" | "y" => return true,
                "no" | "n" => return false,
                _ => {
                    println!("Invalid input, please try again.");
                    wait();
                }
            }
        },
    }
}
fn header(heading: String) {
    let mut divider = String::new();
    for _n in 1..=(heading.len() + 8) {
        divider += "=";
    }
    println!("");
    println!("{}", divider);
    println!("||  {}  ||", heading);
    println!("{}", divider);
    wait();
}
fn view_stats(player: &mut Player) {
    loop {
        let mut input = String::new();
        print!("View stats? [Yes/No] ");
        let _ = io::stdout().flush();
        io::stdin()
            .read_line(&mut input)
            .expect("Error reading line, please try again.");
        match input.to_lowercase().trim() {
            "yes" | "y" => {
                header(String::from("Session Stats"));
                // Calc averages
                let win_rate =
                    (player.stats.wins as f32 / player.stats.games_played as f32) * 100.0;
                let draw_rate =
                    (player.stats.draws as f32 / player.stats.games_played as f32) * 100.0;
                let bust_rate =
                    (player.stats.busts as f32 / player.stats.games_played as f32) * 100.0;
                let net_change_rate =
                    player.stats.net_change as f32 / player.stats.games_played as f32;

                // Print stats
                match player.stats.games_played {
                    1 => {
                        match player.stats.wins {
                            1 => println!("You won the only game you played!"),
                            _ => match player.stats.draws {
                                1 => println!("You tied the only game you played."),
                                _ => println!("You lost the only game you played."),
                            },
                        }
                        wait();
                    }
                    _ => {
                        // Wins
                        match player.stats.wins {
                            0 => println!("You lost every game you played."),
                            1 => println!(
                                "You won once out of {} games, for a win rate of {:.2}%.",
                                player.stats.games_played, win_rate
                            ),
                            _ => println!(
                                "You won {} games, for a win rate of {:.2}%.",
                                player.stats.wins, win_rate
                            ),
                        }
                        wait();
                        // Draws
                        match player.stats.draws {
                            0 => (),
                            1 => {
                                println!(
                                    "You tied once out of {} games, for a draw rate of {:.2}%.",
                                    player.stats.games_played, draw_rate
                                );
                                wait()
                            }
                            _ => {
                                println!(
                                    "You tied {} games, for a draw rate of {:.2}%.",
                                    player.stats.draws, draw_rate
                                );
                                wait()
                            }
                        }
                        // Net change
                        println!(
                            "Your net change was ${}, for a rate of ${:.2} per game.",
                            player.stats.net_change, net_change_rate
                        );
                        wait();
                        // Busts
                        match player.stats.busts {
                            0 => (),
                            1 => {
                                println!(
                                    "You went bust once out of {} games, for a rate of {:.2}%.",
                                    player.stats.games_played, bust_rate
                                );
                                wait()
                            }
                            _ => {
                                println!(
                                    "You went bust {} times, for a rate of {:.2}%",
                                    player.stats.busts, bust_rate
                                );
                                wait()
                            }
                        }
                        // Double Down
                        match player.stats.double_down {
                            0 => (),
                            1 => {
                                println!("You doubled down once.");
                                wait()
                            }
                            _ => {
                                println!("You doubled down {} times.", player.stats.double_down);
                                wait()
                            }
                        }
                        // All in
                        match player.stats.all_in {
                            0 => (),
                            1 => {
                                println!("You went all in once.");
                                wait()
                            }
                            _ => {
                                println!("You went all in {} times.", player.stats.all_in);
                                wait()
                            }
                        }
                        //
                    }
                }
                break;
            }
            "no" | "n" => {
                break;
            }
            _ => {
                println!("Invalid input, please try again.");
                wait();
            }
        }
    }
    println!("Thanks for playing! Your end total is ${}!", player.chips);
}
fn wait() {
    thread::sleep(Duration::from_secs(1));
}

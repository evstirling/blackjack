use rand::Rng;
use std::io;
use std::io::Write;

fn main() {
    let mut player = Player {
        id: 1,
        score: 0,
        bet: 0,
        chips: 100,
        bust: false,
        turn: false,
        double_down: false,
        drawn_cards: Vec::new(),
    };
    let mut dealer = Player {
        id: 2,
        score: 0,
        bet: 0,
        chips: 0,
        bust: false,
        turn: false,
        double_down: false,
        drawn_cards: Vec::new(),
    };
    loop {
        let mut deck = build_deck();
        player.turn(&mut deck, &mut dealer);
        if player.bust == false || player.drawn_cards.len() < 5 {
            dealer.dealer_turn(&mut deck);
        }
        player.compare_scores(&dealer);
        player.reset();
        dealer.reset();
    }
}
// Player creation and functions
struct Player {
    id: u8,
    score: u8,
    bet: i32,
    chips: i32,
    bust: bool,
    turn: bool,
    double_down: bool,
    drawn_cards: Vec<Card>,
}
impl Player {
    fn compare_scores(&mut self, dealer: &Player) {
        if self.score > dealer.score && self.bust == false
            || dealer.bust == true
            || self.drawn_cards.len() == 5
        {
            println!("Congrats, you win!");
            self.chips += self.bet;
        } else if self.score < dealer.score && dealer.bust == false
            || self.bust == true
            || dealer.drawn_cards.len() == 5
        {
            println!("You lose. Better luck next time.");
            self.chips -= self.bet;
        } else if self.score == dealer.score && self.bust == false && dealer.bust == false {
            println!("Draw. Bets returned.");
        } else {
            println!("Error calculating winner. Bets returned.")
        }
    }
    fn hit(&mut self, deck: &mut Vec<Card>) {
        // Draw card, save to cards_drawn
        let drawn_card = draw_card(deck);
        let save_card = drawn_card.clone();
        self.drawn_cards.push(save_card);

        // Print drawn card
        match self.id {
            1 => {
                if self.drawn_cards.len() >= 1 {
                    println!("You drew the {} of {}.", drawn_card.name, drawn_card.suit);
                }
            }
            2 => match self.drawn_cards.len() {
                1 => {
                    println!(
                        "The dealer's face up card is the {} of {}.",
                        drawn_card.name, drawn_card.suit
                    );
                }
                _ => {
                    println!(
                        "The dealer drew the {} of {}.",
                        drawn_card.name, drawn_card.suit
                    );
                }
            },
            _ => {
                println!("An unexpected error occured :(");
            }
        }

        // Ace selection and point tally
        match drawn_card.point_value {
            PointValue::Ace(x, y) => match self.id {
                1 => loop {
                    let mut input = String::new();
                    print!("Count this ace as one or eleven? ");
                    let _ = io::stdout().flush();
                    io::stdin()
                        .read_line(&mut input)
                        .expect("Line could not be read. Please try again.");
                    match input.to_lowercase().trim() {
                        "1" | "one" => {
                            self.score += x;
                            break;
                        }
                        "11" | "eleven" => {
                            self.score += y;
                            break;
                        }
                        _ => {
                            println!("Please enter either one or eleven.")
                        }
                    }
                },
                2 => match self.score {
                    0..=10 => self.score += y,
                    _ => self.score += x,
                },
                _ => {
                    println!("An unexpected error occured :(");
                }
            },
            PointValue::NotAce(_x) => self.score += drawn_card.point_value.unpack(),
        }

        // Print point total and cards drawn
        match self.id {
            1 => {
                println!(
                    "You have {} cards worth {} points.",
                    self.drawn_cards.len(),
                    self.score
                )
            }
            2 => {
                if self.drawn_cards.len() < 1 {
                    println!(
                        "The dealer has {} cards worth {} points.",
                        self.drawn_cards.len(),
                        self.score
                    )
                }
            }
            _ => {
                println!("An unexpected error occured :(");
            }
        }
    }

    fn take_bets(&mut self) {
        println!("You have ${}.", self.chips);
        loop {
            let mut input = String::new();
            print!("Place your bets: $");
            let _ = io::stdout().flush();
            io::stdin()
                .read_line(&mut input)
                .expect("Please enter a valid number.");
            let val_input = input.trim().parse::<i32>();
            match val_input {
                Ok(val_input) => {
                    if self.chips < val_input {
                        println!("Insufficient funds.");
                    } else {
                        println!("Bets placed!");
                        self.bet = val_input;
                        break;
                    }
                }
                Err(_e) => {
                    println!("Please enter a valid number.");
                }
            }
        }
    }

    fn turn(&mut self, deck: &mut Vec<Card>, dealer: &mut Player) {
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
                break;
            }
            // Check double down
            if self.double_down == true {
                self.bet += self.bet;
                println!("Bet increased to ${}", self.bet);
                self.hit(deck);
                break;
            }
            // Check 5 card draw
            if self.drawn_cards.len() >= 5 {
                println!("You have five cards!");
                break;
            }
            // Take action
            let mut input = String::new();
            if self.drawn_cards.len() == 2 {
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
                    break;
                }
                "dd" | "double down" => {
                    if self.drawn_cards.len() == 2 {
                        self.double_down = true;
                    } else {
                        println!("You can only double down on your first turn of the game.")
                    }
                }
                _ => {
                    println!("Please enter a valid input.")
                }
            }
        }
        self.turn = false;
    }
    fn dealer_turn(&mut self, deck: &mut Vec<Card>) {
        self.turn = true;
        loop {
            // Check bust
            if self.score > 21 {
                println!("The dealer has bust.");
                self.bust = true;
                break;
            }
            // Check 5 card draw
            if self.drawn_cards.len() >= 5 {
                println!("The dealer has five cards.");
                break;
            }
            // Hit or stick
            if self.score >= 17 {
                println!("Dealer sticks.");
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
    fn unpack(&self) -> u8 {
        match *self {
            PointValue::NotAce(x) => x,
            _ => 255,
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

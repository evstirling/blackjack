use blackjack::*;

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
    intro();
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

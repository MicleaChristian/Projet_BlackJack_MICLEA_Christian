# Texas Hold'em Poker Hand Evaluator

TDD project: evaluate and compare Texas Hold'em hands. No betting logic.

## Card notation

- **Rank:** `2`-`9`, `T` (10), `J`, `Q`, `K`, `A`
- **Suit:** `c` (clubs), `d` (diamonds), `h` (hearts), `s` (spades)

Examples: `As`, `10h`, `2d`, `Kc`

## Input validity

**Assumption:** No duplicate cards in input. Duplicates are not validated or rejected.

## API

```python
from poker import evaluate, parse_cards

board = parse_cards("5c", "6d", "7h", "8s", "9d")
players = [
    parse_cards("Ac", "Ad"),
    parse_cards("Kc", "Qd"),
]
result = evaluate(board, players)

print(result.winners)           # [0, 1] for tie
print(result.player_results[0].category)   # HandCategory.STRAIGHT
print(result.player_results[0].chosen5)    # Best 5 cards
```

## chosen5 ordering

The 5 chosen cards are returned in a consistent order for tie-break comparison:

| Category       | Order                                      |
|----------------|--------------------------------------------|
| Straight       | Highest to lowest in straight order        |
| Straight flush | Same as straight                           |
| Wheel (A-2-3-4-5) | 5, 4, 3, 2, A                          |
| Four of a kind | Four cards (quad rank), then kicker        |
| Full house     | Trips, then pair                           |
| Flush / High card | Descending ranks                        |
| Three of a kind | Triplet, then 2 kickers descending       |
| Two pair       | High pair, low pair, kicker                |
| One pair       | Pair, then 3 kickers descending            |

## Hand order (highest → lowest)

1. Straight flush  
2. Four of a kind  
3. Full house  
4. Flush  
5. Straight  
6. Three of a kind  
7. Two pair  
8. One pair  
9. High card  

## Examples from spec

- **Example A (wheel):** Board A♣2♦3♥4♠9♦, Player 5♣K♦ → Straight, 5-high
- **Example B (ace-high):** Board 10-J-Q-K-2, Player A-3 → Straight, A-high
- **Example C (flush):** Board A♥J♥9♥4♥2♣, Player 6♥K♦ → Flush A♥J♥9♥6♥4♥
- **Example D (board plays):** Board 5-6-7-8-9, both AA and KQ → tie, straight
- **Example E (quads):** Board 7s, Player1 A+K vs Player2 Q+J → Player1 wins (A kicker)

## Setup

```bash
pip install pytest
pytest tests/ -v
```

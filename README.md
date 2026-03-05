# Texas Hold'em Poker Hand Evaluator

TDD project: evaluate and compare Texas Hold'em hands.

## Card notation

- **Rank:** `2`-`9`, `T` (10), `J`, `Q`, `K`, `A`
- **Suit:** `c` (clubs), `d` (diamonds), `h` (hearts), `s` (spades)

Examples: `As`, `10h`, `2d`, `Kc`

## Input validity

**Assumption:** No duplicate cards in input.

## Setup

```bash
pip install pytest
pytest tests/ -v
```

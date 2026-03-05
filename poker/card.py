from enum import IntEnum
from typing import List

class Suit(IntEnum):
    

    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

class Rank(IntEnum):
    

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

RANK_CHARS = {
    "2": Rank.TWO,
    "3": Rank.THREE,
    "4": Rank.FOUR,
    "5": Rank.FIVE,
    "6": Rank.SIX,
    "7": Rank.SEVEN,
    "8": Rank.EIGHT,
    "9": Rank.NINE,
    "T": Rank.TEN,
    "J": Rank.JACK,
    "Q": Rank.QUEEN,
    "K": Rank.KING,
    "A": Rank.ACE,
}

SUIT_CHARS = {
    "c": Suit.CLUBS,
    "d": Suit.DIAMONDS,
    "h": Suit.HEARTS,
    "s": Suit.SPADES,
}

class Card:
    

    __slots__ = ("rank", "suit")

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))

    def __repr__(self) -> str:
        rank_str = {11: "J", 12: "Q", 13: "K", 14: "A"}.get(self.rank, str(self.rank))
        suit_str = {0: "c", 1: "d", 2: "h", 3: "s"}[self.suit]
        return f"Card({rank_str}{suit_str})"

def parse_card(s: str) -> Card:
    
    s = s.strip().lower()
    if len(s) < 2:
        raise ValueError(f"Invalid card: {s}")

    if s.startswith("10") and len(s) == 3:
        rank_char, suit_char = "T", s[2]
    elif len(s) == 2:
        rank_char, suit_char = s[0].upper(), s[1]
    else:
        raise ValueError(f"Invalid card: {s}")

    if rank_char not in RANK_CHARS:
        raise ValueError(f"Invalid rank: {rank_char}")
    if suit_char not in SUIT_CHARS:
        raise ValueError(f"Invalid suit: {suit_char}")

    return Card(RANK_CHARS[rank_char], SUIT_CHARS[suit_char])

def parse_cards(*strings: str) -> List[Card]:
    
    return [parse_card(s) for s in strings]

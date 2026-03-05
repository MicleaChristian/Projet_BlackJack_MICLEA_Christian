from enum import IntEnum
from typing import List, Tuple

from poker.card import Card, Rank

class HandCategory(IntEnum):
    

    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

def evaluate_hand(cards: List[Card]) -> Tuple[HandCategory, List[Card]]:
    
    if len(cards) != 7:
        raise ValueError("Need exactly 7 cards")
    return _eval_best(cards)

def _eval_best(cards: List[Card]) -> Tuple[HandCategory, List[Card]]:
    
    from itertools import combinations

    best_category = HandCategory.HIGH_CARD
    best_chosen: List[Card] = []
    best_rank_tuple: Tuple[int, ...] = ()

    for five in combinations(cards, 5):
        cat, chosen, rank_tuple = _eval_five(list(five))
        if cat > best_category or (cat == best_category and rank_tuple > best_rank_tuple):
            best_category = cat
            best_chosen = chosen
            best_rank_tuple = rank_tuple

    return best_category, best_chosen

def _eval_five(cards: List[Card]) -> Tuple[HandCategory, List[Card], Tuple[int, ...]]:
    
    if len(cards) != 5:
        raise ValueError("Need exactly 5 cards")

    pair = _find_pair(cards)
    if pair:
        cat, chosen, rt = _build_one_pair(cards, pair)
        return cat, chosen, rt

    return _build_high_card(cards)

def _find_pair(cards: List[Card]) -> List[Card] | None:
    
    by_rank: dict[int, List[Card]] = {}
    for c in cards:
        by_rank.setdefault(c.rank, []).append(c)
    for rank, group in sorted(by_rank.items(), key=lambda x: -x[0]):
        if len(group) >= 2:
            return group[:2]
    return None

def _build_one_pair(
    cards: List[Card], pair: List[Card]
) -> Tuple[HandCategory, List[Card], Tuple[int, ...]]:
    
    pair_rank = pair[0].rank
    kickers = sorted(
        [c for c in cards if c not in pair],
        key=lambda c: (-c.rank, -c.suit),
    )[:3]
    chosen = pair + kickers
    rank_tuple = (pair_rank, kickers[0].rank, kickers[1].rank, kickers[2].rank)
    return HandCategory.ONE_PAIR, chosen, rank_tuple

def _build_high_card(cards: List[Card]) -> Tuple[HandCategory, List[Card], Tuple[int, ...]]:
    
    chosen = sorted(cards, key=lambda c: (-c.rank, -c.suit))[:5]
    rank_tuple = tuple(c.rank for c in chosen)
    return HandCategory.HIGH_CARD, chosen, rank_tuple

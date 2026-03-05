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

    straight = _find_straight(cards)
    if straight:
        return _build_straight(cards, straight)

    trips = _find_trips(cards)
    if trips:
        return _build_three_of_a_kind(cards, trips)

    two_pair = _find_two_pair(cards)
    if two_pair:
        return _build_two_pair(cards, two_pair)

    pair = _find_pair(cards)
    if pair:
        return _build_one_pair(cards, pair)

    return _build_high_card(cards)

def _find_straight(cards: List[Card]) -> int | None:
    
    ranks = sorted(set(c.rank for c in cards), reverse=True)
    if len(ranks) != 5:
        return None

    wheel = {14, 2, 3, 4, 5}
    if set(ranks) == wheel:
        return 5

    for high in [14, 13, 12, 11, 10, 9, 8, 7, 6]:
        run = set(range(high, high - 5, -1))
        if set(ranks) == run:
            return high
    return None

def _build_straight(
    cards: List[Card], high_rank: int
) -> Tuple[HandCategory, List[Card], Tuple[int, ...]]:
    
    if high_rank == 5:
        ordered_ranks = [5, 4, 3, 2, 14]
    else:
        ordered_ranks = list(range(high_rank, high_rank - 5, -1))

    by_rank = {c.rank: c for c in cards}
    chosen = [by_rank[r] for r in ordered_ranks]
    return HandCategory.STRAIGHT, chosen, (high_rank,)

def _find_trips(cards: List[Card]) -> List[Card] | None:
    
    by_rank: dict[int, List[Card]] = {}
    for c in cards:
        by_rank.setdefault(c.rank, []).append(c)
    for rank, group in sorted(by_rank.items(), key=lambda x: -x[0]):
        if len(group) >= 3:
            return group[:3]
    return None

def _find_two_pair(cards: List[Card]) -> Tuple[List[Card], List[Card]] | None:
    
    by_rank: dict[int, List[Card]] = {}
    for c in cards:
        by_rank.setdefault(c.rank, []).append(c)
    pairs = [(r, g[:2]) for r, g in sorted(by_rank.items(), key=lambda x: -x[0]) if len(g) >= 2]
    if len(pairs) >= 2:
        return pairs[0][1], pairs[1][1]
    return None

def _find_pair(cards: List[Card]) -> List[Card] | None:
    
    by_rank: dict[int, List[Card]] = {}
    for c in cards:
        by_rank.setdefault(c.rank, []).append(c)
    for rank, group in sorted(by_rank.items(), key=lambda x: -x[0]):
        if len(group) >= 2:
            return group[:2]
    return None

def _build_three_of_a_kind(
    cards: List[Card], trips: List[Card]
) -> Tuple[HandCategory, List[Card], Tuple[int, ...]]:
    
    trips_rank = trips[0].rank
    kickers = sorted(
        [c for c in cards if c not in trips],
        key=lambda c: (-c.rank, -c.suit),
    )[:2]
    chosen = trips + kickers
    rank_tuple = (trips_rank, kickers[0].rank, kickers[1].rank)
    return HandCategory.THREE_OF_A_KIND, chosen, rank_tuple

def _build_two_pair(
    cards: List[Card], two_pair: Tuple[List[Card], List[Card]]
) -> Tuple[HandCategory, List[Card], Tuple[int, ...]]:
    
    high_pair, low_pair = two_pair
    high_rank, low_rank = high_pair[0].rank, low_pair[0].rank
    kickers = [c for c in cards if c not in high_pair and c not in low_pair]
    kicker = sorted(kickers, key=lambda c: (-c.rank, -c.suit))[0]
    chosen = high_pair + low_pair + [kicker]
    rank_tuple = (high_rank, low_rank, kicker.rank)
    return HandCategory.TWO_PAIR, chosen, rank_tuple

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

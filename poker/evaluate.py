from dataclasses import dataclass
from typing import List

from poker.card import Card
from poker.hands import HandCategory, evaluate_hand, _eval_five

@dataclass
class PlayerResult:
    

    category: HandCategory
    chosen5: List[Card]

@dataclass
class EvaluationResult:
    

    winners: List[int]
    player_results: List[PlayerResult]

def evaluate(board: List[Card], players: List[List[Card]]) -> EvaluationResult:
    
    if len(board) != 5:
        raise ValueError("Board must have exactly 5 cards")
    for i, hole in enumerate(players):
        if len(hole) != 2:
            raise ValueError(f"Player {i} must have exactly 2 hole cards")

    player_results: List[PlayerResult] = []
    rank_tuples: List[tuple] = []

    for hole in players:
        cards = board + hole
        category, chosen5 = evaluate_hand(cards)
        _, _, rank_tuple = _eval_five(chosen5)
        player_results.append(PlayerResult(category=category, chosen5=chosen5))
        rank_tuples.append((category, rank_tuple))

    winners = _find_winners(rank_tuples)
    return EvaluationResult(winners=winners, player_results=player_results)

def _find_winners(rank_tuples: List[tuple]) -> List[int]:
    
    best = max(rank_tuples)
    return [i for i, rt in enumerate(rank_tuples) if rt == best]

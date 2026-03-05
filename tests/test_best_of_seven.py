from poker.card import parse_cards
from poker.hands import HandCategory, evaluate_hand

class TestBestOfSeven:
    def test_board_plays_when_board_is_best(self):
        """Example D: Board 5-6-7-8-9, Player1 AA, Player2 KQ -> both have same straight, board plays."""
        board = parse_cards("5c", "6d", "7h", "8s", "9d")
        hole1 = parse_cards("Ac", "Ad")
        hole2 = parse_cards("Kc", "Qd")
        cards1 = board + hole1
        cards2 = board + hole2
        cat1, chosen1 = evaluate_hand(cards1)
        cat2, chosen2 = evaluate_hand(cards2)
        assert cat1 == cat2 == HandCategory.STRAIGHT
        assert [c.rank for c in chosen1] == [c.rank for c in chosen2] == [9, 8, 7, 6, 5]

    def test_one_hole_card_used_when_beneficial(self):
        """Pair on board + one hole card for trips."""
        board = parse_cards("As", "Ad", "Kh", "10d", "2c")
        hole = parse_cards("Ah", "5s")
        cards = board + hole
        category, chosen = evaluate_hand(cards)
        assert category == HandCategory.THREE_OF_A_KIND
        assert chosen[0].rank == chosen[1].rank == chosen[2].rank == 14

    def test_both_hole_cards_used_when_best(self):
        """Standard case: pair in hole beats high card from board (no wheel/straight)."""
        board = parse_cards("2s", "3d", "4h", "6c", "7d")
        hole = parse_cards("As", "Ad")
        cards = board + hole
        category, chosen = evaluate_hand(cards)
        assert category == HandCategory.ONE_PAIR
        assert chosen[0].rank == chosen[1].rank == 14

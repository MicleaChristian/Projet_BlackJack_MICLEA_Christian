import pytest

from poker.card import Card, Rank, Suit, parse_cards
from poker.hands import HandCategory, evaluate_hand

class TestHighCard:
    def test_high_card_is_default_category(self):
        cards = parse_cards("As", "Kh", "10d", "2c", "5s", "7h", "3d")
        category, chosen = evaluate_hand(cards)
        assert category == HandCategory.HIGH_CARD
        assert len(chosen) == 5

    def test_high_card_chosen5_descending_ranks(self):
        cards = parse_cards("As", "Kh", "10d", "2c", "5s", "7h", "3d")
        _, chosen = evaluate_hand(cards)
        ranks = [c.rank for c in chosen]
        assert ranks == [Rank.ACE, Rank.KING, Rank.TEN, Rank.SEVEN, Rank.FIVE]

    def test_high_card_tie_break_by_descending_ranks(self):
        cards1 = parse_cards("As", "Kh", "10d", "6c", "4s", "3h", "2d")
        cards2 = parse_cards("As", "Kh", "10d", "6c", "5s", "3h", "2d")
        _, chosen1 = evaluate_hand(cards1)
        _, chosen2 = evaluate_hand(cards2)
        assert chosen1[4].rank == Rank.FOUR
        assert chosen2[4].rank == Rank.FIVE

class TestOnePair:
    def test_detect_one_pair(self):
        cards = parse_cards("As", "Ad", "Kh", "10d", "2c", "5s", "7h")
        category, _ = evaluate_hand(cards)
        assert category == HandCategory.ONE_PAIR

    def test_one_pair_chosen5_pair_first_then_kickers(self):
        cards = parse_cards("As", "Ad", "Kh", "10d", "2c", "5s", "7h")
        _, chosen = evaluate_hand(cards)
        assert chosen[0].rank == Rank.ACE and chosen[1].rank == Rank.ACE
        assert [c.rank for c in chosen[2:]] == [Rank.KING, Rank.TEN, Rank.SEVEN]

    def test_one_pair_tie_break_pair_rank_then_kickers(self):
        cards1 = parse_cards("As", "Ad", "Kh", "10d", "2c", "5s", "7h")
        cards2 = parse_cards("Ks", "Kd", "Ah", "10d", "2c", "5s", "7h")
        cat1, chosen1 = evaluate_hand(cards1)
        cat2, chosen2 = evaluate_hand(cards2)
        assert cat1 == cat2 == HandCategory.ONE_PAIR
        assert chosen1[0].rank == Rank.ACE and chosen2[0].rank == Rank.KING

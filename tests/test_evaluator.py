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

class TestTwoPair:
    def test_detect_two_pair(self):
        cards = parse_cards("As", "Ad", "Kh", "Kd", "10c", "5s", "7h")
        category, _ = evaluate_hand(cards)
        assert category == HandCategory.TWO_PAIR

    def test_two_pair_chosen5_high_pair_low_pair_kicker(self):
        cards = parse_cards("As", "Ad", "Kh", "Kd", "10c", "5s", "7h")
        _, chosen = evaluate_hand(cards)
        assert chosen[0].rank == Rank.ACE and chosen[1].rank == Rank.ACE
        assert chosen[2].rank == Rank.KING and chosen[3].rank == Rank.KING
        assert chosen[4].rank == Rank.TEN

    def test_two_pair_tie_break_high_pair_then_low_pair_then_kicker(self):
        cards1 = parse_cards("As", "Ad", "Kh", "Kd", "10c", "5s", "7h")
        cards2 = parse_cards("As", "Ad", "Kh", "Kd", "Jc", "5s", "7h")
        _, chosen1 = evaluate_hand(cards1)
        _, chosen2 = evaluate_hand(cards2)
        assert chosen1[4].rank == Rank.TEN
        assert chosen2[4].rank == Rank.JACK

class TestThreeOfAKind:
    def test_detect_three_of_a_kind(self):
        cards = parse_cards("As", "Ad", "Ah", "Kd", "10c", "5s", "7h")
        category, _ = evaluate_hand(cards)
        assert category == HandCategory.THREE_OF_A_KIND

    def test_three_of_a_kind_chosen5_triplet_then_kickers(self):
        cards = parse_cards("As", "Ad", "Ah", "Kd", "10c", "5s", "7h")
        _, chosen = evaluate_hand(cards)
        assert chosen[0].rank == chosen[1].rank == chosen[2].rank == Rank.ACE
        assert [c.rank for c in chosen[3:]] == [Rank.KING, Rank.TEN]

    def test_three_of_a_kind_tie_break_triplet_then_kickers(self):
        cards1 = parse_cards("As", "Ad", "Ah", "Kd", "10c", "5s", "7h")
        cards2 = parse_cards("Ks", "Kd", "Kh", "Ad", "10c", "5s", "7h")
        cat1, chosen1 = evaluate_hand(cards1)
        cat2, chosen2 = evaluate_hand(cards2)
        assert cat1 == cat2 == HandCategory.THREE_OF_A_KIND
        assert chosen1[0].rank == Rank.ACE and chosen2[0].rank == Rank.KING

class TestStraight:
    def test_detect_basic_straight(self):
        cards = parse_cards("5s", "6h", "7d", "8c", "9s", "2h", "3d")
        category, _ = evaluate_hand(cards)
        assert category == HandCategory.STRAIGHT

    def test_wheel_ace_low_straight(self):
        """Example A: Board A♣2♦3♥4♠9♦, Player 5♣K♦ -> 5-high straight."""
        board = parse_cards("Ac", "2d", "3h", "4s", "9d")
        hole = parse_cards("5c", "Kd")
        cards = board + hole
        category, chosen = evaluate_hand(cards)
        assert category == HandCategory.STRAIGHT
        assert [c.rank for c in chosen] == [5, 4, 3, 2, 14]

    def test_ace_high_straight(self):
        """Example B: Board 10-J-Q-K-2, Player A-3 -> A-high straight."""
        board = parse_cards("10c", "Jd", "Qh", "Ks", "2d")
        hole = parse_cards("Ac", "3d")
        cards = board + hole
        category, chosen = evaluate_hand(cards)
        assert category == HandCategory.STRAIGHT
        assert [c.rank for c in chosen] == [14, 13, 12, 11, 10]

    def test_no_wrap_around_invalid(self):
        """Q-K-A-2-3 is not a valid straight. Only wheel and normal straights."""
        cards = parse_cards("Qs", "Kh", "Ad", "2c", "3s", "7h", "8d")
        category, chosen = evaluate_hand(cards)
        assert category != HandCategory.STRAIGHT

    def test_straight_tie_break_by_highest_card(self):
        cards1 = parse_cards("5s", "6h", "7d", "8c", "9s", "2h", "3d")
        cards2 = parse_cards("6s", "7h", "8d", "9c", "10s", "2h", "3d")
        _, chosen1 = evaluate_hand(cards1)
        _, chosen2 = evaluate_hand(cards2)
        assert chosen1[0].rank == Rank.NINE
        assert chosen2[0].rank == Rank.TEN

class TestFlush:
    def test_detect_flush(self):
        cards = parse_cards("Ah", "Jh", "9h", "6h", "4h", "2c", "Kd")
        category, _ = evaluate_hand(cards)
        assert category == HandCategory.FLUSH

    def test_flush_with_6_suited_picks_best_5(self):
        """Example C: Board A♥J♥9♥4♥2♣, Player 6♥K♦ -> best 5 hearts: A,J,9,6,4."""
        board = parse_cards("Ah", "Jh", "9h", "4h", "2c")
        hole = parse_cards("6h", "Kd")
        cards = board + hole
        _, chosen = evaluate_hand(cards)
        assert [c.rank for c in chosen] == [14, 11, 9, 6, 4]

    def test_flush_tie_break_by_descending_ranks(self):
        cards1 = parse_cards("Ah", "Jh", "9h", "6h", "4h", "2c", "Kd")
        cards2 = parse_cards("Ah", "Jh", "9h", "6h", "5h", "2c", "Kd")
        _, chosen1 = evaluate_hand(cards1)
        _, chosen2 = evaluate_hand(cards2)
        assert chosen1[4].rank == Rank.FOUR
        assert chosen2[4].rank == Rank.FIVE

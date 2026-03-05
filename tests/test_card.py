import pytest

from poker.card import Card, Rank, Suit, parse_card, parse_cards

class TestCardCreation:
    def test_card_has_rank_and_suit(self):
        card = Card(Rank.ACE, Suit.SPADES)
        assert card.rank == Rank.ACE
        assert card.suit == Suit.SPADES

    def test_card_equality(self):
        c1 = Card(Rank.KING, Suit.HEARTS)
        c2 = Card(Rank.KING, Suit.HEARTS)
        c3 = Card(Rank.KING, Suit.CLUBS)
        assert c1 == c2
        assert c1 != c3

    def test_card_hashable(self):
        card = Card(Rank.TWO, Suit.DIAMONDS)
        assert hash(card) == hash((Rank.TWO, Suit.DIAMONDS))

class TestParseCard:
    def test_parse_ace_spades(self):
        assert parse_card("As") == Card(Rank.ACE, Suit.SPADES)

    def test_parse_ten_hearts(self):
        assert parse_card("10h") == Card(Rank.TEN, Suit.HEARTS)

    def test_parse_two_diamonds(self):
        assert parse_card("2d") == Card(Rank.TWO, Suit.DIAMONDS)

    def test_parse_king_clubs(self):
        assert parse_card("Kc") == Card(Rank.KING, Suit.CLUBS)

    def test_parse_case_insensitive(self):
        assert parse_card("as") == parse_card("As")
        assert parse_card("10H") == Card(Rank.TEN, Suit.HEARTS)

    def test_parse_invalid_rank_raises(self):
        with pytest.raises(ValueError, match="Invalid"):
            parse_card("1s")

    def test_parse_invalid_suit_raises(self):
        with pytest.raises(ValueError, match="Invalid"):
            parse_card("Ax")

class TestParseCards:
    def test_parse_multiple_cards(self):
        cards = parse_cards("As", "Kh", "10d", "2c")
        assert cards == [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.TWO, Suit.CLUBS),
        ]

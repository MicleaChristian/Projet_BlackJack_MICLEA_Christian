from poker.card import parse_cards
from poker.evaluate import evaluate
from poker.hands import HandCategory

class TestEvaluate:
    def test_single_winner(self):
        board = parse_cards("2s", "3d", "4h", "6c", "7d")
        players = [
            parse_cards("As", "Ad"),
            parse_cards("Kh", "Kd"),
        ]
        result = evaluate(board, players)
        assert result.winners == [0]
        assert result.player_results[0].category == HandCategory.ONE_PAIR
        assert result.player_results[1].category == HandCategory.ONE_PAIR

    def test_tie_returns_all_winners(self):
        """Example D: Board plays, both have same straight -> split."""
        board = parse_cards("5c", "6d", "7h", "8s", "9d")
        players = [
            parse_cards("Ac", "Ad"),
            parse_cards("Kc", "Qd"),
        ]
        result = evaluate(board, players)
        assert set(result.winners) == {0, 1}
        assert result.player_results[0].category == HandCategory.STRAIGHT
        assert result.player_results[1].category == HandCategory.STRAIGHT
        assert [c.rank for c in result.player_results[0].chosen5] == [9, 8, 7, 6, 5]
        assert [c.rank for c in result.player_results[1].chosen5] == [9, 8, 7, 6, 5]

    def test_three_players_single_winner(self):
        board = parse_cards("7c", "7d", "7h", "7s", "2d")
        players = [
            parse_cards("Ac", "Kc"),
            parse_cards("Qc", "Jc"),
            parse_cards("10c", "9c"),
        ]
        result = evaluate(board, players)
        assert result.winners == [0]
        assert all(r.category == HandCategory.FOUR_OF_A_KIND for r in result.player_results)

    def test_per_player_chosen5_and_category(self):
        board = parse_cards("Ah", "Kh", "Qh", "Jh", "10h")
        players = [parse_cards("2c", "3d")]
        result = evaluate(board, players)
        assert result.winners == [0]
        assert result.player_results[0].category == HandCategory.STRAIGHT_FLUSH
        assert len(result.player_results[0].chosen5) == 5
        assert [c.rank for c in result.player_results[0].chosen5] == [14, 13, 12, 11, 10]

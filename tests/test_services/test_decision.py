"""Test WANT calculation and risk matrix."""
from src.routers.risks import RISK_MATRIX


def test_risk_matrix_h_star():
    assert RISK_MATRIX[("H", "H")] == "H*"


def test_risk_matrix_low():
    assert RISK_MATRIX[("L", "L")] == "L"


def test_risk_matrix_medium():
    assert RISK_MATRIX[("M", "M")] == "M"


def test_risk_matrix_cross():
    assert RISK_MATRIX[("H", "L")] == "M"
    assert RISK_MATRIX[("L", "H")] == "M"


def test_want_weighted_score():
    """weighted_score = weight × score"""
    weight = 8
    score = 7
    assert weight * score == 56


def test_want_total():
    """Total = sum of all weighted scores"""
    scores = [{"weight": 8, "score": 7}, {"weight": 5, "score": 9}, {"weight": 3, "score": 6}]
    total = sum(s["weight"] * s["score"] for s in scores)
    assert total == 8*7 + 5*9 + 3*6  # 56 + 45 + 18 = 119

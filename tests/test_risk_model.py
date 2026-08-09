from ml.risk_model import RiskFeatures, heuristic_risk_score


def test_high_deviation_scores_higher_risk():
    low = heuristic_risk_score(RiskFeatures(2, 4, 100))
    high = heuristic_risk_score(RiskFeatures(90, 1, 1000))
    assert high > low
    assert 0 <= high <= 1

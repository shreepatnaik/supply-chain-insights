import pytest
from core.verify import check_proposal

SCORES = {"naive": 4.3, "seasonal_naive": 4.2, "moving_average": 3.9, "ets": 4.0}
FORECAST = {"method": "ets", "forecast": [{"month": "2017-10", "units": 100}]}

def test_rejects_unknown_method():
    verdict, feedback = check_proposal("magic", None, SCORES, None)
    assert verdict == "reject"
    assert "not a valid method" in feedback


def test_approves_best_method():
    verdict, feedback = check_proposal("moving_average", FORECAST, SCORES, FORECAST)
    assert verdict == "approve"
    assert feedback == ""


def test_approves_method_within_tolerance():
    # naive is 0.4 above the best, inside the default 0.5
    verdict, _ = check_proposal("naive", FORECAST, SCORES, FORECAST)
    assert verdict == "approve"


def test_rejects_method_beyond_tolerance():
    # naive is 0.4 above the best, outside a 0.3 tolerance
    verdict, feedback = check_proposal("naive", FORECAST, SCORES, FORECAST, tolerance=0.3)
    assert verdict == "reject"
    assert "well above the best" in feedback


def test_rejects_mismatched_numbers():
    tampered = {"method": "ets", "forecast": [{"month": "2017-10", "units": 999}]}
    verdict, feedback = check_proposal("ets", tampered, SCORES, FORECAST)
    assert verdict == "reject"
    assert "don't match" in feedback
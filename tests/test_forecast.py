import pytest
import pandas as pd
from forecast import mape, seasonal_naive, moving_average, naive, ets

def test_mape_perfect_forecast_is_zero():
    assert mape(100, 100) == 0

def test_mape_is_relative_to_actual():
    assert mape(200, 180) == 10

def test_mape_averages_over_list():
    assert mape([100, 200], [90, 150]) == pytest.approx(17.5)

def test_seasonal_naive_repeats_last_year():
    history = pd.Series(range(1, 25))
    result = seasonal_naive(history, 3)
    assert list(result) == [13, 14, 15]

def test_moving_average_uses_last_window():
    history = pd.Series([10, 20, 30, 40, 50, 60])
    result = moving_average(history, 2)
    assert result == [50, 50]

def test_naive_repeats_last_value():
    history = pd.Series([10, 20, 30])
    assert list(naive(history, 3)) == [30, 30, 30]

def test_ets_returns_h_values():
    history = pd.Series(range(1, 37))
    assert len(ets(history, 3)) == 3
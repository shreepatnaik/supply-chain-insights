from forecast import mape

def test_mape_perfect_forecast_is_zero():
    assert mape(100, 100) == 0

def test_mape_is_relative_to_actual():
    assert mape(200, 180) == 10
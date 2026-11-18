import sys
from  pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.mcpserver import MCPServer
from core import  stats, forecast



mcp = MCPServer("supply-chain-insights")

@mcp.tool()
def late_by_shipping_mode() -> list[dict]:
    """Late delivery rate by shipping mode, from the orders table (canceled orders are excluded.)"""
    return stats.late_by_shipping_mode()

@mcp.tool()
def late_by_region() -> list[dict]:
    """Late delivery rate by order region, for shipped orders only (canceled orders excluded)."""
    return stats.late_by_region()

@mcp.tool()
def forecast_demand(method: str = "seasonal_naive", months: int = 3) -> dict:
    """Forecast monthly units for the next 1-12 months after Sep 2017.
    Methods: naive, seasonal_naive, moving_average, ets."""
    return forecast.forecast_next(method, months)


@mcp.tool()
def backtest_results() -> dict:
    """Average MAPE per method from a rolling backtest (3-month windows). Lower is better."""
    return forecast.backtest_summary()


if __name__ == "__main__":
    mcp.run()
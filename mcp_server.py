import pandas as pd
from mcp.server.mcpserver import MCPServer
from db import get_engine
import stats

mcp = MCPServer("supply-chain-insights")

@mcp.tool()
def late_by_shipping_mode() -> list[dict]:
    """Late delivery rate by shipping mode, from the orders table."""
    query = """
        SELECT shipping_mode,
               COUNT(*) AS items,
               ROUND(100.0 * AVG(late_delivery_risk::int), 1) AS late_pct
        FROM orders
        GROUP BY shipping_mode
        ORDER BY late_pct DESC;
    """
    return stats.late_by_shipping_mode()

if __name__ == "__main__":
    mcp.run()
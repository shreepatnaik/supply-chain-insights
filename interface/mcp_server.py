import pandas as pd
from mcp.server.mcpserver import MCPServer
import core.stats as stats
import core.forecast as forecast

mcp = MCPServer("supply-chain-insights")

@mcp.tool()
def late_by_shipping_mode() -> list[dict]:
    """Late delivery rate by shipping mode, from the orders table (canceled orders are excluded.)"""
    return stats.late_by_shipping_mode()

@mcp.tool()
def late_by_region() -> list[dict]:
    """Late delivery rate by order region, for shipped orders only (canceled orders excluded)."""
    return stats.late_by_region()




if __name__ == "__main__":
    mcp.run()
from mcp.server.mcpserver import MCPServer
import stats

mcp = MCPServer("supply-chain-insights")

@mcp.tool()
def late_by_shipping_mode() -> list[dict]:
    """Late delivery rate by shipping mode, from the orders table."""
    return stats.late_by_shipping_mode()

@mcp.tool()
def late_by_region() -> list[dict]:
    """Late delivery rate by order region, for shipped orders only (canceled orders excluded)."""
    return stats.late_by_region()

if __name__ == "__main__":
    mcp.run()
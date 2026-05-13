"""
01_market_data.py — Fetch public market data from Orderly.

This script requires NO authentication. It verifies that:
  1. The SDK is installed correctly
  2. You can reach Orderly's API
  3. You can identify which perp markets are tradable

Run this first to confirm your environment works before trying authenticated endpoints.
"""

import sys
import os

# Add parent directory to path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_client, describe_env


def main() -> None:
    print(f"Connecting to Orderly... {describe_env()}")
    print()

    # No auth needed for public endpoints
    client = get_client(require_auth=False)

    # --- Get available symbols ----------------------------------------
    print("Fetching available perp symbols...")
    info = client.get_exchange_info()

    if not info or "data" not in info:
        print("ERROR: unexpected response format")
        print(info)
        return

    rows = info["data"].get("rows", [])
    perps = [r for r in rows if r.get("symbol", "").startswith("PERP_")]

    print(f"Found {len(perps)} perp markets.\n")

    # Print a summary table of the top 10 by some criterion
    # (we don't have volume here, just listing first 10 alphabetically)
    print(f"{'Symbol':<25} {'Min Notional':>14} {'Tick Size':>12}")
    print("-" * 53)
    for row in sorted(perps, key=lambda r: r["symbol"])[:10]:
        symbol = row.get("symbol", "?")
        min_notional = row.get("min_notional", 0)
        tick = row.get("quote_tick", "?")
        print(f"{symbol:<25} {min_notional:>14} {tick:>12}")

    print()

    # --- Get ticker for BTC ------------------------------------------
    print("Fetching BTC perp ticker...")
    try:
        ticker = client.get_futures_for_one_market("PERP_BTC_USDC")
        data = ticker.get("data", {}) if ticker else {}
        if data:
            print(f"  Symbol:        {data.get('symbol')}")
            print(f"  Index price:   ${data.get('index_price')}")
            print(f"  Mark price:    ${data.get('mark_price')}")
            print(f"  Funding rate:  {data.get('est_funding_rate')}")
            print(f"  Open interest: {data.get('open_interest')}")
        else:
            print("  No ticker data returned")
    except Exception as e:
        print(f"  Could not fetch ticker: {e}")

    print()
    print("Done. If this worked, your environment is set up correctly.")
    print("Next: fill in your credentials in .env, then run 02_account_info.py")


if __name__ == "__main__":
    main()

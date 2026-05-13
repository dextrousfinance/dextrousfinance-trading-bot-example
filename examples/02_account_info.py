"""
02_account_info.py — Fetch your account balance, positions, and open orders.

Requires .env to be filled in with valid credentials.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_client, describe_env


def main() -> None:
    print(f"Connecting to Orderly... {describe_env()}")
    print()

    client = get_client(require_auth=True)

    # --- Balance ---------------------------------------------------------
    print("Account balance:")
    try:
        balance = client.get_current_holding()
        holdings = balance.get("data", {}).get("holding", []) if balance else []
        if holdings:
            for h in holdings:
                token = h.get("token", "?")
                amount = h.get("holding", 0)
                frozen = h.get("frozen", 0)
                print(f"  {token:<8} holding={amount}  frozen={frozen}")
        else:
            print("  (no holdings — deposit USDC at dextrous.finance to start trading)")
    except Exception as e:
        print(f"  ERROR: {e}")
    print()

    # --- Positions -------------------------------------------------------
    print("Open positions:")
    try:
        positions = client.get_all_positions_info()
        rows = positions.get("data", {}).get("rows", []) if positions else []
        if rows:
            for p in rows:
                symbol = p.get("symbol")
                size = p.get("position_qty", 0)
                entry = p.get("average_open_price", 0)
                pnl = p.get("unsettled_pnl", 0)
                print(f"  {symbol:<20} size={size:>10}  entry=${entry:>10}  uPnL=${pnl}")
        else:
            print("  (no open positions)")
    except Exception as e:
        print(f"  ERROR: {e}")
    print()

    # --- Open orders -----------------------------------------------------
    print("Open orders:")
    try:
        orders = client.get_orders(status="INCOMPLETE")
        rows = orders.get("data", {}).get("rows", []) if orders else []
        if rows:
            for o in rows:
                symbol = o.get("symbol")
                side = o.get("side")
                price = o.get("price")
                qty = o.get("quantity")
                order_id = o.get("order_id")
                print(f"  #{order_id} {symbol:<20} {side:<5} qty={qty} @ ${price}")
        else:
            print("  (no open orders)")
    except Exception as e:
        print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()

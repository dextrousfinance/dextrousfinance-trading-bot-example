"""
03_place_order.py — Place a single limit order.

By default this places a small BTC perp BUY order well below the current mark
price, so it will NOT fill immediately. You can then cancel it from the script
or from the dextrous.finance UI.

Edit SYMBOL, SIDE, PRICE_OFFSET_PCT, and QUANTITY below to match your needs.

Run with care. Even small orders consume gas and may fill if the market moves.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_client, describe_env


# --- Order parameters — EDIT THESE ---------------------------------------

SYMBOL = "PERP_BTC_USDC"        # which market
SIDE = "BUY"                    # BUY or SELL
QUANTITY = 0.001                # order size (in base token, e.g. 0.001 BTC)
PRICE_OFFSET_PCT = -5.0         # how far from mark price (% — negative = below for BUY)
ORDER_TYPE = "LIMIT"            # LIMIT, MARKET, etc.


def main() -> None:
    print(f"Connecting to Orderly... {describe_env()}")
    print()

    client = get_client(require_auth=True)

    # --- Get current mark price ------------------------------------------
    print(f"Fetching current price for {SYMBOL}...")
    try:
        ticker = client.get_futures_for_one_market(SYMBOL)
        mark = float(ticker["data"]["mark_price"])
        print(f"  Mark price: ${mark}")
    except Exception as e:
        print(f"  ERROR fetching ticker: {e}")
        return

    # --- Calculate order price -------------------------------------------
    order_price = round(mark * (1 + PRICE_OFFSET_PCT / 100), 2)
    print(f"  Placing {SIDE} {QUANTITY} {SYMBOL} @ ${order_price}")
    print(f"  ({PRICE_OFFSET_PCT:+}% from mark — should NOT fill immediately)")
    print()

    # --- Place order -----------------------------------------------------
    confirm = input("Type 'yes' to place this order: ").strip().lower()
    if confirm != "yes":
        print("Aborted.")
        return

    try:
        response = client.create_order(
            symbol=SYMBOL,
            order_type=ORDER_TYPE,
            side=SIDE,
            order_price=order_price,
            order_quantity=QUANTITY,
        )
        data = response.get("data", {}) if response else {}
        order_id = data.get("order_id")
        if order_id:
            print(f"  Order placed. ID: {order_id}")
            print(f"  Status: {data.get('status', 'unknown')}")
        else:
            print("  Unexpected response:")
            print(response)
            return
    except Exception as e:
        print(f"  ERROR placing order: {e}")
        return

    # --- Wait briefly, then show the order ------------------------------
    print()
    print("Waiting 3 seconds, then fetching order status...")
    time.sleep(3)

    try:
        check = client.get_order(order_id)
        print(check.get("data", {}))
    except Exception as e:
        print(f"  Could not refetch order: {e}")

    print()
    print(f"To cancel this order, run:")
    print(f"  python -c \"from config import get_client; "
          f"get_client().cancel_order(order_id={order_id}, symbol='{SYMBOL}')\"")
    print()
    print(f"Or cancel from dextrous.finance UI.")


if __name__ == "__main__":
    main()

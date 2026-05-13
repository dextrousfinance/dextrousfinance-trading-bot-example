"""
04_dca_bot.py — A simple Dollar-Cost-Averaging bot for perp positions.

Every INTERVAL_SECONDS, it places a small MARKET BUY for a target USDC notional.
Useful for:
  - Slowly building a long perp position over time
  - Generating consistent volume (for broker volume tier qualification)
  - Demonstrating a working scheduled trading loop

Configure the parameters below before running. Defaults are intentionally small.

Stop the bot with Ctrl+C.
"""

import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_client, describe_env


# --- DCA parameters — EDIT THESE -----------------------------------------

SYMBOL = "PERP_BTC_USDC"        # which market to DCA into
USDC_PER_TRADE = 5.0            # notional in USDC per buy (kept small for safety)
INTERVAL_SECONDS = 3600         # 1 hour between buys
MAX_TRADES = 24                 # safety cap — bot stops after this many buys

# Safety: only run on testnet by default. Set to True to allow mainnet.
ALLOW_MAINNET = False


def calculate_quantity(client, usdc_notional: float) -> float | None:
    """Convert a USDC notional into a base-token quantity using current mark price."""
    try:
        ticker = client.get_futures_for_one_market(SYMBOL)
        mark = float(ticker["data"]["mark_price"])
        qty = round(usdc_notional / mark, 6)
        return qty if qty > 0 else None
    except Exception as e:
        print(f"  Could not fetch price: {e}")
        return None


def place_market_buy(client, quantity: float):
    """Place a single market buy order."""
    return client.create_order(
        symbol=SYMBOL,
        order_type="MARKET",
        side="BUY",
        order_quantity=quantity,
    )


def main() -> None:
    from config import TESTNET

    print(f"DCA bot starting... {describe_env()}")
    print(f"  Symbol:       {SYMBOL}")
    print(f"  Per trade:    ${USDC_PER_TRADE} USDC")
    print(f"  Interval:     {INTERVAL_SECONDS}s ({INTERVAL_SECONDS / 60:.1f} min)")
    print(f"  Max trades:   {MAX_TRADES}")
    print()

    if not TESTNET and not ALLOW_MAINNET:
        print("SAFETY: ORDERLY_TESTNET=False but ALLOW_MAINNET=False in this script.")
        print("Set ALLOW_MAINNET=True in the script to run on mainnet with real funds.")
        return

    client = get_client(require_auth=True)

    trades_made = 0
    try:
        while trades_made < MAX_TRADES:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] Trade {trades_made + 1}/{MAX_TRADES}")

            qty = calculate_quantity(client, USDC_PER_TRADE)
            if qty is None:
                print("  Skipping this round — could not calculate quantity")
            else:
                print(f"  Buying {qty} {SYMBOL.split('_')[1]} (~${USDC_PER_TRADE})")
                try:
                    response = place_market_buy(client, qty)
                    data = response.get("data", {}) if response else {}
                    print(f"  Order: id={data.get('order_id')} status={data.get('status')}")
                    trades_made += 1
                except Exception as e:
                    print(f"  Order failed: {e}")

            if trades_made >= MAX_TRADES:
                break

            print(f"  Sleeping {INTERVAL_SECONDS}s until next trade...")
            print()
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print()
        print("Bot stopped by user.")

    print()
    print(f"Done. Trades placed: {trades_made}")


if __name__ == "__main__":
    main()

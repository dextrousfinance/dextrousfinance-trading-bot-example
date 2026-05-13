"""
config.py — Loads credentials from .env and provides a helper to instantiate
the Orderly REST client.

All examples import from this file so credentials are managed in one place.
"""

import os
from dotenv import load_dotenv
from orderly_evm_connector.rest import Rest as OrderlyClient

# Load environment variables from .env (if present)
load_dotenv()


# --- Credentials ---------------------------------------------------------

ACCOUNT_ID = os.getenv("ORDERLY_ACCOUNT_ID", "").strip()
ORDERLY_KEY = os.getenv("ORDERLY_KEY", "").strip()
ORDERLY_SECRET = os.getenv("ORDERLY_SECRET", "").strip()
TESTNET = os.getenv("ORDERLY_TESTNET", "True").strip().lower() in ("true", "1", "yes")
WSS_ID = os.getenv("WSS_ID", "dextrousfinance-bot").strip()

# --- Constants -----------------------------------------------------------

BROKER_ID = "dextrousfinance"
DISTRIBUTOR_CODE = "DEXTROUS"


# --- Helpers -------------------------------------------------------------

def get_client(require_auth: bool = True) -> OrderlyClient:
    """
    Return a configured Orderly REST client.

    If require_auth is True, validates that credentials are present.
    For public endpoints (market data), require_auth=False is fine.
    """
    if require_auth:
        missing = []
        if not ACCOUNT_ID or ACCOUNT_ID.startswith("0x_paste"):
            missing.append("ORDERLY_ACCOUNT_ID")
        if not ORDERLY_KEY or "paste_your_key" in ORDERLY_KEY:
            missing.append("ORDERLY_KEY")
        if not ORDERLY_SECRET or "paste_your_secret" in ORDERLY_SECRET:
            missing.append("ORDERLY_SECRET")
        if missing:
            raise RuntimeError(
                f"Missing credentials in .env: {', '.join(missing)}. "
                "See .env.example for setup instructions."
            )

    return OrderlyClient(
        orderly_key=ORDERLY_KEY or None,
        orderly_secret=ORDERLY_SECRET or None,
        orderly_account_id=ACCOUNT_ID or None,
        orderly_testnet=TESTNET,
        timeout=10,
    )


def describe_env() -> str:
    """Return a single-line description of the current env for logging."""
    network = "TESTNET" if TESTNET else "MAINNET"
    masked_id = (
        f"{ACCOUNT_ID[:6]}...{ACCOUNT_ID[-4:]}"
        if len(ACCOUNT_ID) > 12
        else "(not set)"
    )
    return f"[{network}] broker={BROKER_ID} account={masked_id}"

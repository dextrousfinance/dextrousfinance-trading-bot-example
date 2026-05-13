# Dextrous Finance — Trading Bot Example

A minimal, working Python example for algorithmic trading on **[Dextrous Finance](https://dextrous.finance)** — a permissionless perpetual DEX powered by [Orderly Network](https://orderly.network).

This repo is intended for builders, quant traders, and bot operators who want to integrate with Dextrous Finance via the Orderly Network API. Every order placed through an account registered with the `dextrousfinance` broker contributes to Dextrous Finance's volume and earns the account holder broker fee tier benefits.

---

## Why trade through Dextrous Finance?

- **Permissionless market listings** — list any market you want without team approval. No 500K HYPE stake required (Hyperliquid HIP-3). No $25M lockup.
- **Self-custody** — funds sit in Orderly's audited omnichain vault. Not in our custody.
- **No KYC** — connect a wallet, trade. That's it.
- **On-chain settlement** — every trade settles on-chain.
- **Deep shared liquidity** — Dextrous uses Orderly's omnichain orderbook, which aggregates liquidity across 30+ DEXs and 17 chains.
- **Tiered maker/taker fees** — standard Orderly broker fee tiers (see [docs/broker_program.md](docs/broker_program.md)).

---

## Quick start

### 1. Register a Dextrous Finance trading account

Before running this bot, you need an Orderly account registered with the `dextrousfinance` broker.

1. Visit https://dextrous.finance
2. Connect your wallet (MetaMask, WalletConnect, etc.)
3. Sign the registration message — this creates an Orderly account ID derived from your wallet address + the `dextrousfinance` broker ID
4. Generate an Orderly API key from inside the Dextrous Finance interface
5. Copy your **account ID**, **Orderly key**, and **Orderly secret**

These three values are what the bot uses to authenticate. Your wallet's private key is **not** required for trading — only for deposit/withdrawal.

### 2. Install

```bash
git clone https://github.com/dextrousfinance/dextrousfinance-trading-bot-example.git
cd dextrousfinance-trading-bot-example
pip install -r requirements.txt
```

Requires Python 3.9+.

### 3. Configure

```bash
cp .env.example .env
```

Edit `.env` and paste in your credentials from step 1:

```
ORDERLY_ACCOUNT_ID=0x...
ORDERLY_KEY=ed25519:...
ORDERLY_SECRET=ed25519:...
ORDERLY_TESTNET=False
```

Set `ORDERLY_TESTNET=True` while testing — you can register a testnet account at the [Orderly testnet](https://testnet-api-evm.orderly.org).

### 4. Run the examples

```bash
# Public market data (no auth needed) — verify your install works
python examples/01_market_data.py

# Fetch account balance and positions
python examples/02_account_info.py

# Place a single limit order
python examples/03_place_order.py

# Run a simple DCA bot
python examples/04_dca_bot.py
```

---

## Examples included

| File | What it does | Auth required |
|---|---|---|
| `01_market_data.py` | Fetch live markets, prices, funding rates | No |
| `02_account_info.py` | Show your balance, positions, open orders | Yes |
| `03_place_order.py` | Place a single limit order | Yes |
| `04_dca_bot.py` | DCA into a perp position on a schedule | Yes |

Each file is heavily commented. Start with `01_market_data.py` to verify your environment.

---

## Architecture

This bot uses the **official Orderly EVM Python SDK**:

```
orderly-evm-connector (PyPI)
└── github.com/OrderlyNetwork/orderly-evm-connector-python
```

The SDK handles:

- ed25519 request signing (Orderly's auth mechanism)
- Rate limit awareness
- WebSocket reconnection
- Both mainnet (`api-evm.orderly.org`) and testnet (`testnet-api-evm.orderly.org`)

You don't need to implement signing or auth yourself.

---

## Symbol naming

Orderly uses the format `PERP_<TOKEN>_USDC`:

- `PERP_BTC_USDC` — Bitcoin perpetual
- `PERP_ETH_USDC` — Ethereum perpetual
- `PERP_SOL_USDC` — Solana perpetual

The `01_market_data.py` example lists every currently-tradable symbol.

---

## Broker program

Read [docs/broker_program.md](docs/broker_program.md) for details on:

- What the `dextrousfinance` broker ID does
- Fee tiers and volume-based discounts
- Distributor code (`DEXTROUS`) — earn revenue share by referring traders
- How to verify your trades are being attributed correctly

---

## Trade attribution

Every order placed through an account registered with `broker_id=dextrousfinance` is attributed to Dextrous Finance for volume and fee purposes. This happens automatically based on your account ID — no special parameter on each order.

To verify, check the Orderly Indexer API endpoint `/get_broker_volume_statistic` with `broker_id=dextrousfinance` — you'll see the volume contributions from accounts registered under this broker.

---

## Safety notes

- **Start on testnet.** Set `ORDERLY_TESTNET=True` and test with worthless funds first.
- **Use small sizes when going live.** The example bots place small orders by default. Increase only when you've verified the logic.
- **Never commit `.env`.** The `.gitignore` excludes it. Confirm before pushing.
- **Don't share your Orderly secret.** Anyone with it can place orders from your account. Withdrawals still require your wallet signature, but trading does not.

---

## Contributing

PRs welcome. Open an issue first if it's a non-trivial change.

This is example code, not production-graded trading infrastructure. Use at your own risk.

---

## Links

- **Trade**: https://dextrous.finance
- **X / Twitter**: [@DextrousFinance](https://x.com/DextrousFinance)
- **Telegram**: https://t.me/DextrousFinance
- **Orderly docs**: https://orderly.network/docs
- **Orderly EVM API docs**: https://docs-api-evm.orderly.network
- **This repo**: github.com/dextrousfinance/dextrousfinance-trading-bot-example

---

## License

MIT — see [LICENSE](LICENSE).

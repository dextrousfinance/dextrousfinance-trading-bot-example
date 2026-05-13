# Dextrous Finance Broker Program

This doc explains how the `dextrousfinance` broker identifier and the `DEXTROUS` distributor code work, and how developers/affiliates can benefit.

---

## Two separate identifiers

Dextrous has two identifiers in the Orderly ecosystem. They serve different purposes.

### `dextrousfinance` — the broker ID

- Set at the protocol level when a trader registers an account on Orderly via the Dextrous Finance frontend
- Causes every trade from that account to be **attributed to Dextrous Finance for volume statistics**
- Account ID is derived deterministically: `keccak256(wallet_address, "dextrousfinance")`
- This ID cannot be changed for an existing account — it's baked into the account ID hash

### `DEXTROUS` — the distributor code

- A referral identifier used in URL parameters: `https://dextrous.finance/?distributor_code=DEXTROUS`
- When a new trader signs up after clicking a link with this code, they're **attributed as a referral for revenue share**
- Distinct from broker ID — distributor code can be set per-trader via URL
- Affiliates can ask Orderly to assign them their own distributor code if running a sub-distribution scheme

---

## Verifying trade attribution

You can query the Orderly Indexer API to verify volume attribution:

```bash
# Daily volume for the dextrousfinance broker
curl 'https://api-evm.orderly.org/v1/public/broker/info'
```

Or call `/get_broker_volume_statistic` from the Indexer API with `broker_id=dextrousfinance` to see volume statistics.

---

## Fee tiers

Orderly's default broker fee tiers (subject to change — verify against current Orderly docs before relying on these):

| Tier | 30-day Volume       | Maker Fee | Taker Fee |
|------|---------------------|-----------|-----------|
| 1    | $0 – $500K          | 0.030%    | 0.060%    |
| 2    | $500K – $2.5M       | 0.024%    | 0.054%    |
| 3    | $2.5M – $10M        | 0.018%    | 0.048%    |
| 4    | $10M – $100M        | 0.012%    | 0.042%    |
| 5    | $100M – $250M       | 0.006%    | 0.036%    |
| 6    | $250M+              | 0.000%    | 0.030%    |

Volume tier is computed per account. Higher volume = lower fees.

---

## Revenue share for affiliates

Specific revenue share percentages for distributors are negotiated with Orderly directly. See the [Distributor profile](https://dex.orderly.network/en/distributor) in the OrderlyOne portal for current attribution details.

---

## How to integrate Dextrous as a developer

1. **Build a trading bot** — use this repo as the starting point. Any account that registered via dextrous.finance will automatically have its volume attributed to the `dextrousfinance` broker.

2. **Embed Dextrous in your own site** — link to `https://dextrous.finance?distributor_code=DEXTROUS` (or your own distributor code if assigned) so signups are attributed to you for affiliate revenue.

3. **Use the Orderly API directly** — set up an account on dextrous.finance, generate API keys, build whatever automated trading or aggregation logic you want. Orderly's API is permissionless.

---

## Useful endpoints

- **REST API (mainnet)**: `https://api-evm.orderly.org`
- **REST API (testnet)**: `https://testnet-api-evm.orderly.org`
- **API docs**: https://docs-api-evm.orderly.network
- **Indexer API** (volume/ranking stats): see Orderly's Indexer docs

---

## Questions

- General: open an issue on this repo
- Trading-specific: ask on [Orderly Discord](https://discord.com/invite/OrderlyNetwork) — Orderly team monitors there
- Dextrous-specific: see https://dextrous.finance for contact info

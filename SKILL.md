---
name: bitget-mix-futures-mvp
description: Execute core Bitget Mix V2 USDT-M futures API operations from local Python scripts with authenticated signing. Use when Codex needs to do any of these tasks on Bitget futures: check account balance, place an order, cancel an order, query order detail, or query fills. Use when the user asks for command-line API execution with API key/secret/passphrase stored in a local .env file.
---

# Setup

1. Ensure `.env` exists in the skill root with:
- `BITGET_API_KEY`
- `BITGET_SECRET_KEY`
- `BITGET_PASSPHRASE`
2. Run scripts from the skill root (`bitget_api/`).

# Scripts

## 1) Futures Balance
Command:

```bash
python3 scripts/get_balance.py --product-type USDT-FUTURES
```

Required parameters:
- `--product-type` (example: `USDT-FUTURES`)

## 2) Place Order
Command:

```bash
python3 scripts/place_order.py \
  --product-type USDT-FUTURES \
  --symbol BTCUSDT \
  --margin-coin USDT \
  --margin-mode crossed \
  --side buy \
  --order-type market \
  --size 0.01
```

Required parameters:
- `--symbol`
- `--product-type` (default: `USDT-FUTURES`)
- `--margin-coin`
- `--margin-mode` (`crossed` or `isolated`, default: `crossed`)
- `--side` (`buy` or `sell`)
- `--order-type` (`market` or `limit`)
- `--size`

Optional parameters:
- `--trade-side` (`open` or `close`, hedge mode only)
- `--price` (required when `--order-type limit`)
- `--client-oid`

## 3) Cancel Order
Command:

```bash
python3 scripts/cancel_order.py \
  --symbol BTCUSDT \
  --margin-coin USDT \
  --order-id 1234567890
```

Required parameters:
- `--symbol`
- `--margin-coin`
- `--order-id`

## 4) Query Order Detail
Command:

```bash
python3 scripts/query_order.py --symbol BTCUSDT --order-id 1234567890
```

Required parameters:
- `--symbol`
- `--order-id`

## 5) Query Fills
Command:

```bash
python3 scripts/query_fills.py --symbol BTCUSDT --product-type USDT-FUTURES
```

Required parameters:
- `--symbol`
- One of:
  - `--product-type`
  - `--margin-coin`

# Notes

- All scripts share signing and HTTP logic from `scripts/core.py`.
- Signature format is `timestamp + method + requestPath + queryString + body` with HMAC-SHA256 and Base64 encoding.
- Scripts print JSON response to stdout and exit non-zero on API/network/auth errors.

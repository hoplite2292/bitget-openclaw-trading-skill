# bitget_api

Lightweight MVP scripts for Bitget Mix V2 (USDT-FUTURES) trading workflows.

## Features
- Futures account balance query
- Order placement (market/limit)
- Order cancellation
- Order detail query
- Fill history query

## Project Structure
```text
bitget_api/
├── SKILL.md
├── .env.example
├── .gitignore
├── README.md
└── scripts/
    ├── core.py
    ├── get_balance.py
    ├── place_order.py
    ├── cancel_order.py
    ├── query_order.py
    └── query_fills.py
```

## Environment Variables
Create a `.env` file at the project root:

```env
BITGET_API_KEY=...
BITGET_SECRET_KEY=...
BITGET_PASSPHRASE=...
```

## Usage Examples
Run commands from the project root (`bitget_api/`).

### 1) Get Balance
```bash
python3 scripts/get_balance.py --product-type USDT-FUTURES
```

### 2) Place Order (Market)
```bash
python3 scripts/place_order.py \
  --product-type USDT-FUTURES \
  --symbol BTCUSDT \
  --margin-coin USDT \
  --margin-mode crossed \
  --side buy \
  --order-type market \
  --size 0.0003
```

### 3) Cancel Order
```bash
python3 scripts/cancel_order.py \
  --symbol BTCUSDT \
  --margin-coin USDT \
  --order-id <ORDER_ID>
```

### 4) Query Order Detail
```bash
python3 scripts/query_order.py --symbol BTCUSDT --order-id <ORDER_ID>
```

### 5) Query Fills
```bash
python3 scripts/query_fills.py --symbol BTCUSDT --product-type USDT-FUTURES
```

## Notes
- Signature format: `timestamp + method + requestPath + queryString + body`
- Signature method: HMAC-SHA256 + Base64
- `--trade-side` in `place_order.py` is only needed for hedge mode.
- Sensitive data (`.env`) is excluded by `.gitignore`.

# bitget_api

Bitget Mix V2 (USDT-FUTURES)용 최소 기능(MVP) API 스크립트 모음입니다.

## 포함 기능
- 선물 계좌 잔고 조회
- 주문 생성 (시장가/지정가)
- 주문 취소
- 주문 상세 조회
- 체결 내역 조회

## 폴더 구조
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

## 환경 변수 설정
루트에 `.env` 파일을 만들고 아래 값을 채웁니다.

```env
BITGET_API_KEY=...
BITGET_SECRET_KEY=...
BITGET_PASSPHRASE=...
```

## 사용 예시
프로젝트 루트(`bitget_api/`)에서 실행합니다.

### 1) 잔고 조회
```bash
python3 scripts/get_balance.py --product-type USDT-FUTURES
```

### 2) 주문 생성 (시장가)
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

### 3) 주문 취소
```bash
python3 scripts/cancel_order.py \
  --symbol BTCUSDT \
  --margin-coin USDT \
  --order-id <ORDER_ID>
```

### 4) 주문 상세 조회
```bash
python3 scripts/query_order.py --symbol BTCUSDT --order-id <ORDER_ID>
```

### 5) 체결 내역 조회
```bash
python3 scripts/query_fills.py --symbol BTCUSDT --product-type USDT-FUTURES
```

## 참고
- 인증 서명 규칙: `timestamp + method + requestPath + queryString + body`
- 서명 방식: HMAC-SHA256 + Base64
- `place_order.py`의 `--trade-side`는 헤지 모드에서만 사용합니다.
- 민감정보(`.env`)는 Git에 올리지 않도록 `.gitignore`에 등록되어 있습니다.

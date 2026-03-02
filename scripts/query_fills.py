import argparse
import json

from core import BitgetApiError, BitgetClient, print_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query Bitget futures fills")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--product-type", help="Product type, e.g. USDT-FUTURES")
    parser.add_argument("--margin-coin", help="Margin coin, e.g. USDT")

    args = parser.parse_args()
    if not args.product_type and not args.margin_coin:
        parser.error("one of --product-type or --margin-coin is required")

    return args


def main() -> None:
    args = parse_args()
    client = BitgetClient.from_env()

    payload = client.request(
        method="GET",
        request_path="/api/v2/mix/order/fills",
        query={
            "symbol": args.symbol,
            "productType": args.product_type,
            "marginCoin": args.margin_coin,
        },
    )
    print_json(payload)


if __name__ == "__main__":
    try:
        main()
    except BitgetApiError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

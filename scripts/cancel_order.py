import argparse
import json

from core import BitgetApiError, BitgetClient, print_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cancel Bitget futures order")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--margin-coin", required=True, help="Margin coin, e.g. USDT")
    parser.add_argument("--order-id", required=True, help="Bitget order id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = BitgetClient.from_env()

    payload = client.request(
        method="POST",
        request_path="/api/v2/mix/order/cancel-order",
        body={
            "symbol": args.symbol,
            "marginCoin": args.margin_coin,
            "orderId": args.order_id,
        },
    )
    print_json(payload)


if __name__ == "__main__":
    try:
        main()
    except BitgetApiError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

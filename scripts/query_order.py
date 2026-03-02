import argparse
import json

from core import BitgetApiError, BitgetClient, print_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query Bitget futures order detail")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--order-id", required=True, help="Bitget order id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = BitgetClient.from_env()

    payload = client.request(
        method="GET",
        request_path="/api/v2/mix/order/detail",
        query={
            "symbol": args.symbol,
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

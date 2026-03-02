import argparse
import json

from core import BitgetApiError, BitgetClient, print_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get Bitget futures account balance")
    parser.add_argument("--product-type", required=True, help="Product type, e.g. USDT-FUTURES")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = BitgetClient.from_env()

    payload = client.request(
        method="GET",
        request_path="/api/v2/mix/account/accounts",
        query={"productType": args.product_type},
    )
    print_json(payload)


if __name__ == "__main__":
    try:
        main()
    except BitgetApiError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

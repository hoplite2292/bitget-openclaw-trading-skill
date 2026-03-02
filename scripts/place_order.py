import argparse
import json

from core import BitgetApiError, BitgetClient, print_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Place Bitget futures order")
    parser.add_argument(
        "--product-type",
        default="USDT-FUTURES",
        help="Product type, default: USDT-FUTURES",
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--margin-coin", required=True, help="Margin coin, e.g. USDT")
    parser.add_argument(
        "--margin-mode",
        default="crossed",
        choices=["crossed", "isolated"],
        help="Margin mode, default: crossed",
    )
    parser.add_argument("--side", required=True, choices=["buy", "sell"], help="Order side")
    parser.add_argument(
        "--trade-side",
        choices=["open", "close"],
        help="Trade side for hedge mode (open/close)",
    )
    parser.add_argument(
        "--order-type",
        required=True,
        choices=["market", "limit"],
        help="Order type",
    )
    parser.add_argument("--size", required=True, help="Order size")
    parser.add_argument("--price", help="Order price (required for limit order)")
    parser.add_argument("--client-oid", help="Client order id")

    args = parser.parse_args()

    if args.order_type == "limit" and not args.price:
        parser.error("--price is required when --order-type is limit")

    return args


def main() -> None:
    args = parse_args()
    client = BitgetClient.from_env()

    body = {
        "symbol": args.symbol,
        "productType": args.product_type,
        "marginCoin": args.margin_coin,
        "marginMode": args.margin_mode,
        "side": args.side,
        "orderType": args.order_type,
        "size": args.size,
    }

    if args.trade_side:
        body["tradeSide"] = args.trade_side
    if args.price:
        body["price"] = args.price
    if args.client_oid:
        body["clientOid"] = args.client_oid

    payload = client.request(
        method="POST",
        request_path="/api/v2/mix/order/place-order",
        body=body,
    )
    print_json(payload)


if __name__ == "__main__":
    try:
        main()
    except BitgetApiError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

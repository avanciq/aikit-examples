"""Pre-trade check with ccxt: round price and size to the exchange rules from AIKIT, check the minimums,
then (only if you turn it on) place an order on the exchange TESTNET. Default is a dry run.

Not trade ideas, not advice. The price/size here are placeholders for your own logic.
"""
import os, sys
from decimal import Decimal
from aikit_client import symbol_rules, to_step

VENUE, AIKIT_SYMBOL, CCXT_SYMBOL = "binance", "BTCUSDT", "BTC/USDT"


def prepare_order(price, qty):
    rules, receipts = symbol_rules(VENUE, AIKIT_SYMBOL, "spot")
    p, q = to_step(price, rules["tick_size"]), to_step(qty, rules["lot_step"])
    if q < rules["min_order_size"]:
        return None, f"size {q} below minimum {rules['min_order_size']}"
    if p * q < rules["min_notional"]:
        return None, f"value {p * q} below minimum {rules['min_notional']}"
    return (p, q), f"ok (rules from AIKIT, receipts {receipts[:2]}...)"


def main():
    price, qty = Decimal(os.environ.get("PRICE", "50000.1234")), Decimal(os.environ.get("QTY", "0.00123456"))
    order, why = prepare_order(price, qty)
    print(f"asked: price={price} qty={qty} -> {why}")
    if not order:
        return 1
    p, q = order
    print(f"rounded: price={p} qty={q}")
    if os.environ.get("PLACE_TESTNET_ORDER") != "1":
        print("dry run: nothing sent. Set PLACE_TESTNET_ORDER=1 plus testnet keys in the environment to try the testnet.")
        return 0
    import ccxt  # only needed for the testnet step
    ex = ccxt.binance({"apiKey": os.environ["EXCHANGE_TESTNET_KEY"], "secret": os.environ["EXCHANGE_TESTNET_SECRET"]})
    ex.set_sandbox_mode(True)       # TESTNET ONLY. Never point this at a live account.
    print(ex.create_order(CCXT_SYMBOL, "limit", "buy", float(q), float(p)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

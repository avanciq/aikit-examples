"""Tiny AIKIT client (standard library only). Facts only - not trade ideas or advice."""
import json, os, urllib.error, urllib.request
from decimal import Decimal, ROUND_DOWN

BASE = os.environ.get("AIKIT_BASE", "https://api.tradingcheckup.com").rstrip("/")


def _headers():
    h = {"Accept": "application/json", "User-Agent": "aikit-examples/0.1"}
    if os.environ.get("RAPIDAPI_KEY"):              # via RapidAPI
        h["X-RapidAPI-Key"] = os.environ["RAPIDAPI_KEY"]
        if os.environ.get("RAPIDAPI_HOST"):
            h["X-RapidAPI-Host"] = os.environ["RAPIDAPI_HOST"]
    elif os.environ.get("AIKIT_KEY"):               # free beta key
        h["Authorization"] = "Bearer " + os.environ["AIKIT_KEY"]
    return h


def get(path, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    req = urllib.request.Request(f"{BASE}{path}" + (f"?{q}" if q else ""), headers=_headers())
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:      # AIKIT returns a JSON message with 4xx (e.g. key needed)
        return json.loads(e.read() or b"{}")


def symbol_rules(venue, symbol, market="spot"):
    """Return (rules dict with Decimal values, receipt ids). Raises if AIKIT has no answer."""
    out = get("/v1/aikit/symbol", venue=venue, symbol=symbol, market=market)
    if out.get("status") == "key_needed" or not out.get("answer", {}).get("found"):
        raise RuntimeError(f"no answer for {venue} {symbol}: {out.get('message') or out.get('answer')}")
    spec = {k: Decimal(str(v).split()[0]) for k, v in out["answer"]["spec"].items()
            if k in ("tick_size", "lot_step", "min_order_size", "min_notional")}
    receipts = [f["receipt_id"] for f in out.get("facts", [])]
    return spec, receipts


def to_step(x, step):
    """Round DOWN to a multiple of step."""
    x, step = Decimal(str(x)), Decimal(str(step))
    return (x / step).to_integral_value(ROUND_DOWN) * step

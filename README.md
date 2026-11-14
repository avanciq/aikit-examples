# aikit-examples

Small, runnable examples for [AIKIT](https://tradingcheckup.com/aikit/): an API with dated, sourced exchange rules (tick size, lot step, minimum order size and value, fees, rate limits) for trading-bot builders.

**Facts and code checks only, not trade ideas or advice.** The examples place no live orders. The optional step uses an exchange **testnet** only.

## What's here
- `aikit_client.py` - 40-line client (standard library only) and a round-down helper.
- `bot_example.py` - pre-trade check: ask AIKIT for the rules for a symbol, round price to the tick and size to the lot step, check minimum size and minimum value, then (optional) send a limit order to the exchange testnet with ccxt.
- `test_offline.py` - tests that need no network.

## Run it (2 minutes)
```bash
git clone https://github.com/avanciq/aikit-examples && cd aikit-examples
# free beta key, 25 credits, no sign-up (one per network per 30 days):
export AIKIT_KEY=$(curl -s -X POST https://api.tradingcheckup.com/v1/aikit/trial | python3 -c "import sys,json;print(json.load(sys.stdin)['key'])")
python3 bot_example.py
```
Output (example):
```
asked: price=50000.1234 qty=0.00123456 -> ok (rules from AIKIT, receipts [...])
rounded: price=50000.12 qty=0.00123
dry run: nothing sent.
```
Using RapidAPI instead: `export RAPIDAPI_KEY=... RAPIDAPI_HOST=...` (copy the host from the code snippet on the Endpoints tab) - see `.env.example`.

## Testnet step (optional)
Set `PLACE_TESTNET_ORDER=1`, `EXCHANGE_TESTNET_KEY`, `EXCHANGE_TESTNET_SECRET` (testnet keys only; `pip install ccxt`). Keys are read from the environment, never from code. Never use keys that can trade real money.

## Notes
- Every AIKIT fact has an official source URL, a read date and a signed receipt (`/v1/aikit/receipts/{id}`).
- Facts are re-read daily and can change. A missing fact is reported as missing; fall back to the exchange's own API.
- Limits: free beta key = 25 credits (1 per lookup).

MIT licence.

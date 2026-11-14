from decimal import Decimal
from aikit_client import to_step
import bot_example as b

def test_to_step():
    assert to_step("50000.1234", "0.01") == Decimal("50000.12")
    assert to_step("0.00123456", "0.00001") == Decimal("0.00123")

def test_prepare(monkeypatch):
    rules = {"tick_size": Decimal("0.01"), "lot_step": Decimal("0.00001"), "min_order_size": Decimal("0.00001"), "min_notional": Decimal("5")}
    monkeypatch.setattr(b, "symbol_rules", lambda *a: (rules, ["rcp_x"]))
    assert b.prepare_order(Decimal("50000.1234"), Decimal("0.00123456"))[0] == (Decimal("50000.12"), Decimal("0.00123"))
    assert b.prepare_order(Decimal("50000"), Decimal("0.000005"))[0] is None       # below min size
    assert b.prepare_order(Decimal("50000"), Decimal("0.00009"))[0] is None        # 4.5 < 5 min value

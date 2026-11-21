from datetime import date
import todo_core as tc

RAW = '''Sure! ```json
[{"task":"Call dad","priority":"low","deadline":"2026-11-22"},
 {"task":"Finish DBMS assignment","priority":"High","deadline":"2026-11-27"},
 {"task":"Clean laptop","priority":"weird","deadline":""},
 {"task":"Pay hostel fees","priority":"High","deadline":"2026-11-25"},
 {"task":"  ","priority":"High","deadline":"x"}]
```'''

def test_parse_and_sort():
    t = tc.parse_tasks(RAW)
    assert [x["task"] for x in t] == ["Pay hostel fees", "Finish DBMS assignment", "Clean laptop", "Call dad"]
    assert t[2]["priority"] == "Medium" and t[2]["deadline"] == "Not specified"

def test_bad_output():
    import pytest
    with pytest.raises(ValueError):
        tc.parse_tasks("no json here")

def test_prompt_has_date():
    p = tc.build_prompt("buy milk", date(2026, 11, 21))
    assert "2026-11-21" in p and "Saturday" in p and "buy milk" in p

def test_retry(monkeypatch):
    outs = iter(["garbage", RAW])
    monkeypatch.setattr(tc, "call_llm", lambda *a, **k: next(outs))
    assert len(tc.extract_tasks("x", "groq", "k")) == 4

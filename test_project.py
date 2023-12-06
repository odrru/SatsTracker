import pytest
from project import format, old, convert, terminate

def test_format():
    assert format(5) == "-----"

def test_convert(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'USD')
    ticker, conversion = convert(100000000)
    assert ticker == 'USD'
    assert conversion > 10000

def test_old():
    with open("new.txt","w") as file:
        file.write("test")
    assert old("new.txt") == False



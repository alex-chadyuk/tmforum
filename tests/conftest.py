import json
from types import SimpleNamespace

import pytest
import requests
from tmforum import Context


@pytest.fixture
def backend(monkeypatch):
    """Replaces requests.request with a stub that records calls and returns `body`."""
    stub = SimpleNamespace(calls=[], body=None, status_code=200)

    def request(method, url, headers=None, data=None):
        stub.calls.append((method, url))
        text = json.dumps(stub.body) if stub.body is not None else ""
        return SimpleNamespace(status_code=stub.status_code, headers={}, text=text)

    monkeypatch.setattr(requests, "request", request)
    return stub


@pytest.fixture
def context():
    return Context(api_base_url="https://host:port/tmf-api", headers={})

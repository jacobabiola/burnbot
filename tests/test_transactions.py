import ast
import json
import time
import types
from unittest.mock import MagicMock

import pytest


def _load_get_wallet_transactions():
    with open('burnBot.py', 'r') as f:
        source = f.read()
    module = ast.parse(source)
    func_node = next(
        node for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == 'get_wallet_transactions'
    )
    code = compile(ast.Module([func_node], []), 'burnBot.py', 'exec')
    dummy_requests = types.SimpleNamespace(get=MagicMock())
    namespace = {
        'requests': dummy_requests,
        'json': json,
        'time': time,
        'ETHERSCAN_API_KEY': 'key'
    }
    exec(code, namespace)
    return namespace['get_wallet_transactions'], dummy_requests.get

def test_get_wallet_transactions_invalid_blockchain():
    func, mock_get = _load_get_wallet_transactions()
    with pytest.raises(ValueError):
        func('0x123', '0xabc', 'invalid')
    mock_get.assert_not_called()

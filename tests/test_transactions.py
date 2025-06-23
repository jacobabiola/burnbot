import unittest
from unittest.mock import patch
import sys
import types
import ast

# Dynamically load the get_wallet_transactions function without executing the full script
with open('burnBot.py', 'r') as f:
    tree = ast.parse(f.read(), filename='burnBot.py')
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == 'get_wallet_transactions':
        func_code = ast.Module([node], [])
        ns = {}
        exec(compile(func_code, 'burnBot.py', 'exec'), ns)
        get_wallet_transactions = ns['get_wallet_transactions']
        break

# Provide stub modules for external dependencies
requests_stub = types.ModuleType('requests')
requests_stub.get = lambda *args, **kwargs: None
sys.modules.setdefault('requests', requests_stub)

class TestGetWalletTransactions(unittest.TestCase):
    def test_invalid_blockchain_raises(self):
        with patch('requests.get') as mock_get:
            with self.assertRaises(ValueError):
                get_wallet_transactions('0x0', '0x0', 'btc')
            mock_get.assert_not_called()

if __name__ == '__main__':
    unittest.main()

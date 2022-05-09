import datetime
from unittest.mock import Mock
from forta_agent import FindingSeverity, FindingType, create_transaction_event, get_web3_provider
from agent import handle_transaction


class TestUnusualHighGasUsage:
    def test_basic_unusual_high_gas_usage(self):
        gas_values = [15, 16.4, 15, 13.8, 15, 14.1, 16.5, 20, 17, 14, 15.6, 50, 22]
        findings = []

        opensea = '0x7be8076f4ea4a4ad08075c2508e481d6c946d12b'

        gas_multiplier = 10000

        for gas_val in [x * gas_multiplier for x in gas_values]:
            mock_tx_event = create_transaction_event({
                'addresses': [opensea],
                'transaction': {
                    'gas': hex(int(gas_val)),
                    'hash': 'transaction_hash'
                },
                'hash': 'transaction_event_hash',
                'block': {
                    'timestamp': 19971309
                }
            })
            findings = findings.__add__(handle_transaction(mock_tx_event))

        assert len(findings) == 2
        assert findings[0].severity == FindingSeverity.High
        assert findings[1].severity == FindingSeverity.Medium

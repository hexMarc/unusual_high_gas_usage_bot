import datetime
import itertools
from unittest.mock import Mock

import forta_agent
from forta_agent import FindingSeverity, FindingType, create_transaction_event, get_web3_provider, Finding
from web3 import Web3, HTTPProvider

from agent import handle_transaction, findings_count


def pretty_print(findings: [Finding]):
    for finding in findings:
        print(f"Found Unusual Gas Usage\n"
              f"Name: {finding.name}\n"
              f"Description: {finding.description}\n"
              f"Severity: {finding.severity}\n"
              f"Protocol Name: {finding.metadata['protocol_name']}\n"
              f"Transaction Hash: {finding.metadata['transaction_event_hash'].hex()}\n"
              f"\n")
    pass


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

    def test_ronin_bridge_exploiter(self):
        # w3_provider: forta_agent.Web3 = get_web3_provider()
        w3 = Web3(HTTPProvider('https://cloudflare-eth.com'))
        w3.provider.request_counter = itertools.count(start=1)
        print(w3.isConnected())
        initial_block = 14442757
        end_block = 14443221

        findings = []

        for block_number in range(initial_block, end_block):
            block = w3.eth.get_block(block_number, True)
            for txn in block.transactions:
                mock_tx_event = create_transaction_event({
                    'addresses': [txn['to'], txn['from']],
                    'transaction': {
                        'gas': hex(txn.gas),
                        'hash': txn.hash
                    },
                    'hash': 'transaction_event_hash',
                    'block': {
                        'timestamp': block.timestamp
                    }
                })
                fs = handle_transaction(mock_tx_event)
                pretty_print(fs)
                findings = findings.__add__(fs)
            print(f"Processed block {block_number}")

        print(len(findings))


if __name__ == '__main__':
    t = TestUnusualHighGasUsage()
    t.test_ronin_bridge_exploiter()

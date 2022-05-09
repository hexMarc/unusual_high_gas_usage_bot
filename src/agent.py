from forta_agent import Finding, FindingType, FindingSeverity, TransactionEvent
from gas_storer import GasCounter, Trend

INTERESTING_PROTOCOLS = {
    '0xacd43e627e64355f1861cec6d3a6688b31a6f952': 'Yearn Dai vault',
    '0x7be8076f4ea4a4ad08075c2508e481d6c946d12b': 'OpenSea',
    '0x11111112542d85b3ef69ae05771c2dccff4faa26': '1inch V3',
    '0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f': 'SushiSwap: Router',
    '0xa0c68c638235ee32657e8f720a23cec1bfc77c77': 'Polygon (Matic) Bridge',
    '0x7a250d5630b4cf539739df2c5dacb4c659f2488d': 'UniSwap V2',
    '0xa5409ec958c83c3f309868babaca7c86dcb077c1': 'OpenSea: Registry',
    '0x3845badAde8e6dFF049820680d1F14bD3903a5d0': 'The Sandbox Token',
    '0x098B716B8Aaf21512996dC57EB0615e2383E2f96': 'Ronin Bridge  ',
}
TIME_INTERVAL = 60
MAX_STORAGE = 100
MAX_AMOUNT_GAS_VALUES = 100
ACCEPTED_GAS_INTERVAL = 20000

findings_count = 0

gas_counter = GasCounter(TIME_INTERVAL, MAX_STORAGE, ACCEPTED_GAS_INTERVAL)


def normalize_gas(gas_value):
    return gas_value


def handle_gas_finding(transaction_event: TransactionEvent, gas_trend: Trend, protocol: str):
    if gas_trend is Trend.OnTrend:
        return None

    if gas_trend is Trend.OneLevelUp:
        return Finding({
            'name': 'Unusual High Gas Usage',
            'description': f'Gas Usage : {normalize_gas(transaction_event.transaction.gas)}',
            'alert_id': 'UnusualHighGasUsage-1',
            'severity': FindingSeverity.Medium,
            'type': FindingType.Suspicious,
            'metadata': {
                'protocol_address': protocol,
                'protocol_name': INTERESTING_PROTOCOLS[protocol],
                'transaction_event_hash': transaction_event.transaction.hash,
            }
        })

    # In this case the gas_trend should be Trend.TwoLevelUp
    return Finding({
        'name': 'Unusual High Gas Usage',
        'description': f'Gas Usage : {normalize_gas(transaction_event.transaction.gas)}',
        'alert_id': 'UnusualHighGasUsage-2',
        'severity': FindingSeverity.High,
        'type': FindingType.Suspicious,
        'metadata': {
            'protocol_address': protocol,
            'protocol_name': INTERESTING_PROTOCOLS[protocol],
            'transaction_event_hash': transaction_event.transaction.hash,
        }
    })


def handle_transaction(transaction_event: TransactionEvent):
    findings = []

    # limiting this agent to emit only len of the protocols listed findings
    # global findings_count
    # if findings_count >= len(INTERESTING_PROTOCOLS):
    #     return findings
    triggered_addresses = set(transaction_event.addresses)
    involved_protocols = [protocol_address for protocol_address in list(INTERESTING_PROTOCOLS.keys()) if
                          protocol_address in triggered_addresses]

    for protocol in involved_protocols:
        gas_trend = gas_counter.set_gas(protocol, transaction_event.transaction.hash,
                                        transaction_event.block.timestamp,
                                        transaction_event.transaction.gas)
        f = handle_gas_finding(transaction_event, gas_trend, protocol)

        if f is not None:
            findings.append(f)

    return findings

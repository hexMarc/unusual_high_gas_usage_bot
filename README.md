# Unusual High Gas Usage Agent

## Description

This agent Monitor unusual high gas usage.

Accepted Gas: `10000`

## Supported Chains

- Ethereum

## Alerts

Describe each of the type of alerts fired by this agent

- UnusualHighGasUsage-1
    - Fired when transaction spend an amount of gas between `medium_historic_gas + accepted_gas` and
      the `double_of_historic_max_value`.
    - Severity is set to "Medium".
    - Type is always set to "suspicious".
    - Metadata:
        - protocol_address: Address,
        - protocol_name: String,
        - transaction_event_hash: transaction.hash.


- UnusualHighGasUsage-2
    - Fired when transaction spend more than the `double_of_historic_max_value`.
    - Severity is set to "High".
    - Type is always set to "suspicious".
    - Metadata:
        - protocol_address: Address,
        - protocol_name: String,
        - transaction_event_hash: transaction.hash.

## Protocols

|       Protocol          |                 Address                    |
|-------------------------|--------------------------------------------|
|`Yearn Dai vault`        |`0xacd43e627e64355f1861cec6d3a6688b31a6f952`|
|`OpenSea`                |`0x7be8076f4ea4a4ad08075c2508e481d6c946d12b`|
|`1inch V3`               |`0x11111112542d85b3ef69ae05771c2dccff4faa26`|
|`SushiSwap: Router`      |`0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f`|
|`Polygon (Matic) Bridge` |`0xa0c68c638235ee32657e8f720a23cec1bfc77c77`|
|`UniSwap V2`             |`0x7a250d5630b4cf539739df2c5dacb4c659f2488d`|
|`OpenSea: Registry`      |`0xa5409ec958c83c3f309868babaca7c86dcb077c1`|
|`The Sandbox Token`      |`0x3845badAde8e6dFF049820680d1F14bD3903a5d0`|
|`Ronin Bridge`           |`0x098B716B8Aaf21512996dC57EB0615e2383E2f96`|

## Test Data

This agent is based on past data, meaning that it needs to analyze at least 10 transactions for each protocol in order
to contain data related to the protocol before make any assumption.

We test it processing several blocks and transactions:

```
        initial_block = 14442757
        end_block = 14443221
```

Some transactions that cause some alerts are:

- 0x287dad48bfea44fcd5e180a9109e51e56bda64504d3242879c2575d83265c538 (Ronin Bridge)
- 0xbb0c1380942c22799dea1df70cca4b4640f1f38760cb9dac9900d0d8099af7c1 (Ronin Bridge)
- 0x804386b71fc83949a57bbc97fec7f206682d8d42938dfb2943137d3601bacb50 (The Sandbox Token)

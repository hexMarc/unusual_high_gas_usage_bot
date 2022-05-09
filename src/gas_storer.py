from collections import deque
from enum import Enum
import pandas as pd


class Trend(Enum):
    OnTrend = 0
    OneLevelUp = 1
    TwoLevelUp = 2


class TransactionDetails:
    def __init__(self, txn_hash: str, timestamp: int, gas_used: int):
        self.hash = txn_hash
        self.timestamp = timestamp
        self.gas_used = gas_used


# GasCounter represent the class that store all the values that we fetch
# in order to calculate any Unusual High Gas Usage.
class GasCounter:
    # Creates a new instance of GasCounter
    def __init__(self, time_interval_minutes: int, max_storage: int, accepted_gas: int):
        self.time_interval = time_interval_minutes * 60 * 1000
        self.max_storage = max_storage
        self.accepted_gas = accepted_gas
        self.transactionDict = {}

    def get_trend(self, protocol: str, gas_used: int) -> Trend:
        # check only when you already has data to compare
        if len(self.transactionDict[protocol]) < 10:
            return Trend.OnTrend

        series = pd.Series(self.transactionDict[protocol])
        d = {'gas': series}
        df = pd.DataFrame(d)
        median = df.median()['gas']
        max_val = df.max()['gas']

        if median - self.accepted_gas <= gas_used <= median + self.accepted_gas:
            return Trend.OnTrend

        if gas_used < median:
            return Trend.OnTrend

        if median + self.accepted_gas <= gas_used < 2 * max_val:
            return Trend.OneLevelUp

        # THis case wil only fit if gas_used > 2 * max_val
        return Trend.TwoLevelUp

    def set_gas(self, protocol: str, txn_hash: int, block_timestamp: int, gas_used: int):
        if protocol not in self.transactionDict:
            self.transactionDict[protocol] = deque([], maxlen=self.max_storage)
        block_timestamp_ms = block_timestamp * 1000

        # get gas trend
        trend = self.get_trend(protocol, gas_used)

        # Insert new transaction details for gas calculation
        self.transactionDict[protocol].appendleft(TransactionDetails(txn_hash, block_timestamp_ms, gas_used))

        index = []
        i = 0
        # remove any transactions that fall outside of the interval
        for txn in self.transactionDict[protocol]:
            if txn.timestamp < block_timestamp_ms - self.time_interval:
                index.append(i)
            i += 1
        index.reverse()
        for index_to_delete in index:
            del self.transactionDict[protocol][index_to_delete]

        return trend

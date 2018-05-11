import requests
import datetime
from .models import Transaction


def get_transactions(address):
    address_data = requests.get('https://blockchain.info/pl/rawaddr/%s' % (address.value)).json()
    transactions = []

    for tx in address_data['txs']:
        value = 0

        for out in tx['out']:
            print(type(out['addr']), type(address.value))
            if address.value == out['addr']:
                value += out['value']
                print(value)

        transaction = Transaction(transaction_id=tx['tx_index'], value=value, version=tx['ver'], hash=tx['hash'],
                                  date=datetime.datetime.fromtimestamp(tx["time"]), weight=tx['weight'],
                                  result=tx['result'], size=tx['size'], vin=tx['vin_sz'], vout=tx['vout_sz'])

        if 'block_height' in tx.keys():
            transaction.block_height = tx['block_height']
        transaction.save()

        transaction.addresses.add(address)
        transactions.append(transaction)

    return transactions

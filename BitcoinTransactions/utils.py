import requests
import datetime
from .models import Transaction, TransactionValue


def add_transactions(tx, in_or_out, address):
    value = 0
    found_transaction = False

    for data in tx[in_or_out]:
        if address.value == data['addr']:
            value = data['value']
            found_transaction = True

    if found_transaction:
        transaction_values = {'version': tx['ver'],
                              'hash': tx['hash'],
                              'vout': tx['vout_sz'],
                              'date': datetime.datetime.fromtimestamp(tx["time"]),
                              'weight': tx['weight'],
                              'result': tx['result'],
                              'size': tx['size'],
                              'vin': tx['vin_sz']}

        transaction, _ = Transaction.objects.update_or_create(transaction_id=tx['tx_index'],
                                                              defaults=transaction_values)

        if 'block_height' in tx.keys():
            transaction.block_height = tx['block_height']
            transaction.save()

        TransactionValue.objects.create(address=address, transaction=transaction, value=value, is_in=(in_or_out == 'in'))


def collect_transactions(address):
    address_data = requests.get('https://blockchain.info/pl/rawaddr/%s' % (address.value)).json()

    for tx in address_data['txs']:
        if 'in' in tx.keys():
            add_transactions(tx, 'in', address)
        if 'out' in tx.keys():
            add_transactions(tx, 'out', address)

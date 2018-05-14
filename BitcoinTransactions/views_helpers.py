import requests
import datetime
from django.db import transaction
from .models import Transaction, TransactionValue


@transaction.atomic
def add_transactions(transaction_json, address_type, address):
    """
    Get transaction as json and add Transaction and TransactionValue object based on it to database.
    :param transaction_json: json with transaction details
    :param address_type: it could be 'inputs' or 'out'. It refers to incoming and outcoming addresses.
    :param address: Address object
    """

    value = 0
    found_transaction = False

    for data in transaction_json[address_type]:
        if address_type == 'inputs':
            data = data['prev_out']
        if address.value == data['addr']:
            value = data['value']
            found_transaction = True

    if found_transaction:
        transaction_values = {'version': transaction_json['ver'],
                              'hash': transaction_json['hash'],
                              'vout': transaction_json['vout_sz'],
                              'date': datetime.datetime.fromtimestamp(transaction_json["time"]),
                              'weight': transaction_json['weight'],
                              'result': transaction_json['result'],
                              'size': transaction_json['size'],
                              'vin': transaction_json['vin_sz']}

        transaction, _ = Transaction.objects.update_or_create(transaction_id=transaction_json['tx_index'],
                                                              defaults=transaction_values)

        if 'block_height' in transaction_json.keys():
            transaction.block_height = transaction_json['block_height']
            transaction.save()

        TransactionValue.objects.create(address=address, transaction=transaction, value=value,
                                        is_in=(address_type == 'inputs'))


def collect_transactions(address):
    """
    Send request to Blockchain Api and add transactions' objects based on response from it.
    :param address: Address object
    """

    address_data = requests.get('https://blockchain.info/pl/rawaddr/%s' % address.value).json()

    for transaction in address_data['txs']:
        if 'inputs' in transaction.keys():
            add_transactions(transaction, 'inputs', address)
        if 'out' in transaction.keys():
            add_transactions(transaction, 'out', address)

from django.shortcuts import render
from .forms import BitcoinForm
from .models import Address
from .utils import get_transactions


def bitcoin(request):
    if request.method == 'POST':
        form = BitcoinForm(request.POST)
        if form.is_valid():
            bitcoin_address = request.POST['address'].strip()
            address, created = Address.objects.get_or_create(value=bitcoin_address)

            if not created:
                return render(request, 'BitcoinTransactions/transactions.html', {
                    'form': form,
                    'transactions': address.transaction_set.all(),
                    'address': address
                })
            else:
                transactions = get_transactions(address)
                return render(request, 'BitcoinTransactions/transactions.html', {
                    'form': form,
                    'transactions': transactions,
                    'address': address
                })
    else:
        form = BitcoinForm()

    return render(request, 'BitcoinTransactions/bitcoin.html', {'form': form})
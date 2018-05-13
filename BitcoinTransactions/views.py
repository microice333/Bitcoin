import qrcode
from django.shortcuts import render, HttpResponse
from django.db.models import Sum, Count, Q
from django.db.models.functions import Coalesce
from .forms import BitcoinForm
from .models import Address
from .utils import collect_transactions


def bitcoin(request):
    if request.method == 'POST':
        form = BitcoinForm(request.POST)

        if form.is_valid():
            bitcoin_address = request.POST['address'].strip()
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']

            address, created = Address.objects.get_or_create(value=bitcoin_address)

            if created:
                collect_transactions(address)

            filters = dict()

            if from_date:
                filters['transaction__date__gte'] = from_date

            if to_date:
                filters['transaction__date__lte'] = to_date

            transactions = address.transactionvalue_set.filter(**filters)

            return render(request, 'BitcoinTransactions/transactions.html', {
                'address': address,
                'form': form,
                'transactions': transactions,
                'transactions_info': transactions.all().aggregate(sum=Sum('value'), count=Count('transaction'),
                                                                  saldo=Coalesce(Sum('value', filter=Q(is_in=False)), 0)
                                                                  - Coalesce(Sum('value', filter=Q(is_in=True)), 0))
            })
    else:
        form = BitcoinForm()

    return render(request, 'BitcoinTransactions/bitcoin.html', {'form': form})


def generate_qr(request, address):
        img = qrcode.make(address)
        response = HttpResponse(content_type='image/png')
        img.save(response, "PNG")
        return response

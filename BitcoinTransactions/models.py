from django.db import models


class Address(models.Model):
    value = models.CharField(max_length=100)


class Transaction(models.Model):
    addresses = models.ManyToManyField(Address, through='TransactionValue')
    date = models.DateField()
    transaction_id = models.IntegerField()
    size = models.IntegerField()
    version = models.IntegerField()
    vin = models.IntegerField()
    vout = models.IntegerField()
    hash = models.CharField(max_length=100)
    weight = models.IntegerField()
    block_height = models.IntegerField(null=True)
    result = models.IntegerField()


class TransactionValue(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    value = models.BigIntegerField()
    is_in = models.BooleanField()

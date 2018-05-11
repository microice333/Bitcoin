from django.db import models


class Address(models.Model):
    value = models.CharField(max_length=100)


class Transaction(models.Model):
    addresses = models.ManyToManyField(Address)
    date = models.DateField()
    transaction_id = models.IntegerField()
    value = models.BigIntegerField()
    size = models.IntegerField()
    version = models.IntegerField()
    vin = models.IntegerField()
    vout = models.IntegerField()
    hash = models.CharField(max_length=100)
    weight = models.IntegerField()
    block_height = models.IntegerField(null=True)
    result = models.IntegerField()

    def value_btc(self):
        return self.value / 100000000

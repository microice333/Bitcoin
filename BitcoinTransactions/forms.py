from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class BitcoinForm(forms.Form):
    address = forms.CharField(label='Bitcoin address', max_length=100)
    from_date = forms.DateField(widget=DateInput(), required=False)
    to_date = forms.DateField(widget=DateInput(), required=False)

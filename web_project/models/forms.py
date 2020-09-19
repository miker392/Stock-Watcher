from django import forms

class NewStockForm(forms.Form):
    new_stock = forms.CharField(label='new_stock', max_length=100)
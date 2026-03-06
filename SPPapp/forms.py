from django import forms

class StockPredictionForm(forms.Form):
    open_price = forms.FloatField()
    high_price = forms.FloatField()
    low_price = forms.FloatField()
    volume = forms.FloatField()

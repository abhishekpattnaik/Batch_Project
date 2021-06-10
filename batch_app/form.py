from django import forms

class MainForm(forms.Form):
    batch_name = forms.CharField()
    number_of_codes = forms.IntegerField()

class SearchKeyword(forms.Form):
    search_keyword = forms.CharField()
    
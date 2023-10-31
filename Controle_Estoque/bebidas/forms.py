from django import forms
from .models import Bebidas, Venda

class BebidaForm(forms.ModelForm):
    class Meta:
        model = Bebidas
        fields = ['nome', 'quantidade', 'preco_unitario']

class VendaForm(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Bebidas.objects.all(), empty_label=None)  # Adiciona o campo 'produto'
    
    class Meta:
        model = Venda
        fields = ['produto', 'quantidade']

from django import forms
from .models import Bebidas, Venda

# modelForm


class BebidaForm(forms.ModelForm):
    class Meta:
        model = Bebidas
        fields = ['nome', 'quantidade', 'preco']

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['id_bebida', 'quantidade']


# form.Form
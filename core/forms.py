from django import forms
from .models import CreditApplication, CreditProduct

class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        fields = ['product', 'amount', 'phone', 'message']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма кредита'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Дополнительно', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активные продукты
        self.fields['product'].queryset = CreditProduct.objects.all()
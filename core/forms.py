from django import forms
from .models import ContactMessage
from django.utils.safestring import mark_safe

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "company", "phone", "message"]
        labels = {
            "name": "Ваше имя",
            "email": "Email для связи",
            "company": "Название компании",
            "phone": "Телефон",
            "message": "Сообщение",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "company": forms.TextInput(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input"}),
            "message": forms.Textarea(attrs={"class": "input textarea", "rows": 12}),
        }

    agree_to_terms = forms.BooleanField(
        label=mark_safe('Я согласен на <a href="/privacy-policy/" target="_blank">обработку персональных данных</a>'),
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"})
    )


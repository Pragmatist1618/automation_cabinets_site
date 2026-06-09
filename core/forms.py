from django import forms
from .models import ContactMessage

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



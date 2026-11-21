from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Document


class DocumentFilterForm(forms.Form):
    expiry_date = forms.DateField(
        required=False,
        label="Дата окончания",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    owner = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Владелец",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from users.models import User
        self.fields['owner'].queryset = User.objects.all()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "number", "expiry", "owner", "status", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "expiry": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "owner": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_number(self):
        number = self.cleaned_data.get("number")
        if number and len(number) < 3:
            raise ValidationError("Номер документа должен содержать хотя бы 3 символа.")
        return number

    def clean(self):
        cleaned_data = super().clean()
        expiry = cleaned_data.get("expiry")
        status = cleaned_data.get("status")

        if status == Document.Status.EXPIRED and expiry and expiry > date.today():
            raise ValidationError("Нельзя поставить статус 'Просрочен', если дата окончания еще не наступила.")
        return cleaned_data

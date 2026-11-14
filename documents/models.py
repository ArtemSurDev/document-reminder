from django.db import models
from users.models import User
from datetime import date

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название документа")
    number = models.CharField(max_length=100, verbose_name="Номер документа")
    expiry = models.DateField(verbose_name="Действителен до")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Владелец"
    )

    def days_until_expiry(self):
        return (self.expiry - date.today()).days

    def get_status(self):
        days = self.days_until_expiry()
        if days < 0:
            return "ПРОСРОЧЕН"
        elif days == 0:
            return "ИСТЕКАЕТ СЕГОДНЯ"
        elif days <= 30:
            return "ИСТЕКАЕТ СКОРО"
        else:
            return "ДЕЙСТВИТЕЛЕН"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["expiry"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
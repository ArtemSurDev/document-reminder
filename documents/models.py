from django.db import models
from users.models import User
from datetime import date


class Document(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Действителен"
        EXPIRING = "expiring", "Истекает скоро"
        EXPIRED = "expired", "Просрочен"

    title = models.CharField(max_length=200, verbose_name="Название документа")
    number = models.CharField(max_length=100, blank=True, verbose_name="Номер документа")
    expiry = models.DateField(verbose_name="Действителен до")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Владелец"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус",
    )
    image = models.ImageField(upload_to="documents/", blank=True, null=True, verbose_name="Скан документа")

    def days_until_expiry(self):
        return (self.expiry - date.today()).days

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["expiry"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
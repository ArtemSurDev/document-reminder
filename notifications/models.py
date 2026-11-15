from django.db import models
from users.models import User
from documents.models import Document


class NotificationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(created__lte=models.functions.Now())

    def for_document(self, document_id):
        return self.filter(document_id=document_id)


class NotificationManager(models.Manager.from_queryset(NotificationQuerySet)):
    pass


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Пользователь"
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Документ"
    )
    message = models.TextField(verbose_name="Сообщение")
    created = models.DateField(verbose_name="Дата создания")

    objects = NotificationManager()

    def __str__(self):
        return f"Уведомление для {self.user.name}"

    class Meta:
        ordering = ["-created"]
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
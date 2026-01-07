from django.db import models
from django.contrib.auth.models import User

class TimestampedModel(models.Model):
    """Абстрактная модель с created_at и updated_at"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CreditProduct(TimestampedModel):
    """Продукты банка (кредиты)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Мин. сумма")
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Макс. сумма")
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Ставка, %")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кредитный продукт"
        verbose_name_plural = "Кредитные продукты"

class CreditApplication(TimestampedModel):
    """Заявка на кредит"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(CreditProduct, on_delete=models.PROTECT, verbose_name="Продукт")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма кредита")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    def __str__(self):
        return f"Заявка #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = "Заявка на кредит"
        verbose_name_plural = "Заявки на кредит"
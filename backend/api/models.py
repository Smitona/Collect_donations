from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Goal(models.Model):
    """Модель для целей."""
    name = models.CharField()

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Collect(models.Model):
    """Модель Группового денежного сбора."""

    title = models.CharField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='collect'
    )
    image = models.ImageField(
        upload_to='donations/images/',
        null=False, blank=True
    )
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE,
        related_name='collect_goal'
    )
    goal_amount = models.PositiveIntegerField(blank=True)
    description = models.TextField()
    due_to = models.DateTimeField()

    class Meta:
        verbose_name = 'Групповой денежный сбор'
        verbose_name_plural = 'Групповые денежные сборы'
        ordering = ('title',)

    def __str__(self):
        return self.title[:30]

    def formatted_text(self):
        return '<br>'.join(self.description.splitlines())


class Payment(models.Model):
    """Модель Платежа (донации)."""

    amount = models.PositiveIntegerField()
    comment = models.CharField()
    donator = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    donation_to = models.ForeignKey(
        Collect, on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Платёж (донация)'
        verbose_name_plural = 'Платежи (донации)'
        ordering = ('date',)

    def __str__(self) -> str:
        return '{} закинул для {} {} ₽'.format(
            self.donator.username, self.donation_to.title, self.amount
        )

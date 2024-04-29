from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


GOALS = (
    ('Wedding', 'Свадьба'),
    ('PC Upgrade', 'Апгрейд ПК'),
    ('Treatment', 'На лечение'),
    ('For a dream life', 'На красивую жизнь'),
    ('Birthday', 'День рождения'),
    ('Animal Shelter', 'Приют для животных'),
)


class Collect(models.Model):
    """Модель Группового денежного сбора."""

    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='collect'
    )
    image = models.ImageField(
        upload_to='donations/images/',
        null=False, blank=True
    )
    goal = models.CharField(
        max_length=200,
        choices=GOALS
    )
    goal_amount = models.PositiveIntegerField(blank=True, default=None)
    description = models.TextField()
    due_to = models.DateTimeField()

    class Meta:
        verbose_name = 'Групповой денежный сбор'
        verbose_name_plural = 'Групповые денежные сборы'
        ordering = ('title',)

    def __str__(self):
        return self.title[:30]


class Payment(models.Model):
    """Модель Платежа (донации)."""

    amount = models.PositiveIntegerField()
    comment = models.CharField(max_length=200)
    donator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='donations',
    )
    donation_to = models.ForeignKey(
        Collect, on_delete=models.CASCADE,
        related_name='donations'
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

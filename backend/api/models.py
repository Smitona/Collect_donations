from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Goals(models.Model):
    """Модель для целей."""
    name = models.CharField()

    def __str__(self):
        return self.name

class Collect(models.Model):
    """Модель Группового денежного сбора."""

    title = models.CharField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collect'
    )
    image = models.ImageField(
        upload_to='images/', null=True, blank=True
    )
    goal = models.ForeignKey()
    goal_amount = models.PositiveIntegerField(blank=True)
    description = models.TextField()
    due_to = models.DateTimeField()

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


    def __str__(self) -> str:
        return '{} {} закинул для {} {} ₽'.format(
            self.donator.first_name, self.donator.last_name, self.donation_to.title, self.amount
        )
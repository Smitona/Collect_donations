from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()



class Collect(models.Model):
    title = models.CharField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collect'
    )
    image = models.ImageField(
        upload_to='images/', null=True, blank=True
    )
    collected = models.IntegerField()
    goal = models.IntegerField()
    due_to = models.DateTimeField()


class Payment(models.Model):
    amount = models.IntegerField()
    comment = models.CharField()
    donator = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    date = models.DateTimeField()
    collect = models.ForeignKey(
        Collect, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.comment[:30]
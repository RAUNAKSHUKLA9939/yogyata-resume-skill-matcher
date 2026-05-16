from django.db import models
from django.contrib.auth.models import User


class MatchHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    job_role = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    percentage = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_role
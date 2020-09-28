from django.db import models

from authentication.models import User


class Poll(models.Model):
    text = models.CharField(max_length=250)
    # publish_time = models.DateTimeField()


    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')

    text = models.CharField(max_length=250)


    def __str__(self):
        return self.text


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.choice.text + ' ' + self.user.name

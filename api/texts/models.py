from django.db import models


# Create your models here.
class Credentials(models.Model):
    key = models.TextField()
    shared_secret = models.TextField()

    def __str__(self):
        return ''.join([self.key, '|', self.shared_secret])


class Messages(models.Model):
    tag = models.TextField()
    msg = models.TextField()

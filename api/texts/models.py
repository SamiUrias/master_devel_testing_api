from django.db import models


# Create your models here.
class Credentials(models.Model):
    key = models.TextField()
    shared_key = models.TextField()

    def __str__(self):
        return ''.join([self.key, '|', self.shared_key])


class Messages(models.Model):
    tag = models.TextField()
    message = models.TextField()

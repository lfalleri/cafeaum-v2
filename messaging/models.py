from django.db import models

class Config(models.Model):

    sendgrid_key = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.sendgrid_key

    def __str__(self):
        return self.sendgrid_key

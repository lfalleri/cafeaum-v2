from authentication.models import Account
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from messaging.views import sendLessonCancellationEmail


def lessonCancellationEmail(account, instance, nb_personnes):
    sendLessonCancellationEmail(account, instance, nb_personnes)

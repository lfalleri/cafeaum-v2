# -*- coding: utf-8 -*-
from rest_framework import views, status
import json
from rest_framework.response import Response
from rest_framework import  status
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .models import Config


def getApiKey():
    config = Config.objects.get(id=1)
    return config

SENDGRID_API_KEY = getApiKey()

class EmailView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)
        lesson = data['lesson']
        account = data['account']
        print("lesson : %s"%lesson)
        print("account : %s"%account['email'])
        mail = EmailMultiAlternatives(
            subject="Your Subject",
            body="This is a simple text email body.",
            from_email="laurent.falleri@gmail.com",
            to=["laurentfall@hotmail.fr"],
            headers={"Reply-To": "laurentfall@hotmail.fr"}
        )
        # Add template
        mail.template_id = 'f6581133-5c0b-4cc1-9a86-96a8bcd0db06'

        # Replace substitutions in sendgrid template
        mail.substitutions = {'%type%': 'Hatha',
                              '%date%': 'mercredi 28 juin',
                              '%heure%': '11h30'}


        # Add categories
        mail.categories = [
            'confirmation',
        ]

        mail.send()
        return Response({
            'status': 'OK',
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)


class ContactEmailView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)

        type = data['type']
        name = data['name']
        email= data['email']
        tel = data['tel']
        message =data['message']

        mail = EmailMultiAlternatives(
            subject="Subject",
            body="Body",
            from_email="laurent.falleri@gmail.com",
            to=["laurent.falleri@gmail.com"],
            headers={"Reply-To": "laurent.falleri@gmail.com"}
        )

        # Add template (ContactMessage)
        mail.template_id = '4f9c3e44-7d6f-4ff8-a8f2-99018e998aff'

        # Replace substitutions in sendgrid template
        mail.substitutions = {'%type%': type,
                              '%email%' : email,
                              '%nom%': name,
                              '%message%':message,
                              '%tel%': tel}

        # Add categories
        mail.categories = [
            'contact',
        ]

        mail.send()

        return Response({
            'status': 'OK',
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)

# -*- coding: utf-8 -*-
from rest_framework import views, status
import json
from rest_framework.response import Response
from rest_framework import  status
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .models import SendgridApiKey, StaffEmail
from authentication.models import Account
from django.utils.dateparse import parse_datetime
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Attachment

def getApiKey():
    key = SendgridApiKey.objects.get(id=1)
    return key

def getEmails():
    emails = StaffEmail.objects.get(id=1)
    return emails

class AccountCreationEmailView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)
        json_email = data['email']

        staff_email = getEmails()
        account = Account.objects.filter(email=json_email)
        if not account:
            return Response({
                'status': 'Not found',
                'message': 'Account not found'
            }, status=status.HTTP_404_NOT_FOUND)

        account = account[0]

        subject = "Création de compte"
        message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Création de compte</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            <style>
               * {font-family: Montserrat, sans-serif;}
            </style>
            </head>
            <div style="font-family : Montserrat;font-size:120%%;color:#3f3f3f;">
               Bonjour %s,<br>
               Nous vous remercions d'avoir créer un compte CafeAum. <br><br>

               Vous pouvez désormais recharger votre carte et réserver les cours de yoga qui vous intéresse en vous rendant sur le
               <a href="http://cafeaum.fr/yoga/calendrier">Calendrier des cours</a><br><br>

               Bonne journée, <br>
               L'équipe CafeAum   <br>
               <br>
            </div>
            </html>
        """%(account.get_first_name())

        sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

        from_email = Email(staff_email.noreply())
        to_email = Email(json_email)
        content = Content("text/html", message_content)
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code >= 200) and (response.status_code < 300):
            return Response({
                'status': 'OK',
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'KO',
                'message': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class YogaConfirmationEmailView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)
        json_lesson = data['lesson']
        json_account = data['account']
        nb_persons = data['nb_persons']
        reservation_id = data['reservation_id']

        lesson_type = json_lesson['type']
        lesson_intensity = json_lesson['intensity']
        lesson_animator = json_lesson['animator']['prenom'] + " " + json_lesson['animator']['nom']
        lesson_date = str(parse_datetime(json_lesson['date']).strftime("%A %d %b %Y à %Hh%M"))

        account = Account.objects.get(id=json_account['id'])

        staff_email = getEmails()

        subject = "Confirmation de réservation"
        message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Confirmation de réservation</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            <style>
               * {font-family: Montserrat, sans-serif;}
            </style>
            </head>
            <div style="font-family : Montserrat;font-size:120%%;color:#3f3f3f;">
               Bonjour %s,<br>
               Nous vous confirmons votre réservation pour le cours : <br><br>

               <div style="font-family : Montserrat;">
               %s %s (animé par %s) <br>
               le %s, pour %s personne%s <br><br>
               </div >

               Vous pouvez annuler cette réservation en allant sur <a href="http://cafeaum.fr/yoga/annulation/%s">http://cafeaum.fr/yoga/annulation/%s</a><br><br>

               Bonne journée, <br>
               L'équipe CafeAum   <br>
               <br>
            </div>
            </html>
        """%(account.get_first_name(),
             lesson_type,
             lesson_intensity,
             lesson_animator,
             lesson_date,
             str(nb_persons),
             str("s" if nb_persons > 1 else ""),
             reservation_id,
             reservation_id)

        sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

        from_email = Email(staff_email.noreply())
        to_email = Email(account.get_email())
        content = Content("text/html", message_content)
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code >= 200) and (response.status_code < 300):
            return Response({
                'status': 'OK',
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'KO',
                'message': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class YogaCancellationEmailView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)
        json_lesson = data['lesson']
        json_account = data['account']

        lesson_type = json_lesson['type']
        lesson_intensity = json_lesson['intensity']
        lesson_animator = json_lesson['animator']['prenom'] + " " + json_lesson['animator']['nom']
        lesson_date = str(parse_datetime(json_lesson['date']).strftime("%A %d %b %Y à %Hh%M"))

        account = Account.objects.get(id=json_account['id'])

        staff_email = getEmails()

        subject = "Confirmation d'annulation"
        message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Confirmation de réservation</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            <style>
               * {font-family: Montserrat, sans-serif;}
            </style>
            </head>
            <div style="font-family : Montserrat;font-size:120%%;color:#3f3f3f;">
               Bonjour %s,<br>
               Nous vous confirmons l'annulation de votre cours : <br><br>

               <div style="font-family : Montserrat;">
               %s %s (animé par %s) <br>
               le %s<br><br>
               </div >

               Vous pouvez voir nos autres cours sur le <a href="http://cafeaum.fr/yoga/calendrier">Calendrier des cours</a><br><br>

               Bonne journée, <br>
               L'équipe CafeAum   <br>
               <br>
            </div>
            </html>
        """%(account.get_first_name(), lesson_type, lesson_intensity, lesson_animator, lesson_date)

        sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

        from_email = Email(staff_email.noreply())
        to_email = Email(account.get_email())
        content = Content("text/html", message_content)
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code >= 200) and (response.status_code < 300):
            return Response({
                'status': 'OK',
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'KO',
                'message': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RestaurantReservationEmailView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)

        personal_information = data['personal_information']
        reservation_information = data['reservation_information']

        staff_email = getEmails()

        subject = "Réservation de table"
        message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Demande de contact 2</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            </head>
            <p style="font-family : Montserrat;font-size:130%%;">
               CafeAum,<br><br>
               %s (email : %s %s) souhaite réserver une table le %s à %s pour %s personne%s. <br>
               %s
               <br><br>

               Merci de lui répondre dans les meilleurs délais.

               <br>
            </p>
            </html>
        """%(personal_information["name"],
             personal_information["email"],
             " / tel : %s" % personal_information["tel"] if personal_information["tel"] != "" else "",
             reservation_information["human_date"],
             reservation_information["hour"],
             reservation_information["nb_persons"],
             "s" if int(reservation_information["nb_persons"]) > 1 else "",
             "Son commentaire : <br> \"%s\""%('<br>'.join(personal_information["comment"].splitlines())) if personal_information["comment"] != "" else "",
             )

        sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

        from_email = Email(staff_email.noreply())
        to_email = Email(staff_email.contact())
        content = Content("text/html", message_content)
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code >= 200) and (response.status_code < 300):
            return Response({
                'status': 'OK',
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'KO',
                'message': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactEmailView(views.APIView):

    def post(self, request, format=None):
        data = json.loads(request.body)

        type = data['type']
        name = data['name']
        email = data['email']
        tel = data['tel']
        message = data['message']

        staff_email = getEmails()

        if type == "Réserver une table":
            subject = "Réservation de table"
            message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Demande de contact 2</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            </head>
            <p style="font-family : Montserrat;font-size:130%%;">
               CafeAum,<br>
               %s (email : %s / tel : %s) souhaite réserver une table. Son message :<br>

               "%s"
               <br><br>

               Merci de lui répondre dans les meilleurs délais.

               <br>
            </p>
            </html>
            """%(name, email, tel, '<br>'.join(message.splitlines()))
        else:
            subject = "Demande de contact"
            message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Demande de contact 2</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            </head>
            <p style="font-family : Montserrat;font-size:130%%;">
               CafeAum,<br>
               %s (email : %s / tel : %s) a laissé une demande de contact. Son message :<br>

               "%s"
               <br><br>

               Merci de lui répondre dans les meilleurs délais.

               <br>
            </p>
            </html>
            """%(name, email, tel, '<br>'.join(message.splitlines()))

        sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

        from_email = Email(staff_email.noreply())
        to_email = Email(staff_email.contact())
        content = Content("text/html", message_content)
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code >= 200) and (response.status_code < 300):
            return Response({
                'status': 'OK',
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'KO',
                'message': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordRecoveryEmailView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        email = data['email']
        token = data['token']

        staff_email = getEmails()

        subject = "Renouvellement de mot de passe"
        message_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>Renouvellement de mot de passe</title>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
            </head>
            <p style="font-family : Montserrat;font-size:130%%;">
               Bonjour,<br>
               Pour mettre à jour votre mot de passe, veuillez cliquer sur le lien suivant : <br>
               <a href="http://cafeaum.com/recovery/%s">http://cafeaum.com/recovery/%s</a><br>

               Attention ce lien n'est valide que pour 24h, aussi nous vous recommandons de modifier votre mot de passe dès que possible.<br><br>


               L'équipe CafeAum
               <br>
            </p>
            </html>
        """%(token,token)

        sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

        from_email = Email(staff_email.noreply())
        to_email = Email(email)
        content = Content("text/html", message_content)
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        if (response.status_code >= 200) and (response.status_code < 300):
            return Response({
                'status': 'OK',
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'KO',
                'message': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def send_lesson_cancellation_email(account, type, intensity, date, prix, nb_personnes):
    staff_email = getEmails()
    subject = "Annulation de cours"
    message_content = """
     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
     <html>
    <head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <title>Annulation de cours</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
    </head>
    <p style="font-family : Montserrat;font-size:130%%;">
       Bonjour %s,<br><br>
       Nous sommes dans le regret de vous apprendre que le cours du %s (%s %s) a été annulé.<br><br>
       Vous aviez effectué une réservation pour ce cours pour %d personne%s, aussi votre compte a été recrédité de %s points.
       <br><br>

       Nous vous prions de bien vouloir nous excuser pour la gêne occasionnée.<br>

       <br><br>
       L'équipe CafeAum.
       <br>
    </p>
    </html>
    """ % (account.get_first_name(),
           date,
           type,
           intensity,
           nb_personnes,
           "s" if (nb_personnes > 1) else "",
           str(prix * nb_personnes)
           )

    sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

    from_email = Email(staff_email.noreply())
    to_email = Email(account.get_email())
    content = Content("text/html", message_content)
    mail = Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=mail.get())

    if (response.status_code >= 200) and (response.status_code < 300):
        return Response({
            'status': 'OK',
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
           'status': 'KO',
           'message': 'Error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_lesson_modification_email(account, type, intensity, date, old_type, old_intensity, old_date):
    staff_email = getEmails()
    subject = "Modification de cours"
    message_content = """
     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
     <html>
    <head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <title>Modification de cours</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
    </head>
    <p style="font-family : Montserrat;font-size:130%%;">
       Bonjour %s,<br><br>
       Nous vous informons que le cours du %s (%s %s) pour lequel vous aviez réservé a été modifié. <br><br>
       Il s'agit maintenant d'un cours %s %s qui aura lieu le %s.
       <br><br>

       Vous pouvez, si vous le souhaitez, annuler votre réservation en vous rendant sur <a href='http://cafeaum.fr'>Cafe Aum</a><br>

       <br><br>
       L'équipe CafeAum.
       <br>
    </p>
    </html>
    """ % (account.get_first_name(),
           old_date,
           old_type,
           old_intensity,
           type,
           intensity,
           date,
           )

    sg = sendgrid.SendGridAPIClient(apikey=getApiKey())

    from_email = Email(staff_email.noreply())
    to_email = Email(account.get_email())
    content = Content("text/html", message_content)
    mail = Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=mail.get())

    if (response.status_code >= 200) and (response.status_code < 300):
        return Response({
            'status': 'OK',
            'message': 'Email sent'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
           'status': 'KO',
           'message': 'Error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
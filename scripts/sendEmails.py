import smtplib
import ssl
import time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ticketdb.models import AfterTicket
from ticketdb.models import PromTicket
from scripts.createCodes import run as createCodes


def create_message_prom(ticket_owner, receiver_email, sender_email, filename):
    body = """
        Buna, {0}! Ai atasat mai jos QR code-ul care serveste drept bilet la bal, te rog sa il prezinti la intrare.
        Pentru orice intrebari legate pe bal trimite un mesaj la @cse_avramiancu pe instagram, iar pentru probleme tehnice lui @stefan_lupsan.

        Acest e-mail a fost trimis automat, orice reply nu va fi vazut, te rog scrie-ne pe instagram. """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Bilet Balul Bobocilor Avram Iancu"
    message.attach(MIMEText(body.format(ticket_owner), "plain"))

    # Open file in binary form
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    return text

def create_message_after(ticket_owner, receiver_email, sender_email, filename):
    body = """
        Buna, {0}! Ai atasat mai jos QR code-ul care serveste drept bilet la after, te rog sa il prezinti la intrare.
        Pentru orice intrebari legate pe bal trimite un mesaj la @cse_avramiancu pe instagram, iar pentru probleme tehnice lui @stefan_lupsan.

        Acest e-mail a fost trimis automat, orice reply nu va fi vazut, te rog scrie-ne pe instagram. """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Bilet Balul Bobocilor Avram Iancu"
    message.attach(MIMEText(body.format(ticket_owner), "plain"))

    # Open file in binary form
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    return text


def run():
    createCodes()
    sender_email = "stefan.lupsan@gmail.com"
    password = "ecslhnnwocavnygz"
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.connect('smtp.gmail.com', port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for ticket in PromTicket.objects.all():
            if(ticket.mail_sent == 0):
                filename = "PROMQRCODES/{0}.png".format(ticket.name)
                text = create_message_prom(ticket.name, ticket.email, sender_email, filename)
                server.sendmail(sender_email, ticket.email, text)
                ticket.mail_sent = 1
                ticket.save()
                time.sleep(3)
        for ticket in AfterTicket.objects.all():
            if (ticket.mail_sent == 0):
                filename = "AFTERQRCODES/{0}.png".format(ticket.name)
                text = create_message_after(ticket.name, ticket.email, sender_email, filename)
                server.sendmail(sender_email, ticket.email, text)
                ticket.mail_sent = 1
                ticket.save()
                time.sleep(3)

    except Exception as e:
        print(e)
    finally:
        server.quit()



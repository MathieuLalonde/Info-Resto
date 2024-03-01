from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import yaml

# Configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)["email_config"]

smtp_server = config["smtp_server"]
port = config["port"]
login = config["login"]
password = config["password"]

sender_email = config["sender_email"]
receiver_email = config["receiver_email"]


def send_email(subject, plain_text, html, receiver_email=receiver_email):
    # Inspire de : https://realpython.com/python-send-email/

    # Assemble le contenu
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email

    message.attach(MIMEText(plain_text, "plain"))
    message.attach(MIMEText(html, "html"))

    # Envoie le message
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)  # Secure the connection
        server.login(login, password)

        server.sendmail(sender_email, receiver_email,
                        message.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()

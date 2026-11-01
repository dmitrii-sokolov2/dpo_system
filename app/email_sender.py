import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.mail.ru" 
SMTP_PORT = 465                 
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_magic_link(to_email: str, magic_token: str):
    link = f"http://127.0.0.1:8000/status/view/{magic_token}"
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Статус вашего заявления в отдел ДПО"
    
    body = f"""
    <html>
        <body style="font-family: Arial;">
            <h2>Здравствуйте!</h2>
            <p>Вы запросили проверку статуса вашего заявления.</p>
            <p>Для просмотра статуса перейдите по ссылке:</p>
            <a href="{link}" style="padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px;">Посмотреть статус</a>
            <p style="margin-top: 20px; color: #888;">Если вы не запрашивали эту информацию, просто проигнорируйте это письмо.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"✅ Письмо успешно отправлено на {to_email}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False
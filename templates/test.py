import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'helloworld073616@gmail.com'
EMAIL_HOST_PASSWORD = 'afmt dngs ponj vfsr'

# Email details
sender_email = EMAIL_HOST_USER
receiver_email = 'atulg0736@gmail.com'  # Replace with the recipient's email
subject = 'Test Email'
body = 'This is a test email sent using Python.'

# Create the email content
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Send the email
try:
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(message)
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")


import sendgrid
import base64

def send_email(from_email, to_email, subject, html, key):
    
    message = sendgrid.Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content='Find a Metaflow card attached'
    )

    encoded_content = base64.b64encode(
        html.encode('utf-8')).decode('utf-8')
    
    att = sendgrid.Attachment(
        file_content=encoded_content,
        file_type='text/html',
        file_name='card.html',
        disposition='attachment')
    
    message.add_attachment(att)
    sendgrid.SendGridAPIClient(key).send(message)

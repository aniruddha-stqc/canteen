import os
import smtplib
import logging
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(level=logging.INFO)


# Define the send_email function
def send_email(sender_email, sender_password, sender_dummy_email, recipient_emails, subject, body,
               attachment_file=None):
    try:
        # Create the email message
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender_dummy_email
        message['To'] = ", ".join(recipient_emails)

        # Attach the HTML body
        html_message = MIMEText(body, 'html')
        message.attach(html_message)

        # If an attachment is provided (not None or "NIL"), attach the file
        if attachment_file and attachment_file != "NIL":
            if not os.path.exists(attachment_file):
                raise FileNotFoundError(f"Error: Attachment file '{attachment_file}' not found.")

            print("Attachment file found.")

            print(f"Attaching file: {attachment_file}")
            with open(attachment_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)

            # Correctly format the filename without extra quotes
            filename = os.path.basename(attachment_file)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            message.attach(part)

        # Print email details
        print(f"Email prepared: Subject: {subject}, From: {sender_dummy_email}, To: {', '.join(recipient_emails)}")

        # Send the email
        print("Sending the email...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, message.as_string())
            print("Email sent successfully.")

    except FileNotFoundError as e:
        print(e)
        logging.error(e)
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your credentials.")
        logging.error("Authentication failed. Check your email credentials.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")


# Define the main function
def main():
    # Define the subject and body of the email
    subject = "Email Subject"
    body = """
    <html>
      <body>
        <h1>This is an HTML email</h1>
        <p>This email was sent from Python with an HTML formatted body.</p>
        <p><b>Bold Text</b></p>
        <p><i>Italic Text</i></p>
        <a href="https://www.example.com">Click here for more details</a>
      </body>
    </html>
    """
    sender_email = "ertlcanteen@gmail.com"  # Email for authentication
    sender_dummy_email = "noreplyertlcanteen@gmail.com"  # The 'From' address
    recipient_emails = ["aniruddha2008@gmail.com"]

    # Get email password from environment variable
    sender_password = "izvvljlqnlvrojbl"

    # Specify the file to attach (set to None or "NIL" to skip attachment)
    #attachment_file = r"C:\Users\avishek.raychoudhury\Desktop\CBSE-Class-12-Computer-Science-Syllabus-2023-24.pdf"  # or use None for no attachment
    attachment_file = "NIL"
    # Call the send_email function
    send_email(sender_email, sender_password, sender_dummy_email, recipient_emails, subject, body, attachment_file)

def send_mail_top_up(recipient_emails, amount, balance, transaction_date):
    # Define the subject and body of the email
    subject = "Top Up Confirmation"

    body = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERTL Staff Canteen - Top Up Notification</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; background-color: #f4f4f4; padding: 20px; }}
            .container {{ background-color: #fff; border-radius: 8px; padding: 20px; max-width: 600px; margin: 0 auto; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
            h2 {{ color: #2c3e50; }}
            p {{ font-size: 14px; }}
            .highlight {{ font-weight: bold; color: #16a085; }}
            .footer {{ font-size: 12px; text-align: center; color: #888; }}
            .footer a {{ color: #16a085; text-decoration: none; }}
            .button {{ background-color: #16a085; color: #fff; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>ERTL Staff Canteen - Top Up Notification</h2>
            <p>Dear User,</p>
            <p>We are pleased to inform you that your wallet has been successfully topped up. Here are the details of your transaction:</p>
            <p><strong>Transaction Details:</strong></p>
            <ul>
                <li><span class="highlight">Amount Added:</span> ₹{amount}</li>
                <li><span class="highlight">New Balance:</span> ₹{balance}</li>
                <li><span class="highlight">Date:</span> {transaction_date}</li>
            </ul>
            <p>If you have any questions or need further assistance, please feel free to contact the ERTL Staff Canteen Committee.</p>
            <a href="mailto:ertlcanteen@gmail.com" class="button">Contact Us</a>
            <p class="footer">Best regards,<br>ERTL Staff Canteen Committee</p>
        </div>
    </body>
    </html>
    '''.format(amount=amount, balance=balance, transaction_date=transaction_date)

    sender_email = "ertlcanteen@gmail.com"  # Email for authentication
    sender_dummy_email = "noreplyertlcanteen@gmail.com"  # The 'From' address
    #recipient_emails = ["aniruddha2008@gmail.com"]

    # Get email password from environment variable
    sender_password = "izvvljlqnlvrojbl"

    # Specify the file to attach (set to None or "NIL" to skip attachment)
    # attachment_file = r"C:\Users\avishek.raychoudhury\Desktop\CBSE-Class-12-Computer-Science-Syllabus-2023-24.pdf"  # or use None for no attachment
    attachment_file = "NIL"
    # Call the send_email function
    send_email(sender_email, sender_password, sender_dummy_email, recipient_emails, subject, body, attachment_file)


# Run the main function
if __name__ == "__main__":
    main()
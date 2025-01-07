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
    recipient_emails = ["sreemoyee.meditation@gmail.com", "aniruddha2008@gmail.com", "aniruddha@stqc.gov.in",
                        "avishek@stqc.gov.in"]

    # Get email password from environment variable
    sender_password = "izvvljlqnlvrojbl"

    # Specify the file to attach (set to None or "NIL" to skip attachment)
    attachment_file = r"C:\Users\avishek.raychoudhury\Desktop\CBSE-Class-12-Computer-Science-Syllabus-2023-24.pdf"  # or use None for no attachment
    #attachment_file = "NIL"
    # Call the send_email function
    send_email(sender_email, sender_password, sender_dummy_email, recipient_emails, subject, body, attachment_file)


# Run the main function
if __name__ == "__main__":
    main()
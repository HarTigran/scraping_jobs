import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, sender, recipients, password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(body, 'plain'))

    # Establish a connection with the SMTP server (for Gmail, use 'smtp.gmail.com')
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start TLS encryption (for security)
        server.starttls()

        # Login to your email account
        server.login(sender, password)

        # Send the email
        server.sendmail(sender, recipients, msg.as_string())

    print("Email sent successfully!")


# send_email(subject, body, sender, recipients, password)

# #sender - linkedin populate
# def send_email(match):
#     # Define the email content
#     sender_email = "clmtcampus@gmail.com"
#     receiver_email = "harutyunyan.tigran.v@gmail.com"
#     subject = "Your Subject Here"
#     message = """\
#     Hello,

#     you have been matched{}

#     Sincerely,
#     Your Name
#     """.format(match)

#     # Create the email message
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     # Attach the message to the email
#     msg.attach(MIMEText(message, 'plain'))

#     # Send the email
#     try:
#         # Establish a connection with the SMTP server (for Gmail, use 'smtp.gmail.com')
#         server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your email provider's SMTP server and port

#         # Start TLS encryption (for security)
#         server.starttls()

#         # Login to your email account
#         server.login(sender_email, "Wonderful1234!")  # Replace with your email password

#         # Send the email
#         server.sendmail(sender_email, receiver_email, msg.as_string())

#         # Close the server connection
#         server.quit()

#         print("Email sent successfully!")

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
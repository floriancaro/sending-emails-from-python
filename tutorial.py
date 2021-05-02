#!/usr/bin/env python3

from email.message import EmailMessage

sender = "me@example.com"
recipient = "you@example.com"

body = """Hey there,

I am learning to send emails using Python!"""

message = EmailMessage()

# From, To, and Subject are examples of email header fields. 
# They’re key-value pairs of labels and instructions used by email clients and servers to route and display the email. 
# They’re separate from the email's message body, which is the main content of the message.
message["From"] = sender
message["To"] = recipient
message["Subject"] = "Greetings from {} to {}!".format(sender,recipient)

message.set_content(body)


print(message)
print("Hello, World!")

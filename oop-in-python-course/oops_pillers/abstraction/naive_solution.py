class BadEmailService:
    # def send_email(self):
    #     self.connect()
    #     self.authenticate()
    #     print("Sending email...")
    #     self.disconnect()

    def connect(self):
        print("Connecting to email server...")

    def authenticate(self):
        print("Authenticating...")

    # We could also force clients to call connect, authenticate, send_email, and disconnect to send an email. That wouldn't be very nice tho! No abstraction means more effort for client/dev.
    def send_email(self):
        print("Sending email...")

    def disconnect(self):
        print("Disconnecting from email server...")

email = BadEmailService()

email.connect()
email.authenticate()
email.send_email()
email.disconnect()

# LOGS:
# Connecting to email server...
# Authenticating...
# Sending email...
# Disconnecting from email server...

# Oh no, I don't have such a simple API to just send an email (this thing I actually want to do). Much easier to make mistakes -- I might forget to disconnect after sending.
# What happens if implementation details change? Client code has to change.

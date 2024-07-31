import smtplib
from dotenv import load_dotenv
import os
load_dotenv()
class NotificationManager:
    def __init__(self):
        self.email = os.environ["EMAIL"]
        self.token = os.environ["EMAIL_TOKEN"]

    def send_email(self,to,stops,price,city, destination,departure_date,return_date):
        if stops==0:
            stops="None, Lucky you !!!"
        with smtplib.SMTP('smtp.gmail.com', 587) as connect:
            connect.starttls()
            # This method helps to make sure that our connection is safe, it makes our email encrypted
            connect.login(user=self.email, password=self.token)
            connect.sendmail(from_addr=self.email, to_addrs=to,
                             msg=f"Cheap Ticket to {destination} \n\nPrice:{price} GBP\n"
                                 f"Departure Airport IATA Code: {city}\n"
                                 f"Arrival Airport IATA Code: {destination}\n"
                                 f"Outbound Date: {departure_date}\n"
                                 f"Inbound Date: {return_date}\n"
                                 f"Stopovers:{stops}")
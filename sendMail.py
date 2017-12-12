# File to automatically send e_mail

import smtplib
from credFinder import returnCred

def send_mail(adress_who_send, adress_to_send, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(adress_who_send, password)

    server.sendmail(adress_who_send, adress_to_send, message)
    server.quit()

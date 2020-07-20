import getpass
import json
import os
import smtplib
import ssl
import urllib.request

email = os.environ["EMAIL"] if "EMAIL" in os.environ else input("Email: ")
password = os.environ["PASSWORD"] if "PASSWORD" in os.environ else getpass.getpass()

with urllib.request.urlopen("https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=51.5&lon=0") as fp:
    forecast = json.load(fp)
    precipitation = forecast["properties"]["timeseries"][0]["data"]["next_6_hours"]["details"]["precipitation_amount"]
    if precipitation > 0:
        msg = f"Subject: Don't forget your umbrella!\n\n{precipitation}mm of precipitation is forecast."
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
            server.login(email, password)
            server.sendmail(email, email, msg)

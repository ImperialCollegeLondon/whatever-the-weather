import getpass
import json
import os
import smtplib
import ssl
import urllib.request
import geopy
from geopy.geocoders import Nominatim

email = os.environ["EMAIL"] if "EMAIL" in os.environ else input("Log in to send an email.\nEmail: ")
password = os.environ["PASSWORD"] if "PASSWORD" in os.environ else getpass.getpass(prompt='Password: ')
locationstring = os.environ["LOCATION"] if "LOCATION" in os.environ else input("Location: ")

locator = Nominatim(user_agent="myGeocoder")
location = locator.geocode(locationstring)

print("Fetching weather for: ",location.address)
print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

with urllib.request.urlopen("https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=51.5&lon=0") as fp:
    forecast = json.load(fp)
    precipitation = forecast["properties"]["timeseries"][0]["data"]["next_6_hours"]["details"]["precipitation_amount"]

    print(f"{precipitation}mm of precipitation is forecast.")

    if precipitation > 0:
        msg = f"Subject: Don't forget your umbrella!\n\n{precipitation}mm of precipitation is forecast."
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
            server.login(email, password)
            server.sendmail(email, email, msg)
        print("Email sent.")
    else:
        print("No email sent.")

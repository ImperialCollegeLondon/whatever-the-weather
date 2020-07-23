"""
Author: Srayan Gangopadhyay
2020-07-23
Adapted from MIT-licensed code by Mark Woodbridge
"""

import getpass  # for secure password retrieval
import json  # convert json to python dict
import os  # access environment variables
import smtplib  # send emails
import ssl  # network stuff
import urllib.request  # fetch file from url
import geopy  # turn location into lat/long
from geopy.geocoders import Nominatim

def env_setup():
    """Get parameters from environment variables,
    else get them from stdin.
    """
    # email-sending parameters
    email = (os.environ["EMAIL"] if "EMAIL" in os.environ 
        else input("Log in to send an email.\nEmail: "))
    password = (os.environ["PASSWORD"] if "PASSWORD" in os.environ 
        else getpass.getpass(prompt='Password: '))
    recipient = (os.environ["RECIPIENT"] if "RECIPIENT" in os.environ 
        else input("Recipient email: "))
    # convert location to lat-long
    locationstring = (os.environ["LOCATION"] if "LOCATION" in os.environ 
        else input("Location: "))
    locator = Nominatim(user_agent="myGeocoder")
    loc = locator.geocode(locationstring)
    return email, password, recipient, loc

def get_weather(loc):
    """Fetch weather data from Meteorologisk Institutt."""
    url = (f"https://api.met.no/weatherapi/locationforecast/"
        f"2.0/compact?lat={loc.latitude}&lon={loc.longitude}")
    with urllib.request.urlopen(url) as fp:
        forecast = json.load(fp)
        precipitation = (forecast["properties"]["timeseries"][0]["data"]
            ["next_6_hours"]["details"]["precipitation_amount"])
        return precipitation

def send_email(precipitation, loc, email, password, recipient):
    """Log into server and send an email with precipitation forecast."""
    msg = (f"Subject: Don\'t forget your umbrella!\n"
        f"\n{precipitation}mm of precipitation is forecast in {loc.address}.")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
        server.login(email, password)
        server.sendmail(email, recipient, msg)

if __name__ == "__main__":
    email, password, recipient, location = env_setup()
    precipitation = get_weather(location)
    if precipitation > 0:
        send_email(precipitation, location, email, password, recipient)

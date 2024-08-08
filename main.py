import time
import requests
import datetime as dt
import smtplib
import pytz

tz = pytz.timezone('Europe/Berlin')
berlin_now_hour = dt.datetime.now(tz).hour


my_email = "blatan334@gmail.com"
my_password = "frsmxbpbprgmqwgm"
LATITUDE_BERLIN = 52.520008
LONGITUDE_BERLIN = 13.404954

while True:
    time.sleep(60)
    # -------------------- ISS POSITION-----------------------------------
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_response.json()

    iss_lat = float(iss_response.json()["iss_position"]["latitude"])
    iss_lng = float(iss_response.json()["iss_position"]["longitude"])
    print(iss_lat)
    parameters = {
        "lat": LATITUDE_BERLIN,
        "lng": LONGITUDE_BERLIN,
        "formatted": 0
    }
    # -----------------------SUNRISE & SUNSET in Berlin ----------------
    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()

    sunrise = sun_response.json()["results"]["sunrise"]
    sunrise = int((sunrise.split("T")[1].split(":")[0]))

    sunset = sun_response.json()["results"]["sunset"]
    sunset = int((sunset.split("T")[1].split(":")[0]))

    # -----------------------Check if ISS near Berlin ----------------
    # Check if Latitude is near Berlin
    if LATITUDE_BERLIN + 2 >= iss_lat >= LATITUDE_BERLIN - 2:
        lat_near_enough = True
    else:
        last_near_enough = False

    # Check if Longitude is near Berlin
    if LONGITUDE_BERLIN + 2 >= iss_lng >= LONGITUDE_BERLIN - 2:
        lng_near_enough = True
    else:
        lng_near_enough = False

    # ----------------------- Check if dark in now Berlin ----------------

    if berlin_now_hour >= sunset or berlin_now_hour <= sunrise:
        is_dark = True
    else:
        is_dark = False

    # ----------------------- Send notifying EMAIL ----------------
    if lng_near_enough and lng_near_enough and is_dark:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email,
                             password=my_password)
            connection.sendmail(to_addrs=my_email,
                                from_addr=my_email,
                                msg="Subject: ISS overhead\n\n ISS is above Berlin, get out and look")
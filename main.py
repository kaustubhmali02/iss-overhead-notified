import requests
import datetime as dt
import smtplib
import time

EMAIL = "Your Email"
PASSWORD = "Your Password"

MY_LONGITUDE = 72.964256
MY_LATITUDE = 19.199560


def is_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if MY_LATITUDE - 5 <= iss_latitude <= MY_LATITUDE + 5 and MY_LONGITUDE - 5 <= iss_longitude <= MY_LONGITUDE + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0
    }

    response = requests.get(url=f"https://api.sunrise-sunset.org/json",
                            params=parameters)
    response.raise_for_status()
    data = response.json()
    # print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


try:
    while True:
        time.sleep(60)
        if is_near() and is_near():
            with smtplib.SMTP(host="smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(EMAIL, PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=EMAIL,
                    msg="Subject: Lookup\n\n"
                        "ISS is Over head")

except KeyboardInterrupt as error:
    print("Stopped by the user")

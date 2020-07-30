import tweepy, requests, json, logging
from datetime import datetime
LOG_FILENAME = "twipy.log"
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)  
url = "http://api.openweathermap.org/data/2.5/weather?zip=14469,US&appid=6f521a9d2ef90c3cab501db55d64c0ea"

response = requests.get(url)

x = response.json()
logging.info("Got a response.   " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))
if x["cod"] != "404":
    y = x["main"]

    current_temp = y["temp"]

    current_pressure = y["pressure"]

    current_humidity = y["humidity"]

    z = x["weather"]

    w_description = z[0]["description"]

    a = x["wind"]
    
    wind_speed = a["speed"]
    #convert wind speed (m/s) to mph
    wind_mph = wind_speed/0.4470
    #convert wind direction to the cardinal format from degrees
    wind_direction = a["deg"]
    if wind_direction > 348.75 or wind_direction < 11.25:
        card_direction = "N"
    elif wind_direction > 11.25 and wind_direction < 78.75:
        card_direction = "NE"
    elif wind_direction > 78.75 and wind_direction < 101.25:
        card_direction = "E"
    elif wind_direction > 101.25 and wind_direction < 168.75:
        card_direction = "SE"
    elif wind_direction > 168.75 and wind_direction < 191.25:
        card_direction = "S"
    elif wind_direction > 191.25 and wind_direction < 258.75:
        card_direction = "SW"
    elif wind_direction > 258.75 and wind_direction < 281.25:
        card_direction = "W"
    elif wind_direction > 281.25 and wind_direction < 348.75:
        card_direction = "NW"
    else:
        logging.warning("Invalid wind direction.    " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))

    #convert temps to both c and f
    c_temp = current_temp - 273.15
    f_temp = 1.8*(current_temp - 273) + 32
    try:
        b = x["visibility"]
        b = b * 0.00062137119223733
        b = str("{0:.2f}".format(b) + " miles")
    except:
        logging.warning("Visibility data not available.  " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))
        b = "Not available right now"
    
else:
    logging.error("City does not exist  " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))
    
auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    logging.info("Authenticaiton OK " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))
except:
    logging.error("Error during authentication  " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))
api.update_status("Current weather for the [your area here] area:\nTemperature: " + str("{0:.2f}".format(c_temp)) + "°C   " + str("{0:.2f}".format(f_temp)) + "°F" +
"\nAtmospheric pressure: " + str(current_pressure) + " hPa" + 
"\nHumidity: " + str(current_humidity) + "%" + 
"\nWind speed: " + str("{0:.2f}".format(wind_mph)) + " mph in the direction of " + card_direction + 
"\nVisibility: " + b + 
"\n\n" + w_description.capitalize())
logging.info("Updated status with: \n" + "Current weather for the Canandaigua area:\nTemperature: " + str("{0:.2f}".format(c_temp)) + "°C   " + str("{0:.2f}".format(f_temp)) + "°F" +
"\nAtmospheric pressure: " + str(current_pressure) + " hPa" + 
"\nHumidity: " + str(current_humidity) + "%" + 
"\nWind speed: " + str("{0:.2f}".format(wind_mph)) + " mph in the direction of " + card_direction + 
"\nVisibility: " + b + 
"\n\n" + w_description.capitalize() + " " + datetime.now().strftime('%H_%M_%S_%d_%m_%Y'))

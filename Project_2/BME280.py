import smbus2 
import bme280 
import time
from datetime import datetime 
import csv 

from arduino_iot_cloud import ArduinoCloudClient

def read_value(client):

    try: 
        # Read sensor data 
        data = bme280.sample(bus, address, calibration_params) 
 
        # Extract temperature, pressure, humidity, and corresponding timestamp 
        temperature_fahrenheit = round((data.temperature * 1.8) + 32, 2)
        humidity = round(data.humidity, 2)
        pressure = round(data.pressure, 2)

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        file = open('/media/sidkcl/My Passport/kroger_2/data.csv','a')
        writer = csv.writer(file, delimiter=',')
        values = [timestamp, temperature_fahrenheit, humidity, pressure]
        writer.writerow(values)
        file.close()

        return pressure
    
    except KeyboardInterrupt: 
        print('Program stopped') 
    except Exception as e: 
        print('An unexpected error occurred:', str(e)) 

DEVICE_ID = b"(id)"
SECRET_KEY = b"(key)"

# BME280 sensor address (default address) 
#sudo i2cdetect -y 1s
address = 0x77
 
# Initialize I2C bus 
bus = smbus2.SMBus(1) 
 
# Load calibration parameters 
calibration_params = bme280.load_calibration_params(bus, address) 

#Create Arduino Cloud connection
client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

# Register the Arduino Cloud aariable with the callback function
client.register("pressure", on_read=read_value, interval=60.0)

#Start the client
client.start()
 

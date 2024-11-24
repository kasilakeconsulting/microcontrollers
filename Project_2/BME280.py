import smbus2 
import bme280 
import time 
from datetime import datetime 
import csv
 
# BME280 sensor address (default address) 
# sudo i2cdetect -y 1s
address = 0x77
 
# Initialize I2C bus 
bus = smbus2.SMBus(1) 
 
# Load calibration parameters 
calibration_params = bme280.load_calibration_params(bus, address) 
 
# Create a variable to control the loop 
running = True 

# Loop forever 
while running: 
    try: 
        # Read sensor data 
        data = bme280.sample(bus, address, calibration_params) 
 
        temperature_fahrenheit = round((data.temperature * 1.8) + 32, 2)
        humidity = round(data.humidity, 2)
        pressure = round(data.pressure, 2)
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        file = open('/media/sidkcl/My Passport/project_2/data.csv','a')
        writer = csv.writer(file, delimiter=',')
        values = [timestamp, temperature_fahrenheit, humidity, pressure]
        writer.writerow(values)
        file.close()
      
        time.sleep(30) 
 
    except KeyboardInterrupt: 
        print('Program stopped') 
        running = False 
    except Exception as e: 
        print('An unexpected error occurred:', str(e)) 
        running = False 
 
file.close()

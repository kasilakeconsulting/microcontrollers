import requests 
import json 
import time 
from datetime import datetime 
import csv
from flask import Flask, request 

app = Flask(__name__) 
@app.route('/data', methods=['GET']) 
def handle_data(): 

    # Get a new bearer token. 

    url = "https://api2.arduino.cc/iot/v1/clients/token" 
    payload = 'audience=https%3A%2F%2Fapi2.arduino.cc%2Fiot&client_id=(id)&client_secret=(secret)&grant_type=client_credentials' 
    headers = { 

        'Content-Type': 'application/x-www-form-urlencoded', 

        'Authorization': 'Bearer (token)' 

    } 
    response = requests.request("POST", url, headers=headers, data=payload) 

    if response is not None: 
        responseJSON = json.loads(response.text) 
        token = responseJSON['access_token'] 
    
        url = "https://api2.arduino.cc/iot/v2/things/(thing id)/properties/(temperature property id)" 
        payload = {} 
        files = {} 
        headers = { 
            'Authorization': 'Bearer ' + token 
        } 

        response = requests.request("GET", url, headers=headers, data=payload, files=files) 
        responseJSON = json.loads(response.text) 
        temperature = responseJSON['last_value'] 

        url = "https://api2.arduino.cc/iot/v2/things/(thing id)/properties/(humidity property id)" 
        payload = {} 
        files = {} 
        headers = { 
            'Authorization': 'Bearer ' + token 
        } 

        response = requests.request("GET", url, headers=headers, data=payload, files=files) 
        responseJSON = json.loads(response.text) 
        humidity = responseJSON['last_value'] 

        temperatureStr = f"{temperature:.1f}"
        humidityStr = f"{humidity:.1f}"

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        timeminute = now.strftime("%H:%M")

        file = open('/media/sidkcl/My Passport/kroger_3/data.csv','a')
        writer = csv.writer(file, delimiter=',')

        values = [timestamp, temperatureStr, humidityStr]
        writer.writerow(values)

        file.close()

        data = {
            'time':timeminute,
            'temperature': temperatureStr, 
            'humidity': humidityStr 
        } 

        dataJSON = json.dumps(data) 
        return dataJSON, 200 

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8000) 

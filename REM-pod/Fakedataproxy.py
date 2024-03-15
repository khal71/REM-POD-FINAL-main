import requests
import random
from datetime import datetime
import time



api_endpoint = 'https://rem-pod-app.azurewebsites.net/REM_POD_'
 


#api_endpoint = 'http://localhost:5263/REM_POD_'  


def send_data(data):
    try:
      
        response = requests.post(api_endpoint, json=data)
        response.raise_for_status()
        print("Data sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

def generate_random_data():
    temperature = random.uniform(-10, 40)
    magnetometer = random.uniform(0, 10)
    distance = random.uniform(0, 300)
    return {
        #'id': None,  
        'timestamp': datetime.now().isoformat(),
        'temperature': temperature,
        'magnetometer': magnetometer,
        'distance': distance
    }


if __name__ == "__main__":
    while True:
        data = generate_random_data()
        if data['temperature'] < 0 or data['temperature'] > 35 or \
           data['magnetometer'] > 7.5 or data['distance'] < 30:
            send_data(data)
        time.sleep(15)  

      

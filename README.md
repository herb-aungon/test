
The following will need to be installed before running the Weather Api
1. Virtual Environment
  - Acitivate Virutal Environment Created onced installed
2. Install Flask / pip install what is listed on the requirements.txt
    -run Flask app (weather_service_complete.py). Run the code below: 
      -export FLASK_APP=weather_service_complete.py
      -flask run --host=0.0.0.0 (make the server publicly)
      
To access the Weather API running:
1. check and get your IP Address 
  -run the following command for linux/ubuntu ifconfig
  -run the following command for windows ipconfig
2. enter ip address at the web browser's address bar (e.g. http://192.168.33.10:5000/forecast/city (for weather forecast for specific city and http://192.168.33.10:5000/forecast/city/date/temperature_format) 
  -accepted temperature format (metric, imperial and kelvin)
  *for better result use postman extension fo chrome and access the following app routes 

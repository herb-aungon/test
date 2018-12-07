from flask import Flask
from datetime import datetime
import json
import requests
import datetime


app = Flask(__name__)

open_weather_id = '42aea4b1b6c2867215515c367b7a82e5'

#display error message 
@app.errorhandler( 500 )
def internal_500_error( exception ):
    resp = {
        'error':'Something went wrong',
        'error_code':'Internal Server Error'
    }
    return json.dumps(resp)

@app.errorhandler( 404 )
def internal_404_error( exception ):
    resp = {
        'error':'Something went wrong',
        'error_code':'URL not found'
    }
    return json.dumps(resp)



#main route for testing purposes and getting the main part working
@app.route('/forecast',methods = ['GET'])
def index():
    try:
        url_raw = 'http://api.openweathermap.org/data/2.5/weather/?q={}&units=metric&appid='
        city = 'London'
        url = url_raw + open_weather_id
        raw_data = requests.get(url.format(city)).json()
        format_data = {
            "city":raw_data['name'],
            "humidity":raw_data['main']['humidity'],
            "pressure":raw_data['main']['pressure'],
            "temperature":raw_data['main']['temp'],
            "weather":raw_data['weather'][0]['main']
        }
        resp = json.dumps (format_data, indent = 4)
    except Exception as e:
        resp = "Error! %s " % e
        

    return resp



@app.route('/forecast/<city>/<date_weather_check>',methods = ['GET'])
def main(city, date_weather_check):
    try:
        
        date_format = '%d-%m-%Y'
        date_validate = datetime.datetime.strptime(date_weather_check, date_format)
        
        check_date_range = datetime.datetime.now() - date_validate
        if check_date_range.days > 0 and check_date_range.days < 16:
            val = check_date_range.days
            #url_raw = '%s&cnt={%s}' % (open_weather_id,val)
            url_raw = 'http://api.openweathermap.org/data/2.5/weather/?q={}&units=metric&appid='
            add_date = '&cnt=%s' % val
            url = url_raw + open_weather_id + add_date
            raw_data = requests.get(url.format(city)).json()
            format_data = {
                "city":raw_data['name'],
                "humidity":raw_data['main']['humidity'],
                "pressure":raw_data['main']['pressure'],
                "temperature":raw_data['main']['temp'],
                "weather":raw_data['weather'][0]['main'],
                "weather forecast for" :date_weather_check
            }
            
            resp = json.dumps (format_data, indent = 4)            




        elif check_date_range.days > 16:
            resp ="Date is older than 16 days. No data Found"
        else:
            resp = "Invalid Date. Please check the date entered"
        #raw_data = requests.get(url.format(city)).json()


    except Exception as e:
        resp = "Error! %s " % e
        

    return resp



@app.route('/forecast/test',methods = ['GET'])
def main_():
    try:
        city='london'
        url_raw = 'http://api.openweathermap.org/data/2.5/weather/?q={}&units=metric&appid='
        url = url_raw + open_weather_id
        raw_data = requests.get(url.format(city)).json()
        resp = json.dumps (raw_data, indent = 4)            
        
    except Exception as e:
        resp = "Error! %s " % e
        

    return resp

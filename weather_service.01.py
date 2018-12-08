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
        if check_date_range.days > 0 and check_date_range.days < 6:
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




        elif check_date_range.days > 6:
            resp ="Date (%s)is older than 6 days. No data Found -%s" % (date_weather_check, check_date_range)
        else:
            resp = "Invalid Date(%s). Please check the date entered -%s" % (date_weather_check, check_date_range)
        #raw_data = requests.get(url.format(city)).json()


    except Exception as e:
        resp = "Error! %s " % e
        

    return resp



@app.route('/hi/<place>/<date_check>',methods = ['GET'])
def main_(place, date_check):
    
    try:        
        url_raw = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid='
        url = url_raw + open_weather_id
        
        raw_data = requests.get(url.format(place)).json()
        day_1 = raw_data['list'][0]
        five_day_forecast_data ={
            day_2 = raw_data['list'][10]
            temp_1 = {
                "date":day_1['dt_txt'],
                "city":raw_data['city']['name'],
                "clouds":day_1['weather'][0]['description'],
                "pressure":day_1['main']['pressure'],
                "temperature":day_1['main']['temp'],
                "humidity":day_1['main']['humidity']
            }        

            day_2 = raw_data['list'][10]
            temp_2 = {
                "date":day_2['dt_txt'],
                "city":raw_data['city']['name'],
                "clouds":day_2['weather'][0]['description'],
                "pressure":day_2['main']['pressure'],
                "temperature":day_2['main']['temp'],
                "humidity":day_2['main']['humidity']
            }        

        }
        
        date_format = '%Y-%m-%d'
        date_validate = datetime.datetime.strptime(str(date_check), date_format)
        d_t = str(date_validate)
        d_t = d_t.split()


        
        # five_day_dates = {
        #     'day_1' : str(raw_data['list'][0]['dt_txt'].split()[0]),
        #     'day_2' : str(raw_data['list'][9]['dt_txt'].split()[0]),
        #     'day_3' : str(raw_data['list'][17]['dt_txt'].split()[0]),
        #     'day_4' : str(raw_data['list'][24]['dt_txt'].split()[0]),
        #     'day_5' : str(raw_data['list'][32]['dt_txt'].split()[0]),
        #     'day_5' : str(raw_data['list'][38]['dt_txt'].split()[0])
        # }

        five_day_dates = [
         str(raw_data['list'][0]['dt_txt'].split()[0]),
         str(raw_data['list'][9]['dt_txt'].split()[0]),
         str(raw_data['list'][17]['dt_txt'].split()[0]),
         str(raw_data['list'][24]['dt_txt'].split()[0]),
         str(raw_data['list'][32]['dt_txt'].split()[0]),
         str(raw_data['list'][38]['dt_txt'].split()[0])
        ]
        if  d_t[0] in five_day_dates:
            result = True
            msg = "Weather forecast data found" 

        else:
            result = True
            msg = "Date out of range (%s). Weather App only support +5 days from the current date" %  d_t[0]


        msg ={
            'data':'',
            'result':'',
            'message':msg,
            'test2': d_t[0]
        }
        resp = json.dumps (msg, indent = 4)            


    except Exception as e:
        resp = "Error! %s " % e
        

    return resp

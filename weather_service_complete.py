from flask import Flask
from datetime import datetime
import json
import requests
import datetime


app = Flask(__name__)

#id 
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




#main route for getting weather forecast (city, date and temp)
@app.route('/forecast/<city>/<date_check>/<temp_format>',methods = ['GET'])
def main_(city, date_check, temp_format):
    
    try:
        #used for response purpose. Value will be amended with response data or none
        get_data = None
        #check temp_format value if it exists within the supported temperature format
        temp_format_check  =[
            'metric',
            'imperial'
        ]
        if temp_format in temp_format_check:
            url_raw = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=%s&appid=' % temp_format
        else:
            #if temperature format is not support, default temperature format is set (Kelvin)
            url_raw = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid='

        #complete url for getting data
        url = url_raw + open_weather_id

        #getting data response
        raw_data = requests.get(url.format(city)).json()

        #gathers data for 5 day forecast and only get the necessary fields.
        raw_city = raw_data['city']['name']
        
        day_1 = raw_data['list'][0]
        dict_name_1 = 'temp_%s' % day_1['dt_txt'].split()[0]
        
        day_2 = raw_data['list'][10]
        dict_name_2 = 'temp_%s' % day_2['dt_txt'].split()[0]

        day_3 = raw_data['list'][19]
        dict_name_3 = 'temp_%s' % day_3['dt_txt'].split()[0]

        day_4 = raw_data['list'][24]
        dict_name_4 = 'temp_%s' % day_4['dt_txt'].split()[0]

        day_5 = raw_data['list'][36]
        dict_name_5 = 'temp_%s' % day_5['dt_txt'].split()[0]

        
        five_day_forecast_data ={
    
            dict_name_1 : {
                "date":day_1['dt_txt'],
                "city":raw_city,
                "clouds":day_1['weather'][0]['description'],
                "pressure":day_1['main']['pressure'],
                "temperature":day_1['main']['temp'],
                "humidity":day_1['main']['humidity']
            },        


            dict_name_2 : {
                "date":day_2['dt_txt'],
                "city":raw_city,
                "clouds":day_2['weather'][0]['description'],
                "pressure":day_2['main']['pressure'],
                "temperature":day_2['main']['temp'],
                "humidity":day_2['main']['humidity']
            },
            dict_name_3 : {
                "date":day_3['dt_txt'],
                "city":city,
                "clouds":day_3['weather'][0]['description'],
                "pressure":day_3['main']['pressure'],
                "temperature":day_3['main']['temp'],
                "humidity":day_3['main']['humidity']
            },
            dict_name_4 : {
                "date":day_4['dt_txt'],
                "city":raw_city,
                "clouds":day_4['weather'][0]['description'],
                "pressure":day_4['main']['pressure'],
                "temperature":day_4['main']['temp'],
                "humidity":day_4['main']['humidity']
            },

            dict_name_5 : {
                "date":day_5['dt_txt'],
                "city":raw_city,
                "clouds":day_5['weather'][0]['description'],
                "pressure":day_5['main']['pressure'],
                "temperature":day_5['main']['temp'],
                "humidity":day_5['main']['humidity']
            }

        }
        #validates the data entered
        date_format = '%Y-%m-%d'
        date_validate = datetime.datetime.strptime(str(date_check), date_format)
        #removes time from dates for checking results
        d_t = str(date_validate)
        d_t = d_t.split()

        #get and stores dates from response data. used to check if date entered is withing range
        five_day_dates = [
         str(raw_data['list'][0]['dt_txt'].split()[0]),
         str(raw_data['list'][10]['dt_txt'].split()[0]),
         str(raw_data['list'][19]['dt_txt'].split()[0]),
         str(raw_data['list'][24]['dt_txt'].split()[0]),
         str(raw_data['list'][36]['dt_txt'].split()[0])
        ]

        #check and get data for specific date weather forcast
        if  d_t[0] in five_day_dates:
            result = True
            msg_ = "Weather forecast data found" 
            get_data = five_day_forecast_data.get('temp_%s' % d_t[0])
        else:
            result = True
            msg_ = "Date out of range (%s). Weather App only support +5 days from the current date" %  d_t[0]


        msg ={
            'data':get_data,
            'message':msg_
        }

        #testing purpose to check data gathered
        # msg ={
        #     'data':five_day_forecast_data,
        #     'result':five_day_dates,
        #     'message':msg_,
        #     'test2': dict_name_1,
        #     'test3':get_data
        # }
        resp = json.dumps (msg, indent = 4)            


    except Exception as e:
        msg ={
            'data':get_data,
            'message':"Something went wrong.Error! %s " % e
        }
        resp = json.dumps (msg, indent = 4)            

            

    return resp



@app.route('/forecast/<city>',methods = ['GET'])
def main(city):
    try:
        url_raw = 'http://api.openweathermap.org/data/2.5/weather/?q={}&units=metric&appid='
        url = url_raw + open_weather_id
        raw_data = requests.get(url.format(city)).json()
        format_data = {
            "city":raw_data['name'],
            "humidity":raw_data['main']['humidity'],
            "pressure":raw_data['main']['pressure'],
            "temperature":raw_data['main']['temp'],
            "clouds":raw_data['weather'][0]['main']
        }

        msg ={
            'data':format_data,
            'message':"Weather forecast data found"
        }


    except Exception as e:
        test = str(e)
        if test.replace("'", "") == "name":
            e = "City not found"
        else:
            e = e
        msg ={
            'data':None,
            'message':"Error! %s " % e
        }

    resp = json.dumps (msg, indent = 4)                    

    return resp


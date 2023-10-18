import json
import os
import requests
import boto3
import datetime

def lambda_handler(event, context):
    current_time = datetime.datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    sns = boto3.client('sns')

    try:
        #DOWNLOAD THE WEATHER DATA FIRST!
        # Make API request
        lat = 45.06832229980975  # latitude
        lon = 7.636441878389062  # longitude
        API_key = API_key
        part = "daily,hourly"
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_key}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        ######This part parses the weather data######
        
        timezone = data.get("timezone")
        current_weather = data.get("current")
        temp = current_weather['temp'] - 273.15
        temp = "{:.2f}".format(temp)
        heat_index = current_weather["feels_like"] - 273.15
        heat_index = "{:.2f}".format(heat_index)
        humidity = current_weather["humidity"]
        dew_point = current_weather["dew_point"] - 273.15
        dew_point = "{:.2f}".format(dew_point)
        alerts = (data.get("alerts"))[0]
        weather_situation = alerts["event"]

        Weather_message = f"This is a weather notification message. Temperature is {temp}. Heat index is {heat_index}. Humidity is {humidity}%. The dew point is {dew_point}. The overall weather situation can be described as {weather_situation}."
        print(Weather_message)

        if "warning" in weather_situation.lower():
            response = sns.publish(
                TopicArn='SNS Topic ARN',
                Message=Weather_message
            )
            
        ####TELEGRAM BOT CODE####    
        request_body = json.loads(event['body'])
        BOT_TOKEN = os.environ.get('TOKEN')
        BOT_CHAT_ID = os.environ.get('CHATID')
        command = request_body['message']['text'].strip('/')

        if command == 'start':
            message = "Welcome to the weather notification bot. You can receive real-time weather data."
        elif command == 'help':
            message = "Here are the available commands: /start, /help, /weather"
        elif command == 'weather': 
            message = Weather_message

            Telegram_Msg = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + str(BOT_CHAT_ID) + \
            '&text=' + message
            response = requests.po(Telegram_Msg)
            print(Telegram_Msg)
                
        else:
            message = "I'm sorry, I didn't understand that command. Please try again."

        return {
            'statusCode': 200,
            'body': json.dumps('Message sent to Telegram!')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

import speech_recognition as sr
from datetime import datetime
from gtts import gTTS
import webbrowser
import playsound
import requests
import os


# speech recognition
def speak(text):
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    tts = gTTS(text=text)
    filename = "voice" + date_string + ".mp3"
    tts.save(filename)
    playsound.playsound(filename)


def get_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        audio = r.listen(source)
        said = ""

        try:
            r.recognize_google(audio)
        except sr.UnknownValueError:
            print("could not understand audio")
        except sr.RequestError as e:
            print("error; {0}".format(e))

            return said


# get current weather
def current_weather():
    api_key = "4898e54c3108f13bce4bfd3b0d526c3f"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = 'Dubai'

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)

    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperatureK = y["temp"]
        current_temperatureC = (int(current_temperatureK) - 273.15)

        # store the value corresponding
        # to the "humidity" key of y
        current_humidity = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        weather = (" the Temperature is (in Celsius):  " +
                   str(current_temperatureC) +
                   "\n the humidity is (in percentage):  " +
                   str(current_humidity) +
                   "\n today appears to be:   " +
                   str(weather_description))
        speak('today\'s weather is: ' + weather)
    else:
        print('city not found')
        speak('city not found')


# function for Virtual Assistant
def virtual_assistant():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello,Good Morning Maxim")
    elif 12 <= hour < 18:
        speak("Hello,Good Afternoon Maxim")
    else:
        speak("Hello,Good Evening Maxim")

    text = get_speech()

    if 'hello' in text:
        speak('Hello, how can i help you today?')
    elif 'name' in text:
        speak('My name is sam')
    elif 'google' in text:
        webbrowser.open('https://www.google.com/')
    elif 'youtube' in text:
        webbrowser.get('chrome').open('https://www.youtube.com')
    elif 'shutdown' in text:
        os.system('shutdown -s')
    elif 'current time' in text:
        time = (datetime.today().strftime("%I:%M %p"))
        speak('the time is: ' + time)
    elif 'today\'s date' in text:
        date = (datetime.today().strftime('%d-%m-%Y'))
        speak('today\'s date is: ' + date)
    elif 'weather' in text:
        current_weather()
    elif 'goodbye' in text:
        speak('goodbye, maxim have a nice day')
        quit()


virtual_assistant()

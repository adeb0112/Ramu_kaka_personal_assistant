from __future__ import unicode_literals
import urllib.request
import urllib.parse
import re
import os 
import subprocess
import win32com.client as wincl
import speech_recognition as sr
import pythoncom
import json
import pafy
from pygame import mixer
from pytube import YouTube
from weather import Weather
import pafy
import subprocess
from pygame import mixer # Load the required library
import time

def weather_telecast():
    f = urllib.request.urlopen('http://freegeoip.net/json/')
    json_string = f.read().decode()
    f.close()
    location = json.loads(json_string)
    print(location)
    location_city = location['city']    
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak("Weather forecast for your city" + location_city + "is")
    #location_state = location['region_name']
    #location_country = location['country_name']
    weather = Weather()
    location = weather.lookup_by_location(location_city)
    forecasts = location.forecast()
    speak.Speak('For Today highest temperature is'+str(int((int(forecasts[0]['high'])-32)/1.8))+'degree celcius, lowest temperature is'+str(int((int(forecasts[0]['low'])-32)/1.8))+'degree celcius and the weather is'+forecasts[0]['text'])
    speak.Speak('For tommorow highest temperature will be'+str(int((int(forecasts[1]['high'])-32)/1.8))+'degree celcius, lowest temperature will be'+str(int((int(forecasts[1]['low'])-32)/1.8))+'degree celcius and the weather will be'+forecasts[1]['text'])
    
    
    
def news_broadcast():
    direct_output1 = subprocess.check_output('news the-hindu', shell=True)
    print(direct_output1)
    direct_output2 = direct_output1.decode(encoding='UTF-8')
    text = re.sub(r'33m\S+', 'Next News',  direct_output2)
    text = re.sub(r"32m", '',  text)
    text = re.sub(r"0m", '',  text)
    last_index = text.rfind("Next News")
    text = text[:last_index-1]
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(text)
    

def download_audio(txt):
    txt = txt.replace(' ','+')
    html_content = urllib.request.urlopen("http://www.youtube.com/results?search_query="+txt)
    
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())    
    url = "http://www.youtube.com/watch?v=" + search_results[0]        
    video = pafy.new(url)
    duration = video.length
    print(duration)
    audiostreams = video.audiostreams
    for x in audiostreams:
        if x.extension.find("m4a")!=-1:
            break
    x.download(filepath="./pkg." + x.extension)
    process = subprocess.Popen(r"C:\\ffmpeg\\bin\\ffmpeg.exe -i .\pkg.m4a .\pkg.ogg", shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
    mixer.init()
    mixer.music.load(r".\pkg.ogg")
    mixer.music.play()
    time.sleep(duration)
    mixer.music.stop()
    os.remove(r".\pkg.m4a")
    os.remove(r".\pkg.ogg")
    
    #audiostreams[0].download()
    



pythoncom.CoInitialize()
r = sr.Recognizer()
m = sr.Microphone()
#set threhold level
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))
# obtain audio from the microphone
while 1 :
        
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.record(source, duration = 10, offset = 1)
    print("Listen Completed")
    try :
        speech_to_text = r.recognize_google(audio)
    except :
        continue
    print(speech_to_text)
    if(speech_to_text.lower().find("ramu kaka")!=-1 or speech_to_text.lower().find("ramukaka")!=-1):
        if(speech_to_text.find("timer")!=-1):
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak("Janab, Timer set up")
            
                
        elif(speech_to_text.find("news")!=-1):
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak("Here's News broadcasst")
            news_broadcast()
        
        
            
        elif(speech_to_text.find("weather")!=-1):
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak("Janab, weather set up")
            weather_telecast()
        
        
        
        elif(speech_to_text.find("song")!=-1):
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak("Janab, downloading song")
            download_audio(speech_to_text[speech_to_text.find("song")+4:])
            
        else
            speak.Speak("Janab, disn't understand what you said")
            
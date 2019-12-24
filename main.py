import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import yfinance as yf # to fetch financial data
import ssl
import certifi
import time
import os # to remove created audio files

class person:
    name = ''
    def setName(self, name):
        self.name = name

r = sr.Recognizer() # initialise a recogniser

# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source: # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(voice_data.lower()) # print what user said
        return voice_data.lower()

# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(audio_string) # print what app said
    os.remove(audio_file) # remove audio file

def respond(voice_data):

    #if 'hey' in voice_data or "hi" in voice_data:
    #    greetings = ["hey, how can I help you","hey, what's up?","Hi, Reza","I'm listening","how can I help you?"]
    #    greet = greetings[random.randint(0,len(greetings)-1)]
    #    speak(greet)
    # 1: greeting
    for term in ['hey','hi','hello']:
        if term in voice_data:
            greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
            greet = greetings[random.randint(0,len(greetings)-1)]
            speak(greet)
            break

    # 2: name
    if 'what is your name' in voice_data or "what's your name" in voice_data:
        speak("my name is kiri. what's your name?")

    if 'my name is' in voice_data:
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)

    # 3:
    if 'how are you' in voice_data or "how are you doing?" in voice_data:
        speak("I'm very well, thanks for asking Reza")

    # 4: time
    if "what's the time" in voice_data or "tell me the time" in voice_data or "what time is it" in voice_data:
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)

    # 5: search google
    if 'search for' in voice_data and 'youtube' not in voice_data:
        #search_term = record_audio('what do you wanna search for?')
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term}')

    # 6: search youtube
    if 'youtube' in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    # 7: get stock price
    if "price of" in voice_data:
        search_term = voice_data.lower().split(" of ")[-1].strip() #strip removes whitespace after/before a term in string
        stocks = {
            "apple":"AAPL",
            "microsoft":"MSFT",
            "facebook":"FB",
            "tesla":"TSLA",
            "bitcoin":"BTC-USD"
        }
        stock = stocks[search_term]
        stock = yf.Ticker(stock)
        price = stock.info["regularMarketPrice"]

        speak(f'price of {search_term} is {price} {stock.info["currency"]}')

    # : exit
    if 'exit' in voice_data:
        exit()


time.sleep(1)

person_obj = person()
while(1):
    voice_data = record_audio() # get the voice input
    respond(voice_data) # respond



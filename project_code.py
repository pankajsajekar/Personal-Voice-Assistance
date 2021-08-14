import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from tkinter import Button
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import random
import os
import pyautogui
import requests
import time
import threading
from pyowm import OWM

engine = pyttsx3.init()
#init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

root1 = tk.Tk()

tk.Label(root1,
         text="RO-BROS",
         fg="white",
         bg="#000000",
         font="Algerian 40 bold italic").place(relx=0.16, rely=0.20)

tk.Label(root1,
         text="(Personal Voice Assistance)",
         fg="white",
         bg="#000000",
         font="Times 20").place(relx=0.05, rely=0.35)

tk.Button(root1,
          text="Next",
          bg="#ABB2B9",
          fg="#000000",
          font="Arebic 14",
          width=19,
          command=lambda: mainpage()
          ).place(relx=0.20, rely=0.85, relheight=0.07, relwidth=0.60, )

def mainpage():
    root1.destroy()
    root = tk.Tk()

    def switch():
        keyboardbtn.destroy()
        recognition1.destroy()
        settingbtn.destroy()

        def display_msg(event):
            msg = entryMsg.get()
            if not msg:
                return
            if 'Type here...' in msg:
                return
            entryMsg.delete(0, "end")
            msg2 = data(msg)
            text_chatbox.config(state=NORMAL)
            text_chatbox.insert(END, "You : " + msg + "\n")
            text_chatbox.insert(END, "Bro : " + msg2 + "\n\n")
            text_chatbox.config(state=DISABLED)
            text_chatbox.see(END)

        def switch1():
            entryMsg.destroy()
            mic_btn.destroy()
            keyboardbtn = Button(labelBottom, text="keyboard", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                                 command=lambda: switch())
            keyboardbtn.place(relx=0.008, rely=0.002, relheight=0.05, relwidth=0.22, )
            recognition1 = Text(labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 14")
            recognition1.place(relwidth=0.50, relheight=0.05, rely=0.002, relx=0.008, x=114)
            settingbtn = Button(labelBottom, text="mic", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                                command=lambda: mic_fun())
            settingbtn.place(relx=0.77, rely=0.002, relheight=0.05, relwidth=0.22)

            def mic_fun():
                query = takeCommand().lower()
                res = data(query)
                text_chatbox.config(state=NORMAL)
                text_chatbox.insert(END, "You : " + query + "\n")
                text_chatbox.insert(END, "Bro : " + res + "\n\n")
                text_chatbox.config(state=DISABLED)
                text_chatbox.see(END)

            def takeCommand():
                r = sr.Recognizer()
                while True:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        r.pause_threshold = 0.8
                        audio = r.listen(source)
                        print("Listening...")


                    try:
                        print("Recognizning......")

                        query = r.recognize_google(audio, language='en-in')
                        print(f"You said: {query}\n")
                        query = query.lower()

                    except Exception as e:
                        print(e)
                        speak("say that again please.....")
                        return "none"
                    return query

            def speak(audio):
                print(audio)
                engine.say(audio)
                engine.runAndWait()
                return audio

            def web_scraping(query):
                res = speak("Serching " + query + "")
                return res

            def data(query):
                # if __name__ == "__main__":
                # wishme()
                while True:
                    if query != None:

                        if 'time' in query:
                            Time = datetime.datetime.now().strftime("%I:%M:%S")
                            res = speak("Sir Current time is " + Time)

                        elif 'date' in query:
                            strdate = datetime.datetime.today().strftime("%d-%m-%y")
                            res = speak("Sir today's date is %s" % strdate)

                        elif 'say hello' in query:
                            res = speak('Hello Everyone! My self RO-BRO')
                        elif 'hello' in query:
                            res = speak("Hello Sir")

                        else:
                            res = web_scraping(query)
                            query = None

                        return res

        entryMsg = Entry(labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        entryMsg.insert(0, 'Type here...')  # placeholder
        entryMsg.bind("<Return>", display_msg)  # hits on enter get value
        # place the given widget
        # into the gui window
        entryMsg.place(relwidth=0.74, relheight=0.05, rely=0.002, relx=0.008)
        entryMsg.focus()
        mic_btn = Button(labelBottom, text="Back", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                         command=lambda: switch1())
        mic_btn.place(relx=0.77, rely=0.002, relheight=0.05, relwidth=0.22)

    def mic_fun():
        query = takeCommand().lower()
        res = data(query)

    def takeCommand():
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                recognition1.insert(END, "Listening...")
                recognition1.update_idletasks()
                #recognition1.delete(0, END)
                r.pause_threshold = 0.8
                audio = r.listen(source)
            try:
                print("Recognizning......")
                recognition1.delete(0.0, END)
                recognition1.insert(END, "Recognizing...")
                recognition1.update_idletasks()
                query = r.recognize_google(audio, language='en-in')
                print(f"You said: {query}\n")
                query = query.lower()
                text_chatbox.config(state=NORMAL)
                text_chatbox.insert(END, "You : " + query + "\n")
                text_chatbox.config(state=DISABLED)
                text_chatbox.see(END)
                text_chatbox.update_idletasks()
                time.sleep(2)
                recognition1.delete(0.0, END)

            except Exception as e:
                print("Exception: Sorry...I couldn't  recognize what u said " + str(e))
                speak("Could u please say that again ...")
                return "None"

            return query

    def speak(audio):
        print("Bro : ", audio)
        text_chatbox.config(state=NORMAL)
        text_chatbox.insert(END, "Bro : " + audio + "\n\n")
        text_chatbox.config(state=DISABLED)
        text_chatbox.see(END)
        text_chatbox.update_idletasks()
        engine.say(audio)
        engine.runAndWait()
        return audio

    def web_scraping(query):
        res = speak("Serching " + query + "")
        return res

    def wishme():
        hour = datetime.datetime.now().hour
        if hour >= 6 and hour < 12:
            res = speak("Good Morning sir! \n How can i help you?")
        elif hour >= 12 and hour < 18:
            res = speak("good arternoon sir! \n How can i help you?")
        elif hour >= 18 and hour < 24:
            res = speak("good evening sir! \n How can i help you?")
        else:
            res = speak("good night sir! \n How can i help you?")
        return res

    def data(query):
        # if __name__ == "__main__":
        # wishme()
        while True:
            if query != None:
                if 'time' in query:
                    Time = datetime.datetime.now().strftime("%I:%M:%S")
                    res = speak("Sir Current time is " + Time)

                elif 'date' in query:
                    strdate = datetime.datetime.today().strftime("%d-%m-%y")
                    res = speak("Sir today's date is %s" % strdate)

                elif 'youtube' in query:
                    if 'open youtube' in query:
                        webbrowser.open("www.youtube.com")
                        res = speak("Opening YouTube")
                    else:
                        youtube_ex = re.search('youtube(.*)', query)
                        youtube_ex = youtube_ex.group(1)
                        url = "https://www.youtube.com/results?search_query=" + youtube_ex
                        webbrowser.get().open(url)

                elif 'google' in query:
                    webbrowser.open("www.google.com")
                elif 'facebook' in query:
                    webbrowser.open("www.facebook.com")
                elif 'instagram' in query:
                    webbrowser.open("www.instagram.com")
                elif 'whatsapp' in query:
                    webbrowser.open("https://web.whatsapp.com")
                elif 'greekforgreek' in query:
                    webbrowser.open("www.greekforgreek.com")

                elif 'exit' in query or 'stop' in query:
                    exit()

                elif 'screenshot' in query:
                    x = random.randint(1, 1000000000)
                    pyautogui.screenshot("c:\\Desktop\\" + str(x) + ".png")
                    res = speak("okay sir, commond is done")

                elif 'who are you' in query:
                    res = speak("My name is Ro-Bro, I am your personal Voice assistant")
                elif 'thank you' in query:
                    res = speak("Welcome Sir")
                elif 'can you do for me' in query:
                    res = speak('I can do multiple tasks for you sir. tell me whatever you want to perform sir')
                elif 'old are you' in query:
                    res = speak("I am a little baby sir")
                elif 'your name' in query:
                    res = speak('myself RO-BROS sir')
                elif 'who creates you' in query or "who made you" in query or "who discovered you" in query:
                    res = speak('My Creator is Mr. Amey Patil & Mr. Pankaj Sajekar')
                elif 'say hello' in query:
                    res = speak('Hello Everyone! My self RO-BRO')
                elif 'hello' in query:
                    res = speak("Hello Sir")

                elif 'wikipedia' in query :
                    if 'open wikipedia' in query:
                        webbrowser.open('wikipedia.com')
                    else:
                        try:
                            res = speak("searching wikipedia")
                            query = query.replace("wikipedia", "")
                            result = wikipedia.summary(query, sentences=2)
                            res = speak("According to wikipedia")
                            res = speak(result)
                        except Exception as e:
                            res = speak('sorry sir could not find any results')

                elif 'search' in query:
                    search_ex = re.search('search (.*)', query)
                    search_ex = search_ex.group(1)
                    #res = speak("what do you want to search for?")
                    #search = takeCommand()
                    url = "https://google.com/search?q=" + search_ex
                    webbrowser.get().open(url)
                elif 'location' in query:
                    res = speak("what is the location?")
                    location = takeCommand()
                    url = "https://google.nl/maps/place/" + location + '&amp;'
                    webbrowser.get().open(url)
                    res = speak("here is the location of" + location)

                elif "weather" in query:
                    api_key = "3bb77efcfb71d016b3ff53851cab3875"
                    base_url = "https://api.openweathermap.org/data/2.5/weather?"
                    res = speak("what is the city name")
                    city_name = takeCommand()
                    print(city_name)
                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                    response = requests.get(complete_url)
                    x = response.json()
                    if x["cod"] != "404":
                        y = x["main"]
                        current_temperature = y["temp"]
                        current_humidiy = y["humidity"]
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        res = speak(city_name+"\n Temperature in kelvin is :" +
                                    str(current_temperature) +
                                    "\nThe humidity percentage is :" +
                                    str(current_humidiy) +
                                    "\n Description is :" +
                                    str(weather_description))
                    else:
                        res = speak(" City Not Found ")

                elif 'logout' in query:
                    os.system("shutdown -1")
                    res = speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                    # time.sleep(10)
                elif 'shutdown' in query:
                    os.system("shutdown /s /t 1")
                    res = speak("Ok , your pc will shutdown in 10 sec make sure you exit from all applications")
                    # time.sleep(10)
                elif 'restart' in query:
                    os.system("shutdown /r /t 1")
                    res = speak("Ok , your pc will restart in 10 sec make sure you exit from all applications")
                    # time.sleep(10)
                elif "hibernate" in query or "sleep" in query:
                    res = speak("Hibernating")
                    os.system("shutdown / h")

                elif 'open' in query:
                    reg_ex = re.search('open (.+)', query)
                    if reg_ex:
                        domain = reg_ex.group(1)
                        print(domain)
                        url = 'https://www.' + domain
                        webbrowser.open(url)
                        res = speak('The website you have requested has been opened for you Sir.')
                    else:
                        pass

                elif 'close' in query:
                    reg_ex = re.search('close (.+)', query)
                    print(query)
                    if reg_ex:
                        app = reg_ex.group(1)
                        os.system("taskkill /f /im " +app+ str(".exe"))
                        res = speak("closed")


                else:
                    res = web_scraping(query)
                    query = None

                return res

    line = Label(root, width=450, bg="#ABB2B9")
    line.place(relwidth=1, rely=0.01, relheight=0.012)
    # display frame
    text_chatbox = Text(root, height=2, bg="#17202A", fg="white", font="Helvetica 12", padx=5, pady=5)
    text_chatbox.place(relheight=0.890, relwidth=1, rely=0.01)

    labelBottom = Label(root, bg="#ABB2B9", height=55)
    labelBottom.place(relwidth=1, rely=0.890)

    keyboardbtn = Button(labelBottom, text="keyboard", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                         command=lambda: switch())
    keyboardbtn.place(relx=0.008, rely=0.002, relheight=0.05, relwidth=0.22, )
    recognition1 = Text(labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 16")
    recognition1.place(relwidth=0.50, relheight=0.05, rely=0.002, relx=0.008, x=114)
    settingbtn = Button(labelBottom, text="mic", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                        command=lambda: mic_fun())
    settingbtn.place(relx=0.77, rely=0.002, relheight=0.05, relwidth=0.22)

    text_chatbox.config(cursor="arrow")
    text_chatbox.config(state=DISABLED)

    root.title("RO-BROS")
    root.geometry("500x750+380+0")
    root.resizable(width=False, height=False)  # (0,0)
    root.configure(background='#17202A')
    root.mainloop()

root1.title("RO-BROS")
root1.geometry("500x750+380+0")
root1.resizable(width=False, height=False)  # (0,0)
root1.configure(background='#000000')

root1.mainloop()



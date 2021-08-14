import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from tkinter import Button, messagebox
from PIL import Image, ImageTk
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import random
import wolframalpha
import os
import pyautogui
import requests
import time
from pyowm import OWM
from bs4 import BeautifulSoup
import smtplib
from tkinter import simpledialog
import google_news
import google_translate
from threading import Thread
import socket

REMOTE_SERVER = "1.1.1.1"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', 130)
engine.setProperty('voice', voices[0].id)

root1 = tk.Tk()


def wish_me_speak(audio):
    engine.say(audio)
    engine.runAndWait()


logo = Image.open("Assistant.png")
logo = logo.resize((520, 410), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo, width=235, height=230)
logo_label.image = logo
logo_label.place(relx=0.25, rely=0.06)

project_name = Label(root1, text="RO-BROS", fg="#DAA520", bg="#000000", font="Algerian 40 bold italic")
project_name.place(relx=0.16, rely=0.36)

project_sub_name = Label(root1, text="(Personal Voice Assistance)", fg="#fff8dc", bg="#000000", font="Times 20")
project_sub_name.place(relx=0.05, rely=0.50)

next_btn = Button(root1, text="Start", bg="#F5F5F5", fg="#000000", font="Arebic 14", width=19,
                  command=lambda: start_btn())
next_btn.place(relx=0.20, rely=0.85, relheight=0.07, relwidth=0.60, )


def wish_me():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        wish_me_speak("Good Morning sir! How can i help you?")
    elif hour >= 12 and hour < 18:
        wish_me_speak("Good Afternoon sir! How can i help you?")
    elif hour >= 18 and hour < 24:
        wish_me_speak("Good Evening sir! How can i help you?")
    else:
        wish_me_speak("Good Night sir! How can i help you?")


def check_internet_connection():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass
    return False


def start_btn():
    check_internet = check_internet_connection()
    if check_internet:
        mainpage()
    else:
        messagebox.showwarning("Warning", "Please check your internet connection")


def mainpage():
    root1.destroy()
    root = tk.Tk()
    t = Thread(target=wish_me)
    t.start()

    def switch():

        type_btn.destroy()
        recognition1.destroy()
        mic_btn.destroy()

        def display_msg(event):
            msg = entry_msg.get()
            if not msg:
                return
            if 'Type here...' in msg:
                return
            entry_msg.delete(0, "end")
            text_chatbox.config(state=NORMAL)
            text_chatbox.insert(END, "You : " + msg + "\n")
            text_chatbox.update_idletasks()
            time.sleep(0.15)
            msg2 = data(msg)
            text_chatbox.insert(END, "Bro : " + msg2 + "\n\n")
            text_chatbox.update_idletasks()
            text_chatbox.config(state=DISABLED)
            text_chatbox.see(END)

        entry_msg = Entry(label_bottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        entry_msg.insert(0, 'Type here...')  # placeholder
        entry_msg.bind("<Return>", display_msg)  # hit
        # s on enter get value
        # place the given widget
        # into the gui window
        entry_msg.place(relwidth=0.745, relheight=0.05, rely=0.002, relx=0.01)
        entry_msg.focus()
        send_btn = Button(label_bottom, text="Send", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                          command=lambda: display_msg(None))
        send_btn.place(relx=0.77, rely=0.002, relheight=0.05, relwidth=0.22)

    def mic_fun():
        query = take_command().lower()
        res = data(query)
        return res

    def take_command():
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                r.pause_threshold = 0.8
                r.phrase_threshold = 0.290
                r.energy_threshold = 368
                r.adjust_for_ambient_noise(source, duration=1.2)
                print("Listening...")
                recognition1.configure(state=NORMAL)
                recognition1.insert(END, "LISTENING...")
                recognition1.update_idletasks()
                recognition1.config(state=DISABLED)
                audio = r.listen(source)
            try:
                recognition1.configure(state=NORMAL)
                recognition1.delete(0.0, END)
                recognition1.insert(END, "RECOGNIZE...")
                recognition1.update_idletasks()
                print("Recognizing...")
                time.sleep(0.15)
                recognition1.delete(0.0, END)
                recognition1.config(state=DISABLED)
                query = r.recognize_google(audio, language='en-in')
                print(f"You said : {query}\n")
                query = query.lower()
                text_chatbox.config(state=NORMAL)
                text_chatbox.insert(END, "You : " + query + "\n")
                text_chatbox.config(state=DISABLED)
                text_chatbox.see(END)
                text_chatbox.update_idletasks()

            except Exception as e:
                recognition1.configure(state=NORMAL)
                recognition1.delete(0.0, END)
                recognition1.insert(END, " ")
                recognition1.update_idletasks()
                recognition1.config(state=DISABLED)
                print(e)
                speak("Could u please say that again ...")
                return " "
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

    def web_scraping(qs):
        global flag

        url = 'https://www.google.com/search?q=' + qs
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        links = soup.findAll("a")
        all_links = []
        for link in links:
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:
                all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))

        flag = False
        for link in all_links:
            if 'https://en.wikipedia.org/wiki/' in link:
                wiki = link
                flag = True
                break

        div0 = soup.find_all('div', class_="kvKEAb")
        div1 = soup.find_all("div", class_="Ap5OSd")
        div2 = soup.find_all("div", class_="nGphre")
        div3 = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

        if len(div0) != 0:
            speak(div0[0].text)
        elif len(div1) != 0:
            speak(div1[0].text + "\n" + div1[0].find_next_sibling("div").text)
        elif len(div2) != 0:
            speak(div2[0].find_next("span").text + "\n" + div2[0].find_next("div", class_="kCrYT").text)
        elif len(div3) != 0:
            speak(div3[1].text)
        elif flag == True:
            page2 = requests.get(wiki)
            soup = BeautifulSoup(page2.text, 'html.parser')
            title = soup.select("#firstHeading")[1].text

            paragraphs = soup.select("p")
            for para in paragraphs:
                if bool(para.text.strip()):
                    speak(title + "\n" + para.text)
                    break
        else:
            res = speak("Sorry. I could not find the desired results")
            return res

    def send_email(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        # Enable low security in gmail
        server.login('blackstone00001111@gmail.com', 'bs00001111')
        server.sendmail('blackstone00001111@gmail.com', to, content)
        server.close()

    def data(query):
        res = ''
        while True:

            if 'current time' in query or "whats a time" in query:
                time_var = datetime.datetime.now().strftime("%I:%M:%S")
                res = speak("Sir Current time is " + time_var)

            elif 'todays date' in query or "what is today date" in query or "current date" in query:
                date_var = datetime.datetime.today().strftime("%d-%m-%y")
                res = speak("Sir today's date is %s" % date_var)

            elif 'exit' in query or 'stop application' in query:
                speak("good bye!")
                time.sleep(1)
                exit()

            elif "what day is today" in query or "what day is it" in query:
                localtime = time.asctime(time.localtime(time.time()))
                day = localtime[0:3]
                if day == "Sun":
                    res = speak("it's sunday")
                if day == "Mon":
                    res = speak("it's monday")
                if day == "Tue":
                    res = speak("it's tuesday")
                if day == "Wed":
                    res = speak("it's wednesday")
                if day == "Thu":
                    res = speak("it's thursday")
                if day == "Fri":
                    res = speak("it's friday")
                if day == "Sat":
                    res = speak("it's saturday")

            elif 'youtube' in query:
                if 'open youtube' in query:
                    webbrowser.open("www.youtube.com")
                    res = speak("Youtube open now")
                else:
                    youtube_ex = re.search('youtube(.*)', query)
                    youtube_ex = youtube_ex.group(1)
                    url = "https://www.youtube.com/results?search_query=" + youtube_ex
                    webbrowser.get().open(url)
                    res = speak("Youtube open now")

            elif 'google' in query:
                webbrowser.open("www.google.com")
                res = speak("google open now")
            elif 'facebook' in query:
                webbrowser.open("www.facebook.com")
                res = speak("facebook open now")
            elif 'instagram' in query:
                webbrowser.open("www.instagram.com")
                res = speak("Instagram open now")
            elif 'whatsapp' in query:
                webbrowser.open("https://web.whatsapp.com")
                res = speak("whatsapp open now")
            elif 'open gmail' in query:
                webbrowser.open("www.gmail.com")
                res = speak("Google Mail open now")
            elif 'greekforgreek' in query:
                webbrowser.open("www.greekforgreek.com")
                res = speak("greek for greek open now")
            elif "stack overflow" in query:
                webbrowser.open("www.stackoverflow.com")
                res = speak("stack overflow open now")

            elif 'screenshot' in query:
                try:
                    x = random.randint(1, 1000000000)
                    time.sleep(2)
                    pyautogui.screenshot("C://Users//panka//OneDrive//Desktop//" + str(x) + '.png')
                    res = speak("okay sir, done screenshot save on desktop.")
                except Exception:
                    x = random.randint(1, 1000000000)
                    time.sleep(2)
                    pyautogui.screenshot("C:/Users/Amey Patil/Desktop/screenshot" + str(x) + '.png')
                    res = speak("okay sir, done screenshot save on desktop.")

            elif 'wikipedia' in query:
                if 'open wikipedia' in query:
                    webbrowser.open('wikipedia.com')
                    speak("wikipedia open now!")
                else:
                    try:
                        speak("searching on wikipedia")
                        query = query.replace("wikipedia", "")
                        result = wikipedia.summary(query, sentences=2)
                        res = speak("According to wikipedia :\n" + result)
                    except Exception as e:
                        print(e)
                        res = speak('sorry sir,I could not find any result about that!')

            elif 'search' in query:
                search_ex = re.search('search (.*)', query)
                search_ex = search_ex.group(1)
                # res = speak("what do you want to search for?")
                # search = take_command()
                url = "https://google.com/search?q=" + search_ex
                webbrowser.get().open(url)

            elif 'location' in query:
                speak("Give me the location ")
                location = take_command()
                url = "https://google.nl/maps/place/" + location + '&amp;'
                webbrowser.get().open(url)
                res = speak("Here is the location of " + location)

            elif 'where is' in query:
                words = query.split('where is')
                res = speak("here is " + words[-1])
                link = str(words[-1])
                link = re.sub(' ', '', link)
                link = f'https://www.google.co.in/maps/place/{link}'
                webbrowser.open(link)

            elif "translate it" in query or 'translate' in query:
                statement = query.replace('translate ', '')
                speak("In which language?")
                dest = take_command()
                res = google_translate.langTranslator(statement, dest)
                res = speak(res)

            elif 'send email' in query:
                try:
                    speak("What should I say?")
                    content = take_command()
                    speak("Whome should i send email")
                    to = simpledialog.askstring("Input", "Please Enter Destiny mail address", parent=root)
                    send_email(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("I am not able to send this email")

            elif "email to pankaj" in query:
                try:
                    speak("What should I say??")
                    content = take_command()
                    to = "pankajsajekar123@gmail.com"
                    send_email(to, content)
                    speak("Email has been sent !")
                except Exception as e:
                    print(e)
                    speak("I am not able to send this email")

            elif 'open' in query:
                words = query.split('open')
                speak(words[-1])
                link = str(words[-1])
                link = re.sub(' ', '', link)
                link = f'https://{link}'
                webbrowser.open(link)
                res = speak('The website you have requested has been opened for you Sir.')

            elif 'remember that' in query or "write a notes" in query or "keep notes" in query or "add notes" in query:
                speak("what should i Write ,sir")
                note = take_command()
                speak("I remember that ,sir")
                remember = open('note.txt', 'w')
                remember.write(note)
                remember.close()
            elif 'do you know anything' in query or "show notes" in query:
                remember = open('note.txt', 'r')
                res = speak("note : \n " + remember.read())
            elif 'delete note' in query or "delete notes" in query:
                os.remove('note.txt')
                speak("Note has deleted, sir")

            elif "change system voice" in query or "robro change your voice" in query or "change voice" in query:
                sys_voice = engine.getProperty('voice')
                if str(
                        sys_voice) == "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0":
                    print("female voice")
                    engine.setProperty('voice', voices[0].id)
                else:
                    print("male voice")
                    engine.setProperty('voice', voices[1].id)
                res = speak('system voice is changed!')

            elif "weather" in query or "weather report" in query or "weather condition" in query:
                if 'current weather' in query:
                    reg_ex = re.search('current weather in (.*)', query)
                    city = reg_ex.group(1)
                    owm = OWM(API_key='3bb77efcfb71d016b3ff53851cab3875')
                    obs = owm.weather_at_place(city)
                    if reg_ex:
                        w = obs.get_weather()
                        k = w.get_status()
                        x = w.get_temperature(unit='celsius')
                        res = speak(
                            'weather in %s \n Description is %s \n The maximum temperature is %0.f °C \n The minimum temperature is %0.f °C' % (
                                city, k, x['temp_max'], x['temp_min']))
                else:
                    api_key = "3bb77efcfb71d016b3ff53851cab3875"
                    base_url = "https://api.openweathermap.org/data/2.5/weather?"
                    speak("what is the city name?")
                    city_name = take_command()
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
                        res = speak(city_name + "\nTemperature in kelvin is :" +
                                    str(current_temperature) +
                                    "\nThe humidity percentage is :" +
                                    str(current_humidiy) +
                                    "\nDescription is :" +
                                    str(weather_description))
                    else:
                        res = speak("City Not Found")

            elif 'logout' in query:
                os.system("shutdown -1")
                res = speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                # time.sleep(1)
            elif 'shutdown' in query:
                os.system("shutdown /s /t 1")
                res = speak("Ok , your pc will shutdown in 10 sec make sure you exit from all applications")
                # time.sleep(1)
            elif 'restart' in query:
                os.system("shutdown /r /t 1")
                res = speak("Ok , your pc will restart in 10 sec make sure you exit from all applications")
                # time.sleep(1)
            elif "hibernate" in query or "sleep" in query:
                res = speak("Hibernating")
                os.system("shutdown / h")

            elif 'close' in query or "closed" in query:
                reg_ex = re.search('close (.+)', query)
                print(query)
                if reg_ex:
                    app = reg_ex.group(1)
                    os.system(" taskkill /f /im " + app + str(".exe"))
                    res = speak("closed")

            elif 'tell me answer' in query or "give me answer" in query or 'activate alpha' in query:
                speak('I can answer to computational and geographical questions')
                # res = speak("You can ask anything")
                question = take_command()
                app_id = "U785EA-9LJ6UETJA2"
                client = wolframalpha.Client(app_id)
                res = client.query(question)
                answer = next(res.results).text
                res = speak(answer)

            elif "news" in query or "news headlines" in query or "today's news" in query:
                region = "india"
                news_list = google_news.getgooglenews(3, region)
                speak("Presenting you today's headlines...")
                for news in news_list:
                    speak(news)
                speak("Presented today's headlines...")

            elif 'on voice mode' in query or "activate voice" in query:
                speak("Voice mode is activated")
                while True:
                    if "on" in query or "activate" in query:
                        query2 = take_command().lower()
                        if "stop voice" in query2 or "stop voice mode" in query2 or "deactivate voice" in query2:
                            res = speak("Voice mode is De-activate")
                            break
                        else:
                            data(query2)

            elif 'say hello' in query:
                res = speak('Hello Everyone! My self Ro-Bro')
            elif 'hello' in query or "hello robro" in query or "Hey" in query:
                res = speak("Hello Sir")
            elif 'who are you' in query:
                res = speak("My name is Ro-Bro, I am your personal Voice assistant")
            elif 'how are you' in query:
                speak("I'm doing well!")
            elif 'thank you' in query or "thanks" in query:
                res = speak("Welcome Sir")
            elif 'what can you do for me' in query:
                res = speak('I can do multiple tasks for you sir. tell me whatever you want to perform sir')
            elif 'how old are you' in query or "your age" in query or "what is your age" in query:
                res = speak("I am still young by your standards.")
            elif 'your name' in query or "ro-bro" in query or "what is your name" in query:
                res = speak('myself RO-BROS sir')
            elif 'who creates you' in query or "who made you" in query or "who discovered you" in query or " who is your creater" in query:
                res = speak('My Creator is Mr. Amey Patil & Mr. Pankaj Sajekar')
            elif "where are you" in query:
                speak("i'm on the internet")
            elif "what can you eat" in query:
                speak("I consume RAM, and binary digits")
            elif "what language to use" in query:
                speak("I use Python, Java and C++ quite often.")
            elif "what are your hobbies" in query:
                speak("Playing soccer, painting, and writing are my hobbies. How about you?")
            elif "you are never sad" in query:
                res = speak("Not right now, no.")
            elif "you are jealous" in query or "you can not feel" in query or "you can not experience" in query or "feelings" in query:
                res = speak("Normally, as a bot i don't have feelings.")
            elif "where are you from" in query:
                res = speak("I am from where all software programs are from; a galaxy far, far away")
            elif "what is your location" in query:
                res = speak("I am everywhere.")
            elif "do you have any brothers" in query:
                res = speak("I don't have any brothers. but I have a lot of clones.")
            elif "who is your father" in query or "who is your mother" in query:
                res = speak("A human")
            elif "who is your boss" in query:
                res = speak("I like to think of myself as self-employed.")
            elif "what is your number" in query:
                res = speak(" I don't have any number")

            elif 'can you play study music on YouTube ?' in query or 'study music' in query:
                webbrowser.open("https://www.youtube.com/watch?v=bQzIQa5YKvw")
                res = speak("Yes sir. Opening YouTube.")
            elif 'i love this ' in query or 'your smart' in query:
                res = speak('Thank you sir. But I know that. Because you are the one who makes me Smart. ')
            elif 'robro, show me nearest gardens location' in query or 'garden' in query:
                webbrowser.open(
                    "https://www.google.co.in/maps/search/nearest+garden+to+me/@19.1726971,72.9445214,14z/data=!3m1!4b1")
                res = speak("here are the results of nearest gardens location on you screen")
            elif 'good morning' in query:
                res = speak("good morning sir. have a nice day.")

            else:
                res = web_scraping(query)
                # query = None
                return res
            return res

    # display Chats frame
    text_chatbox = Text(root, height=2, bg="#17202A", fg="white", font="Helvetica 12", padx=17, pady=12, border="7")
    text_chatbox.place(relheight=0.890, relwidth=1, rely=0.007)

    label_bottom = Label(root, bg="#D3D3D3", height=55)
    label_bottom.place(relwidth=1, rely=0.891)

    type_btn = Button(label_bottom, text="Type", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                      command=lambda: switch())
    type_btn.place(relx=0.01, rely=0.002, relheight=0.05, relwidth=0.22)
    recognition1 = Text(label_bottom, bg="#2C3E50", fg="#EAECEE", font="Rockwell 16", padx=14, pady=12)
    recognition1.config(state=DISABLED)
    recognition1.place(relwidth=0.51, relheight=0.05, rely=0.002, relx=0.245)
    mic_btn = Button(label_bottom, text="Mic", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                     command=lambda: mic_fun())
    mic_btn.place(relx=0.77, rely=0.002, relheight=0.05, relwidth=0.22)
    text_chatbox.config(cursor="arrow")
    text_chatbox.config(state=DISABLED)

    root.title(" RO-BROS")
    root.geometry("500x750+380+0")
    root.resizable(width=False, height=False)  # (0,0)
    root.configure(background='#17202A')
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='robro.png'))
    root.mainloop()


root1.geometry("500x750+380+0")
root1.resizable(width=False, height=False)  # (0,0)
root1.title(" RO-BROS")
root1.configure(background='#000000')
root1.tk.call('wm', 'iconphoto', root1._w, tk.PhotoImage(file='robro.png'))
root1.mainloop()

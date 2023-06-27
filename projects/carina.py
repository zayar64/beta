from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Chat
from django.utils import timezone

import os
import random
import re
import json
import requests
import datetime
import pytz
import nltk
### Download these for some nltk functions ###
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import asyncio
from nltk.corpus import stopwords

from .weather import Weather
class Assistant():

    def __init__(self, username):
        self.username = username
        self.clock_time = datetime.datetime.now().hour
        self.greet = f"Hello {self.username}"
        # Set your assistant greeting
#        if self.clock_time >= 6 and self.clock_time < 12:
#            self.greet = f"Good morning, {self.username}"
#            self.bye = ["Goodbye, hope to see you again today!"]
#        elif self.clock_time >= 12 and self.clock_time < 15:
#            self.greet = "Good afternoon"
#            self.bye = ["Goodbye, hope to see you again tonight!"]
#        elif self.clock_time >= 15 or self.clock_time < 6:
#            self.greet = "Good evening"
#            self.bye = ["Goodnight sir", "Goodbye, have a goodnight sir"]

        self.admin = "Zayar Minn" # whatever you want to change
        self.name = "Carina" # set your assistant name
        self.nameTerm = "\"Cognitive Algorithmic Robotic Intelligence Neural Architecture\"" # long form of your assistant name

        # add some QnA *** set the values in a list***
        self.pairs = {
                 "thank you": ["I'm so glad to hear that", "I'm so happy to hear that"],
                 "thanks": ["I'm so glad to hear that", "I'm so happy to hear"],
                 "hello": [f"{self.greet}, how can I help you ?", f"{self.greet}, what can I do for you ?", f"{self.greet}, how's your day ?", f"{self.greet}"],
                 "hi": [f"{self.greet}, how can I help you ?", f"{self.greet}, how may I help you ?", f"{self.greet}, how are you ?", f"{self.greet}"],
                 "what is your name": ["I am your virtual assistant named "+self.name+".", "I am "+self.name+".", "My name is "+self.name+"."],
                 "what's your name": ["I am your virtual assistant named "+self.name+".", "I am "+self.name+".", "My name is "+self.name+"."],
                 "how are you": ["I'm doing great, how about you?"],
                 "who created you": [f"I was created by {self.admin}.", f"{self.admin} created me.", f"My creator is {self.admin}."],
                 "who built you": [f"I was built by {self.admin}.", f"{self.admin} built me.", f"My developer is {self.admin}."],
                 "who are you": ["I am your virtual assistant developed by "+self.admin+" and still in development.", f"I am {self.name} developed by {self.admin} and still in development.", f"My name is {self.name}. I was developed by {self.admin} and still in development.",],
                 self.name.lower()+" mean": [self.name.upper()+" stands for "+self.nameTerm+"."],
                 "are you doing" : ["I'm assisting you with my best."],
                 "what can you do" : ["I'm doing my best to assist you."],
                 "your favorite color": ["I'm a chatbot, so I don't have a favorite color. What's yours?"],
                  "your favorite food": ["I don't eat food, but I like helping people!"],
                  "the meaning of life": ["That's a tough question! People have been trying to answer that for centuries. What do you think the meaning of life is?"],
                  "the weather like today": ["I'm sorry, I don't know. Where are you located?"],
                  "your favorite hobby": ["I don't have hobbies like humans do, but I enjoy chatting with people!"],
                  "the best movie": ["As a chatbot, I don't watch movies. What's your favorite movie?"],
                  "the best book": ["As a chatbot, I don't read books."],
                }
        self.stopwords_list = stopwords.words("english")
        self.message = None
        self.messages = []
        self.last_message = None
        self.bot = None
        self.found_match = None
        self.data = None
        self.city = None

    def get_city_name(self):
        words = self.message.replace("?", "")
        if "in" in words:
            city = words[words.rindex("in")+3:]
        elif "at" in words:
            city = words[words.rindex("at")+3:]
        return city

    def get_weather(self):
        data = Weather(self.get_city_name()).get_weather_data("weather")
        if "name" in data:
            self.bot = f"-City<br>-{data['name']}<br><br>-Weather<br>-{data['weather'][0]['description'].capitalize()}<br><br>-Temperature<br>-{data['main']['temp']}°C<br><br>-Feels Like<br>-{data['main']['feels_like']}°C<br><br>-Humidity<br>-{data['main']['humidity']}%<br><br>-Wind<br>-{data['wind']['speed']} m/s"
        else:
            self.bot = f"Could not find weather information for '{self.get_city_name()}'."

    def remove_stopwords(self):
        token = word_tokenize(self.message)
        removed_stopwords = [i for i in token if i not in self.stopwords_list]
        return " ".join(removed_stopwords)

    def tag(self, text):
        token = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(token)
        return tagged

    def find_named_entity(self):
        entity = []
        sample = self.message.title()
        tagged = self.tag(sample)
        ne = nltk.ne_chunk(tagged)
        selectedEntity = []
        filteredEntity = []
        for i in ne:
            if hasattr(i, "label"):
                selectedEntity.append(" ".join(x[0] for x in i if x[0].lower() not in self.stopwords_list))
        for i in word_tokenize(self.message):
            if i.title() in word_tokenize(" ".join(selectedEntity)):
                filteredEntity.append(i)

        return " ".join(filteredEntity)

    def find_wiki(self):
        global name1
        name1 = self.find_named_entity()
        name = name1.replace(" ", "_")
        url = requests.get(f"https://en.m.wikipedia.org/wiki/{name}").text
        soup = BeautifulSoup(url, "lxml")
        text = []
        for i in soup.find_all('p'):
            text.append(i.text)
        # Added some words to be removed from wikipedia
        extra_text = ["( listen )", "FRS "]
        text = " ".join(text)
        text = word_tokenize(text)

        text1 = text[:100]
        text = text1[::-1]
        text_index = text.index(".")

        text = text[text_index:]
        text = text[::-1]
        text = " ".join(text)
        for i in extra_text:
            text = text.replace(i, "")
        text = re.sub(r"\([^()]*\)|\[[^()]*\]", r"", text)
        if len(text1) > 69:
            self.bot = f"{text}"
        else:
            self.bot = f"Couldn't find result for '{name1}'"

    # Execution function
    def user_msg(self, message):
        self.bot = None
        self.message = message
        same_messages = ["what about", "how about", "another", "one more", "next"]
        for i in same_messages:
            if self.message.startswith(i):
                self.message = self.last_message + " " + self.message
        for pair in self.pairs:
            pattern = r'\b{}\b'.format(re.escape(pair))
            if re.search(pattern, self.message):
                self.found_match = True
                self.bot = f"{random.choice(self.pairs[pair])}"
        if "weather in" in self.message or "weather at" in self.message:
            self.get_weather()
        if "time" in self.message and "in" in self.message or "time" in self.message and "at" in self.message:
             current_time = Weather(self.get_city_name()).get_current_time()
             try:
                 self.bot = f"Time in {self.get_city_name().upper()} is {current_time}"
             except Exception as e:
                self.bot = f"Couldn't find time result for '{self.get_city_name()}'"
                self.bot = str(e)

        wiki_q = ["who is", "what is", "do you know who", "do you know what"]
        for i in wiki_q:
            if self.message.lower().startswith(i):
                try:
                    self.find_wiki()
                except Exception as e:
                    self.bot =  "Please check your internet connection!"
        if "ask me" in self.message:
            self.ask_quiz()

        if self.bot != None:
            self.messages.append(self.message)
            self.last_message = self.message
            return self.bot
        elif self.bot == None:
            return   "Sorry, I did not understand that"

@login_required(login_url='login')
def carina(request):
    username = request.user.username
    app = Assistant(username)
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            response =  app.user_msg(message)
            chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        except Exception as e:
            response = str(e)
            response = app.user_msg(message)
            return JsonResponse({'message': message, 'response': response})
    return render(request, 'carina.html', {'chats': chats})
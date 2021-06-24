import requests
import telebot
import config
from datetime import datetime

URL = "https://cplistapi.herokuapp.com/"

r = requests.get(url=URL)
t1 = datetime.now()
data = r.json()

bot = telebot.TeleBot(config.API_KEY)


def fetchData():
    global t1
    t2 = datetime.now()
    duration = t2 - t1
    duration_in_s = duration.total_seconds()
    hours = divmod(duration_in_s, 3600)[0]
    if hours < 2:
        return
    t1 = t2
    global data
    r = requests.get(url=URL)
    data = r.json()


help_msg = "'/OnGoingEvents<platform name>' --> to show the ongoing events on that platform\n\n"
help_msg += "'/UpComingEvents<platform name>' --> to show the upcoming events on that platform\n\n"
help_msg += "Example:- '/UpcomingEventsHackerEarth'"


@bot.message_handler(commands=['start', 'help'])
def sendmessage(message):
    bot.reply_to(message, help_msg)


def getOnGoingData(platform, type):
    fetchData()
    global data
    msg = platform.upper()+'\n'
    k = 0
    for i, d in enumerate(data['results'][type]):
        if d["platform"] == platform:
            msg += str(k+1) + ") :\n"
            msg += "Event Name : " + d["name"] + "\n"
            msg += "Platform : " + d["platform"]+"\n"
            msg += "Start Time : " + \
                str(datetime.fromtimestamp(d["startTime"]))+"\n"
            msg += "End Time : " + \
                str(datetime.fromtimestamp(d["endTime"]))+'\n'
            msg += "Link To Register : " + d['url'] + '\n\n\n'
            if k == 11:
                break
            k += 1
    if k == 0:
        msg += 'InvalidPlatform or No data Available'
    msg += "\n\nHappy Coding!"
    return msg


@bot.message_handler(regexp="OnGoingEvents")
def sendmessage(message):
    bot.reply_to(message, getOnGoingData(
        message.text[14:].lower(), type="ongoing"))


@bot.message_handler(regexp="UpComingEvents")
def sendmessage(message):
    bot.reply_to(message, getOnGoingData(
        message.text[15:].lower(), type="upcoming"))


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, help_msg)


bot.polling()

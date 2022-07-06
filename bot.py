from webbrowser import get
import telebot
import requests
from bs4 import BeautifulSoup
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import secrets

#define telebot
bot = telebot.TeleBot(secrets.TELEGRAM_TOKEN)

c_id = secrets.c_id
m_id = secrets.m_id

#Scheduler instantiate
sched = BlockingScheduler()



#get hora
def gettime():
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=-4)
    return now.strftime("%H:%M")

#get fecha
def getdate():
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=-4)
    return now.strftime("%d/%m/%Y")

#USDCLP
def getusd():
    web = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=usd&tsyms=clp"
    response = requests.get(web)
    data = response.json()
    price = data["RAW"]["USD"]["CLP"]["PRICE"]
    return price

#BTCUSD
def getbtcusd():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']


#add start command
@bot.message_handler(commands=['ids'])
def send_welcome(message):
    print(message.chat.id)
    print(message.id)
    bot.send_message(message.chat.id, "MODIFICAR")


@sched.scheduled_job('interval',id='send_welcome', minutes = 1)
def send_welcome():
    bot.edit_message_text(
        chat_id=c_id,
        text="Precio del dolar: $" +
        str(getusd()) +
        "\nPrecio del Bitcoin: $" +
        str(getbtcusd()) +
        "\n\n" +
        "Ultima actualizacion: " +
        str(gettime()) +
        " | " +
        str(getdate()),
        message_id=m_id)



#start schedule / bot
sched.start()


#initialize the bot
#bot.polling()

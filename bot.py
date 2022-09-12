from webbrowser import get
import telebot
import requests
from bs4 import BeautifulSoup
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import secrets
import json

#define telebot
bot = telebot.TeleBot(secrets.TELEGRAM_TOKEN)

c_id = secrets.c_id
m_id = secrets.m_id

#Scheduler instantiate
sched = BlockingScheduler()



#get hora y fecha
def gettime():
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=-3)   
    return now.strftime("%H:%M %d/%m/%Y")


#USDCLP
def getusd3():
    headers = {'User-Agent':'...','referer':'https:/...'}
    url = "https://apps.bolchile.com/api/v1/dolarstatd2"
    response = requests.get(url, headers=headers, verify=True)
    if response.status_code == 200:
        data = json.loads(response.text)
        price = data[0]['cp']
        hp = data[0]['hp']
        return str(price) + " (" + str(hp) + ")"

#BTCUSD
def getbtcusd():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    return data['bpi']['USD']['rate']

def geteth():
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
    data = response.json()
    return data['USD']

def getlunc():
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=LUNA&tsyms=USD')
    data = response.json()
    return data['USD']


#add start command
@bot.message_handler(commands=['ids'])
def send_welcome(message):
    print(message.chat.id)
    print(message.id)
    #bot.send_message(message.chat.id, "MODIFICAR")


@sched.scheduled_job('interval',id='send_welcome', minutes = 1)
def updateMensaje():
    bot.edit_message_text(
        chat_id=c_id, 
        text="Precio del dolar: $" + str(getusd3()) + 
        "\n\nPrecio del Bitcoin: $" + str(getbtcusd()) + 
        "\nPrecio de ETH: $" + str(geteth()) +
        "\nPrecio de LUNC: $" + str(getlunc()) +
        "\n\n" + 
        "Ultima actualizacion: " + str(gettime()), message_id=m_id)        



#start schedule / bot
sched.start()


#initialize the bot
#bot.polling()








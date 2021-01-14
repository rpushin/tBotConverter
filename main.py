import telebot
import tgAuth
from extensions import Bot
from extensions import RatesApi
import lxml.html
import requests
import json
import re
#

tgbot = Bot(tgAuth.TOKEN)
tgbot.poll()


# reg = re.compile("(\d*)(?:.*)(USD|RUB|EUR)(?:.*)(USD|RUB|EUR)")
# m = reg.search('fEURUSkatakatasdfsdf')
# print(m)
# print(m.group(0))
# print(m.group(1))
# print(m.group(2))
# print(m.group(3))
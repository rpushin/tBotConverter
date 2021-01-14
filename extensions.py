import requests
import json
import telebot

class Error(Exception):
    pass

class APIException(Error):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        if self.type == 'non-float':
            return 'Первый аргумент невозможно привести к числу'
        elif self.type == 'currency_error':
            return 'Одна из введённых валют не поддерживается'


class RatesApi:
    @staticmethod
    def get_rates(base, quote, amount):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('non-float')
        currencies = {'base': base, 'symbols': quote}
        html_response = requests.get('https://api.exchangeratesapi.io/latest', params=currencies)
        ret = json.loads(html_response.content)
        if 'error' in ret:
            raise APIException('currency_error')
        _res = float(ret['rates'][quote])
        return round(amount * _res, 2), round(_res, 4)


class Bot:
    def __init__(self, _bt):
        self.bot = telebot.TeleBot(_bt)

        @self.bot.message_handler(commands=['start', 'help'])
        def handle_start_help(message):
            response = "Этот бот перевеодит одну валюту в другую\n" \
                       "Набери /values чтобы узнать какие валюты поддерживаются\n" \
                       "Или введи '(валюта откуда) (валюта куда) 100', чтобы конвертировать, например:\n" \
                       "USD EUR 1000"
            self.bot.send_message(message.chat.id, response)

        @self.bot.message_handler(commands=['values'])
        def handle_value(message):
            response = "Используй трёхбуквенные коды для одной из:\n" \
                       "RUB - российский рубль\n" \
                       "USD - американский доллар\n" \
                       "EUR - Евро\n"
            self.bot.send_message(message.chat.id, response)

        @self.bot.message_handler(content_types=['text'])
        def handle_mess(message):
            m = message.text.split(' ')
            if not m:
                self.bot.reply_to(message, "Введи /help чтобы узнать какие команды я понимаю\n")
            elif len(m) != 3:
                self.bot.reply_to(message, "Нужно вводить по формату 'USD RUB 1000' не забывая пробелы\n"
                                           "Введи /help чтобы узнать какие команды я понимаю\n")
            else:
                try:
                    api_response = RatesApi.get_rates(m[0], m[1], m[2])
                except APIException as e:
                    self.bot.reply_to(message, str(e) )
                    return
                self.bot.reply_to(message, f'Актуальный курс: {api_response[1]}\n'
                                           f'{m[2]} {m[0]} = {api_response[0]} {m[1]}' )

    def poll(self):
        self.bot.polling(none_stop=True)
        self.bot.polling(none_stop=True)
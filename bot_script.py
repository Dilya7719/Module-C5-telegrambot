from config import TOKEN, currency_dict
from extensions import APIException, ParsingPrice
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message: telebot.types.Message):
    text = 'Чтобы начать работу, отправьте боту команду в формате:' \
                   '\n <имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>' \
                   '\n\nинформацию вводите через пробел' \
                   '\n результат округляется до сотых' \
                   '\n\nПосмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values_message(message: telebot.types.Message):
    text = '\n'.join(currency_dict.keys())
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def text_message(message: telebot.types.Message):
    try:
        if message.text[0] == '/':
            raise APIException('Неизвестная команда.')
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Вы ввели некорректное количество параметров.')
        quote, base, amount = values
        total = ParsingPrice.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        if amount == '1':
            quote = currency_dict[quote]['is_amount_one']
        else:
            quote = currency_dict[quote]['is_quote']
        base = currency_dict[base]['is_base']
        text = f'Цена {amount} {quote} в {base} - {total}'
        bot.send_message(message.chat.id, text)

bot.polling()

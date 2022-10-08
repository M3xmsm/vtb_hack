import telebot
from telebot import types
from vtb_hack.backend.backbone import get_news_records_by_label


bot = telebot.TeleBot('5779900311:AAHqsPweK0Mzu_Ck-3iMrKpx3vnFHRHUPBI')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("CEO: новости экономики в стране и мире")
    item2 = types.KeyboardButton("Бухгалтерия: изменения  в законодательстве и рынок труда")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, 'Какие новости ты хотел бы узнать?', reply_markup=markup)


@bot.message_handler(regexp="👈 Вернуться в меню")
def main_menu(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("CEO: новости экономики в стране и мире")
    item2 = types.KeyboardButton("Бухгалтерия: изменения  в законодательстве и рынок труда")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, 'Какие новости ты хотел бы узнать?', reply_markup=markup)


@bot.message_handler(regexp="Бухгалтерия: изменения  в законодательстве и рынок труда")
def buh_news(m, res=False):
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    # markup.row('Законодательство', 'HR: баланс сил')
    markup.row('Законодательство')
    markup.row('👈 Вернуться в меню')
    bot.send_message(m.chat.id, 'Могу рассказать про последние изменения в законодательстве', reply_markup=markup)


# @bot.message_handler(regexp="HR: баланс сил")
# def hr_news(m, res=False):
#     markup = telebot.types.ReplyKeyboardMarkup(True, True)
#     markup.row('IT', 'Product')
#     markup.row('Project', 'Прочее')
#     markup.row('👈 Вернуться в меню')
#     bot.send_message(m.chat.id, 'Кого будем искать?', reply_markup=markup)


@bot.message_handler(regexp="Законодательство")
def buh_reg_news(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👈 Вернуться в меню")
    markup.add(item1)
    news_records = get_news_records_by_label('Бухгалтерия')
    for news in news_records:
        msg = news['headline'] + '\n\n*Подробнее*: ' + news['link']
        bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(regexp="CEO: новости экономики в стране и мире")
def ceo_news(m, res=False):
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row('Экономика и финансы💸', 'Изменения в УК🫣')
    markup.row('👈 Вернуться в меню')
    bot.send_message(m.chat.id, 'Могу рассказать про последние новости экономики или об изменениях в УК',  reply_markup=markup)


@bot.message_handler(regexp="Экономика и финансы💸")
def ceo_econ_news(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👈 Вернуться в меню")
    markup.add(item1)
    news_records = get_news_records_by_label('Экономика')
    for news in news_records:
        msg = news['headline'] + '\n\n*Подробнее*: ' + news['link']
        bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(regexp="Изменения в УК🫣")
def ceo_uk_news(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("👈 Вернуться в меню")
    markup.add(item1)
    news_records = get_news_records_by_label('Юристы')
    for news in news_records:
        msg = news['headline'] + '\n\n*Подробнее*: ' + news['link']
        bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode='Markdown')


if __name__ == "__main__":
    print("Running...")
    bot.polling(none_stop=True, interval=0)

from telebot import TeleBot, types
import config


bot = TeleBot(config.token)
users = config.fake_database['users']


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    wallet = types.KeyboardButton('Кошелек')
    transaction = types.KeyboardButton('Перевод')
    history = types.KeyboardButton('История')
    markup.add(wallet, transaction, history)
    bot.send_message(message.chat.id, 'у меня ты можешь хранить и отправлять биткоины', reply_markup=markup)
    # print(message.from_user.to_dict())


@bot.message_handler(regexp='Кошелек')
def wallet(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    balance = 0
    text = f'Ваш баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Перевести')
def transaction(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    text = f'Введите адрес кошелька куда хотите перевести: '
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='История')
def history(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    markup.add(btn1)
    transactions = ['1', '2', '3']
    text = f'Ваши транзакции{transactions}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Меню')
def menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Кошелек')
    btn2 = types.KeyboardButton('Перевести')
    btn3 = types.KeyboardButton('История')
    markup.add(btn1, btn2, btn3)
    text = f'Главное меню'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == "Админ")
def admin_panel(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('Общий баланс')
    btn2 = types.KeyboardButton('Все пользователи')
    btn3 = types.KeyboardButton('Данные по юзеру')
    btn4 = types.KeyboardButton('Удалить юзера')
    markup.add(btn1, btn2, btn3, btn4)
    text = f'Админ-панель'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == "Все пользователи")
def all_users(message):
    text = f'Пользователи:'
    inline_markup = types.InlineKeyboardMarkup()
    for user in users:
        inline_markup.add(types.InlineKeyboardButton(text=f'Юзер: {user["name"]}',
                                                             callback_data=f"user_{user['id']}"))
    bot.send_message(message.chat.id, text, reply_markup=inline_markup)


bot.infinity_polling()
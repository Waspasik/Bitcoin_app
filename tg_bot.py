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
    text = 'У меня ты можешь хранить и отправлять биткоины'
    bot.send_message(message.chat.id, text, reply_markup=markup)
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
    text = f'Ваши транзакции {transactions}'
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
        inline_markup.add(types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                             callback_data=f"user_{user['id']}"))
    bot.send_message(message.chat.id, text, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    query_type = call.data.split('_')[0]
    if query_type == 'user':
        user_id = call.data.split('_')[1]
        inline_markup = types.InlineKeyboardMarkup()
        for user in users:
            if str(user['id']) == user_id:
                back = types.InlineKeyboardButton(text='Назад', callback_data='users')
                delete_user = types.InlineKeyboardButton(text='Удалить юзера', callback_data=f'delete_user_{user_id}')
                inline_markup.add(back, delete_user)
                bot.edit_message_text(text=f'Данные по пользователю:\n'
                                           f'ID: {user["id"]}\n'
                                           f'Имя: {user["name"]}\n'
                                           f'Ник: {user["nick"]}\n'
                                           f'Баланс: {user["balance"]}',
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=inline_markup)
                print('Запрошен ', user)
                break
    if query_type == 'users':
        inline_markup = types.InlineKeyboardMarkup()
        for user in users:
            show_user = types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                   callback_data=f"user_{user['id']}")
            inline_markup.add(show_user)
            bot.edit_message_text(text='Пользователи:',
                                 chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 reply_markup=inline_markup)
    if query_type == 'delete' and call.data.split('_')[1] == 'user':
        user_id = int(call.data.split('_')[2])
        for index, user in enumerate(users):
            print(user['name'])
            if user['id'] == user_id:
                print(f'Удален пользователь: {users[index]}')
                users.pop(index)
        inline_markup = types.InlineKeyboardButton
        for user in users:
            show_user = types.InlineKeyboardButton(text=f'Пользователь: {user["name"]}',
                                                   callback_data=f"user_{user['id']}")
            bot.edit_message_text(text='Пользователи:',
                                 chat_id=call.message.chat.id,
                                 message_id=call.message.message_id,
                                 reply_markup=inline_markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == 'Общий баланс')
def total_balance(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    menu = types.KeyboardButton('Меню')
    admin = types.KeyboardButton('Админ')
    markup.add(menu, admin)
    balance = 0.0
    for user in users:
        balance += user['balance']
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


bot.infinity_polling()
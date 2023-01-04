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
    page = 1
    count_page = len(users) // 4 + bool(len(users) % 4)
    left_board = 0
    right_board = 4
    markup = types.InlineKeyboardMarkup()
    for i in range(left_board, right_board):
        markup.add(types.InlineKeyboardButton(text=f'Пользователь: {users[i]["name"]}',
                                              callback_data=f"user?{users[i]['id']}?{page}?{left_board}?{right_board}?{count_page}"))
    markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
    markup.add(types.InlineKeyboardButton(text=f'{page}/{count_page}', callback_data=f' '),
               types.InlineKeyboardButton(text=f'Вперёд --->',
                                          callback_data=f"pagination?{page+1}?{left_board+4}?{right_board+4}?{count_page}"))
    bot.send_message(message.chat.id, 'Пользователи:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    query = call.data.split('?')
    query_type = call.data.split('?')[0]
    print(query_type)

    # Обработка кнопки - скрыть
    if query_type == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # Обработка кнопки - вперед и назад
    elif query_type == 'pagination':
        page = int(query[1])
        left_board = int(query[2])
        right_board = int(query[3])
        count_page = len(users) // 4 + bool(len(users) % 4)
        markup = types.InlineKeyboardMarkup()
        if count_page == 1:
            for i in range(left_board, len(users)):
                markup.add(types.InlineKeyboardButton(text=f'Пользователь: {users[i]["name"]}',
                                                      callback_data=f"user?{users[i]['id']}?{page}?{left_board}?{right_board}?{count_page}"))
            markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
            markup.add(types.InlineKeyboardButton(text=f'{page}/{count_page}', callback_data=f' '))
        elif page == 1:
            for i in range(left_board, right_board):
                markup.add(types.InlineKeyboardButton(text=f'Пользователь: {users[i]["name"]}',
                                                      callback_data=f"user?{users[i]['id']}?{page}?{left_board}?{right_board}?{count_page}"))
            markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
            markup.add(types.InlineKeyboardButton(text=f'{page}/{count_page}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->',
                                                  callback_data=f"pagination?{page+1}?{left_board+4}?{right_board+4}?{count_page}"))
        elif page == count_page:
            if bool(len(users) % 4):
                for i in range(left_board, len(users)):
                    markup.add(types.InlineKeyboardButton(text=f'Пользователь: {users[i]["name"]}',
                                                          callback_data=f"user?{users[i]['id']}?{page}?{left_board}?{right_board}?{count_page}"))
                markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
                markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                      callback_data=f"pagination?{page-1}?{left_board-4}?{right_board-4}?{count_page}"),
                           types.InlineKeyboardButton(text=f'{page}/{count_page}', callback_data=f' '))
            else:
                for i in range(left_board, right_board):
                    markup.add(types.InlineKeyboardButton(text=f'Пользователь: {users[i]["name"]}',
                                                          callback_data=f"user?{users[i]['id']}?{page}?{left_board}?{right_board}?{count_page}"))
                markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
                markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                      callback_data=f"pagination?{page-1}?{left_board-4}?{right_board-4}?{count_page}"),
                           types.InlineKeyboardButton(text=f'{page}/{count_page}', callback_data=f' '))
        else:
            for i in range(left_board, right_board):
                markup.add(types.InlineKeyboardButton(text=f'Пользователь: {users[i]["name"]}',
                                                      callback_data=f"user?{users[i]['id']}?{page}?{left_board}?{right_board}?{count_page}"))
            markup.add(types.InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад',
                                                  callback_data=f"pagination?{page-1}?{left_board-4}?{right_board-4}?{count_page}"),
                       types.InlineKeyboardButton(text=f'{page}/{count_page}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->',
                                                  callback_data=f"pagination?{page+1}?{left_board+4}?{right_board+4}?{count_page}"))
        bot.edit_message_text(text='Пользователи:',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)
    
    # Обработка запроса пользователя
    elif query_type == 'user':
        page = int(query[2])
        left_board = int(query[3])
        right_board = int(query[4])
        count_page = len(users) // 4 + bool(len(users) % 4)
        user_id = int(call.data.split('?')[1])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Назад',
                                              callback_data=f"pagination?{page}?{left_board}?{right_board}?{count_page}"),
                   types.InlineKeyboardButton(text='Удалить пользователя',
                                              callback_data=f'delete?{user_id}?{page}?{left_board}?{right_board}?{count_page}'))
        for index, user in enumerate(users):
            if user['id'] == user_id:
                bot.edit_message_text(f'<b>id:</b> <i>{users[index]["id"]}</i>\n'
                              f'<b>Имя:</b> <i>{users[index]["name"]}</i>\n'
                              f'<b>Ник:</b><i>{users[index]["nick"]}</i>\n'
                              f'<b>Баланс:</b><i> {users[index]["balance"]}</i>',
                              parse_mode="HTML",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup = markup)
                print('Запрошен ', users[index])
    
    # Удаление пользователя
    elif query_type == 'delete':
        page = int(query[2])
        left_board = int(query[3])
        right_board = int(query[4])
        count_page = len(users) // 4 + bool(len(users) % 4)
        user_id = int(call.data.split('?')[1])
        for index, user in enumerate(users):
            if user['id'] == user_id:
                print(f'Удален пользователь: {users[index]}')
                users.pop(index)
        print(users)
        count_page_after_delete = len(users) // 4 + bool(len(users) % 4)
        if count_page > count_page_after_delete:
            left_board = len(users) - 4
            right_board = len(users)
            page = right_board // 4 + bool(len(users) % 4)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='К списку пользователей',
                                              callback_data=f"pagination?{page}?{left_board}?{right_board}?{len(users) // 4 + bool(len(users) % 4)}"))
        bot.edit_message_text(text='Пользователи:',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)


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
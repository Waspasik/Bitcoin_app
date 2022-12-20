import fastapi
import database
import pydantic_models
import config


api = fastapi.FastAPI()


fake_database = {'users':[
    {
        "id":1,             # тут тип данных - число
        "name":"Anna",      # тут строка
        "nick":"Anny42",    # и тут
        "balance": 15300    # а тут int
     },

    {
        "id":2,             # у второго пользователя 
        "name":"Dima",      # такие же 
        "nick":"dimon2319", # типы 
        "balance": 160.23   # кроме баланса - float
     }
    ,{
        "id":3,             # у третьего
        "name":"Vladimir",  # юзера
        "nick":"Vova777",   # мы специально сделаем 
        "balance": "25000"  # нестандартный тип данных в его балансе
     }
],}


# response = {"Ответ":"Который возвращает сервер"}

# @api.get('/')
# def index():
#     return response

@api.get('/static/path')
def hello():
    return "hello"

@api.get('/user/{nick}')
def get_nick(nick):
    return {"user": nick}

@api.get('/userid/{id:int}')
def get_id(id):
    return {'user': id}

@api.get('/user_id/{id}')
def get_id2(id: int):
    return {'user': id}

@api.get('/user_id_str/{id:str}')
def get_id3(id):
    return {'user': id}

@api.get('/test/{id:int}/{text:str}/{custom_path:path}')
def get_test(id, text, custom_path):
    return {"id":id,
            "":text,
            "custom_path": custom_path}

@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id-1]

@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance(id):
    return fake_database['users'][id-1]['balance']

@api.get('/get_total_balance')
def get_total_balance():
    total_balance: float = 0.0
    for user in fake_database['users']:
        total_balance += pydantic_models.User(**user).balance 
    return total_balance

@api.get("/users/")
def get_users(skip: int = 0, limit: int = 10):
    return fake_database['users'][skip: skip + limit]

@api.get("/user/{user_id}")
def read_user(user_id: str, query: str | None = None):
    if query:
        return {"user_id": user_id, "query": query}
    return {"user_id": user_id}
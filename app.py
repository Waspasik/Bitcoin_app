import fastapi
from fastapi import FastAPI

import pydantic_models
from database import crud

api = FastAPI()


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.UserToUpdate = fastapi.Body()):
    """Обновляем юзера"""
    if user_id == user.id:
        return crud.update_user(user).to_dict()


@api.delete('/user/{user_id}')
@crud.db_session
def delete_user(user_id: int = fastapi.Path()):
    """
    Удаляем юзера
    :param user_id: 
    :return: 
    """
    crud.get_user_by_id(user_id).delete()
    return True


@api.post('/user/create')
def create_user(user: pydantic_models.UserToCreate):
    """
    Создаем Юзера
    :param user: 
    :return: 
    """
    return crud.create_user(tg_id=user.tg_ID,
                            nick=user.nick if user.nick else None).to_dict()


@api.get('/get_info_by_user_id/{user_id:int}')
@crud.db_session
def get_info_about_user(user_id):
    """
    Получаем инфу по юзеру
    :param user_id: 
    :return: 
    """
    return crud.get_user_info(crud.User.get(id=user_id))


@api.get('/get_user_balance_by_id/{user_id:int}')
@crud.db_session
def get_user_balance_by_id(user_id):
    """
    Получаем баланс юзера
    :param user_id: 
    :return: 
    """
    return crud.User[user_id].wallet.balance


@api.get('/get_total_balance')
@crud.db_session
def get_total_balance():
    """
    Получаем общий баланс
    :return: 
    """
    balance = 0.0
    crud.update_all_wallets()
    for user in crud.User.select()[:]:
        balance += user.wallet.balance
    return balance


@api.get("/users")
@crud.db_session
def get_users():
    """
    Получаем всех юзеров
    :return: 
    """
    users = []
    for user in crud.User.select()[:]:
        users.append(user.to_dict())
    return users


@api.get("/user_by_tg_id/{tg_id:int}")
@crud.db_session
def get_user_by_tg_id(tg_id):
    """
    Получаем юзера по айди его ТГ
    :param tg_id: 
    :return: 
    """
    user = crud.get_user_info(crud.User.get(tg_ID=tg_id))
    return user


@api.get('/get_user_wallet/{user_id:int}')
@crud.db_session
def get_user_wallet(user_id):
    return crud.get_wallet_info(crud.User[user_id].wallet)


# @api.get('/get_user_transaction/{user_id:int}')
# @crud.db_session
# def get_user_transaction(user_id):
#     return crud.get_user_transactions(crud.User[user_id].wallet)
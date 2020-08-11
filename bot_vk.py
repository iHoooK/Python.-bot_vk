import random


def get_user_name(user_id, vkapi):  # получить имя пользователя
    name = vkapi.users.get(user_id=user_id)[0]
    first_name = name['first_name']
    last_name = name['last_name']
    full_name = first_name + " " + last_name
    return full_name






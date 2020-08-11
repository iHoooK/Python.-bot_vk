import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import traceback
import random
import time
import csv
import requests
import logging
from functools import wraps

# файлы бота
import config
import bot_database
import bot_message
import bot_vk
import bot_logs

logging.disable()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# logging.debug('object.from_id=' + str(object.from_id))
# logging.debug(config.admins_id)


def mult_threading(func):
    """Декоратор для запуска функции в отдельном потоке"""

    @wraps(func)
    def wrapper(*args_, **kwargs_):
        import threading
        func_thread = threading.Thread(target=func,
                                       args=tuple(args_),
                                       kwargs=kwargs_)
        func_thread.start()
        return func_thread

    return wrapper

#  Сразу делаем функцию многопоточной
@mult_threading
def check_time():
    while True:
        hours, log_time = bot_logs.get_time()
        if hours == 0:
            print('БАЗА ОБНОВЛЕНА')
            bot_database.today_count()
        time.sleep(3600)


def main():
    # Авторизуемся как сообщество
    vk = vk_api.VkApi(token=config.token)
    vk._auth_token()

    # Работа с сообщениями. Подключение id группы бота
    longpoll = VkBotLongPoll(vk, config.bot_id)
    vkapi = vk.get_api()

    bot_logs.create_file(config.log_file)  # создает файл с заголовками

    print("Server started")
    # Основной цикл
    for event in longpoll.listen():
        # Если пришло новое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:
            # если id беседы не совпадает с id пользователя (значит в беседе)
            if event.object.peer_id != event.object.from_id:
                try:
                    # логи от кого и какое сообщение пришло
                    bot_logs.get_log(event.object.from_id, event.object.text, vkapi)

                    # проверка, какое сообщение пришло
                    config.sleep = bot_message.check_message(vk, vkapi, event.object, config.sleep)
                except Exception:
                    g = 'Ошибка:\n' + traceback.format_exc()
                    print(g)
                    bot_message.write_peer_msg(vk, event.object.peer_id, 'Чот у меня ошибка какая то #ошибка_бота')
                    continue

            # если id беседы совпадает с id пользователя (значит в личке группы)
            elif event.object.peer_id == event.object.from_id:# можно писать от имени бота в чате
                if event.object.from_id == :
                    bot_message.write_peer_msg(vk, , event.object.text)
            print("-------------------")


while True:
    try:
        check_time()
        if __name__ == '__main__':
            main()
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(4)
        continue


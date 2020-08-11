import vk_api
import random
import time

# файлы бота
import config
import bot_database
import bot_vk


# gay_check = ["пидр", "не пидр", "вообще девочка"]


def write_peer_msg(vk, peer_id, message, attachment=None):  # ответить пользователю в беседе
    random_id = vk_api.utils.get_random_id()
    try:
        vk.method('messages.send', {'peer_id': peer_id, 'message': message, "random_id": random_id, 'attachment': attachment})
    except:
        print("\n Что то пошло не так \n")


# def write_user_msg(vk, user_id, message): #ответить пользователю в личке
#     random_id = vk_api.utils.get_random_id()
#     vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


def check_message(vk, vkapi, object, sleep):
    if sleep == 1:
        if object.text.lower() == "!хелп" or object.text.lower() == "!help":
            message = '''
            !хелп или !help - узнать команды бота
            !проверка - проверка на гейство
            !сколько / !всего - узнать сколько сообщений в чате вы написали  за день/всего
            !топ - топ по сообщениям
            !топ всего - весь топ (только для админов)
            !врет? - ответ, врет ли человек
            !поиск - найти гея в чате
            '''
            write_peer_msg(vk, object.peer_id, message)

        elif object.text.lower() == "!сколько":
            message = bot_vk.get_user_name(object.from_id, vkapi) + ', сегодня вы написали ' + bot_database.count_from_database(
                object.from_id) + ' сообщений'
            write_peer_msg(vk, object.peer_id, message)

        elif object.text.lower() == "!всего":
            message = bot_vk.get_user_name(object.from_id, vkapi) + ', всего вы написали ' + bot_database.full_count_from_database(
                object.from_id) + ' сообщений'
            write_peer_msg(vk, object.peer_id, message)

        elif object.text.lower() == "!топ":
            count_list = bot_database.top_count_from_database()
            message = ''
            for x in count_list:
                message = message + x + '\n'
            write_peer_msg(vk, object.peer_id, message)

        elif object.text.lower() == "!топ всего":
            if str(object.from_id) in config.admins_id:
                count_list = bot_database.top_full_count_from_database()
                message = ''
                for x in count_list:
                    message = message + x + '\n'
                write_peer_msg(vk, object.peer_id, message)
            else:
                write_peer_msg(vk, object.peer_id, 'Команда только для админов')

        elif object.text.lower() == "!проверка":
                x = random.choice(["пидр", "не пидр", "вообще девочка"])
                message = "@id" + str(object.from_id) + ", ты " + x
                write_peer_msg(vk, object.peer_id, message)

        elif object.text.lower() == "!врет?":
                message = random.choice(["да, врет", "нет, не врет"])
                write_peer_msg(vk, object.peer_id, message)

        elif object.text.lower() == "админ пидр" or object.text.lower() == "админ пидор":
            write_peer_msg(vk, object.peer_id, 'Сам ты пидор')

        elif object.text.lower() == "!поиск":
            message = bot_vk.get_user_name(object.from_id,
                                           vkapi) + ', ты пидарасина '
            write_peer_msg(vk, object.peer_id, message)
            # user_id, name = bot_database.gay_test()
            # attachment_name, attachment_photo, congratulations = bot_vk.get_random_gay()
            # write_peer_msg(vk, object.peer_id, 'Выполняется поиск..')
            # time.sleep(1)
            #
            # message = congratulations + '\n' + name + ', ты ' + attachment_name + '!'
            # write_peer_msg(vk, object.peer_id, message, attachment = attachment_photo)

        # elif object.text.lower() == "!тест":
        #     bot_database.set_block(object.from_id)

        elif object.text.lower() == "!обновить базу":
            if str(object.from_id) == '':
                write_peer_msg(vk, object.peer_id, 'База обновлена')
                bot_database.today_count()

        elif object.text.lower() == "!спать":
            if str(object.from_id) in config.admins_id:
                write_peer_msg(vk, object.peer_id, 'Спокойной ночи')
                sleep = 0
        else:
            # добавляем в ДБ
            bot_database.add_to_database(object.from_id, vkapi)

    elif object.text.lower() == "!вставай" or object.text.lower() == "!проснись":
        if str(object.from_id) in config.admins_id:
            write_peer_msg(vk, object.peer_id, 'Я работать')
            sleep = 1
    else:
        # добавляем в ДБ
        bot_database.add_to_database(object.from_id, vkapi)

    return sleep
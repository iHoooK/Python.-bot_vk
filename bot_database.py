import pymysql.cursors
import random

# файлы бота
import config
import bot_vk
import bot_logs


def get_connection():
    connection = pymysql.connect(host='host',
                                 user='user',
                                 password='password',
                                 db='db',
                                 charset='utf8mb4', )
    return connection


def add_to_database(user_id, vkapi):  # добавить пользователя в базу / прибавить count
    # Создаем новую сессию
    connection = get_connection()
    # Будем получать информацию от сюда
    cursor = connection.cursor()
    # проверка наличия user_id в базе
    sql = "SELECT user_id FROM users WHERE user_id=%s"
    x = cursor.execute(sql, user_id)
    # если пользователь нашелся, увеличиваем кол-во сообщений
    if x:
        # добавить +1 к счетчику сообщений
        plus_count(user_id, cursor)
    # если пользователь не нашелся, загружаем его в базу
    else:
        # Наш запрос
        sql = "INSERT INTO users (user_id, name, count, full_count) VALUES (%s, %s, %s, %s)"  # ON DUPLICATE KEY UPDATE Mode = %s
        # Выполняем наш запрос и вставляем свои значения
        full_name = bot_vk.get_user_name(user_id, vkapi)
        cursor.execute(sql, (user_id, full_name, 1, 1))
    # Делаем коммит
    connection.commit()
    # Закрываем подключение
    connection.close()


def plus_count(user_id, cursor):  # добавить +1 к счетчику сообщений
    sql = "SELECT count, full_count FROM users WHERE user_id=%s"
    cursor.execute(sql, user_id)
    counts = cursor.fetchall()
    count = counts[0][0]
    full_count = counts[0][1]
    new_count = count + 1
    new_full_count = full_count + 1
    sql = "UPDATE users SET count = %s, full_count = %s WHERE count = %s AND user_id=%s"
    val = (new_count, new_full_count, count, user_id)
    cursor.execute(sql, val)


def count_from_database(user_id):  # вернуть кол-во сообщений определенного пользователя за день
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT count FROM users WHERE user_id = %s"
    cursor.execute(sql, user_id)
    # Получаем запрашиваемые данных и заносим их в переменные
    try:
        count = cursor.fetchall()[0][0]
    except:
        count = 0
    connection.close()
    return str(count)


def full_count_from_database(user_id):  # вернуть кол-во сообщений определенного пользователя за все время
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT full_count FROM users WHERE user_id = %s"
    cursor.execute(sql, user_id)
    # Получаем запрашиваемые данных и заносим их в переменные
    try:
        count = cursor.fetchall()[0][0]
    except:
        count = 0
    connection.close()
    return str(count)


def today_count():  # в 00:00:00  обновить базу подсчета сообщений и обнулить count + block за сегодня
    connection = get_connection()
    cursor = connection.cursor()

    sql = "UPDATE users SET count = %s"
    val = (0)
    cursor.execute(sql, val)

    sql = "UPDATE users SET block = %s"
    val = (-1)
    cursor.execute(sql, val)

    connection.commit()
    connection.close()


def top_count_from_database():  # вернуть топ по сообщениям за день
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT name, count FROM users WHERE count > 0 ORDER BY count DESC"
    cursor.execute(sql)
    result = cursor.fetchall()
    count_list = ['Топ за сегодня','']
    for x in result:
        i = str(x[0]) + ': ' + str(x[1]) + ' сообщений'
        count_list.append(i)
    return count_list


def top_full_count_from_database():  # вернуть топ по сообщениям за все время
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT name, full_count FROM users ORDER BY full_count DESC"
    cursor.execute(sql)
    result = cursor.fetchall()
    count_list = ['Топ за все время','']
    for x in result:
        i = str(x[0]) + ': ' + str(x[1]) + ' сообщений'
        count_list.append(i)
    return count_list


def gay_test():  # поиск гея в чате по базе
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT user_id, name FROM users WHERE count > 0 ORDER BY id"
    users = cursor.execute(sql)
    random_user = random.randint(0, users-1)
    user = cursor.fetchall()[random_user]
    user_id = user[0]
    name = user[1]
    return user_id, name

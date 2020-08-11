import csv
import time

# файлы бота
import config
import bot_vk

def get_time(): #получает время в текстовом виде
    hours = time.strftime("%H")
    hours = int(hours) + 3
    if hours > 23:
        hours = hours - 24
    log_time = f'{hours}:{str(time.strftime("%M:%S"))}'
    return hours, log_time

def create_file_name():
    hours, log_time = get_time()
    data1 = str(time.strftime("%d%m%Y"))
    data2 = str(time.strftime("%M%S"))
    file_name = 'logs/log'+data1 + '_' + str(hours) + data2 + '.csv'
    return file_name


def create_file(path):  # создает файл
    with open(path, 'w', newline='', errors='ignore') as file:  # открытие с записью
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Время', 'Имя', 'Сообщение'])  # первая строка - заголовки


def get_log(user_id, message, vkapi):  # логи программы
    hours, log_time = get_time()
    print(f'Время: {log_time}')
    full_name = bot_vk.get_user_name(user_id, vkapi)
    print('Отправитель: ', full_name)
    print('Сообщение: ', message)
    print('id:', user_id)
    save_file(log_time, full_name, message, config.log_file)  # сохраняет файл


def save_file(log_time, full_name, message, path):  # сохраняет файл
    with open(path, 'a', newline='', errors='ignore') as file:  # открытие с добавлением
        writer = csv.writer(file, delimiter=';')
        writer.writerow([log_time, full_name, message])  # новая строка с данными

import sys
import wmi
import os
from check_key import read_file
from datetime import datetime, timedelta
from time import sleep
from datetime import datetime
from key_generator.generate_key_file import write_key
import math


c = wmi.WMI()

log = open('log.txt', 'a', encoding='utf-8')


def get_path_secret_file(disks, filename):
    for disk in disks:
        try:
            if filename not in os.listdir(disk[0]):
                continue
        except PermissionError:
            continue
        return disk

# disks = [(drive.Caption, drive.VolumeSerialNumber) for drive in c.Win32_LogicalDisk()]
# disk = get_path_secret_file(disks, 'secret.txt')
# owner_info = dict()
# owner_info = read_file(f'{disk[0]}\\secret.txt', disk[1])
def check(f):
    disks = [(drive.Caption, drive.VolumeSerialNumber) for drive in c.Win32_LogicalDisk()]
    disk = get_path_secret_file(disks, 'secret.txt')
    if not disk:
        if f:
            log.write(f'{datetime.now()}: UNKNOWN: запускают программу без ключа\n')
        else:
            log.write(f'{datetime.now()}: {disk[0]}: ключ был изъят\n')
        print('У вас нет доступа')
        input('Вставьте ключ и нажмите любую клавишу: ')
        return

    log.write(f'{datetime.now()}: UNKNOWN: ключ найден на флешке {disk[1]}\n')

    key = read_file(f'{disk[0]}\\secret.txt', '')

    end_date = datetime.strptime(key['date_creation'], '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes=key['lifetime'])

    if end_date < datetime.now():
        log.write(f'{datetime.now()}: {key["owner"]}: ключ действия истек\n')
        print('Ключ действия истек')
        exit()

    log.write(f'{datetime.now()}: {key["owner"]}: успешно запустил программу в доступном {key["level"]}\n')
    return key


menu = [
    (1, 'Завершить работу'),
    (1, 'Сложить 2 числа'),
    (1, 'Вычесть 2 числа'),
    (2, 'Умножить 2 числа'),
    (2, 'Разделить 2 числа'),
    (3, 'Возвести число в степень'),
    (3, 'Вычислить корень'),
]


def do(s):
    key = check(False)
    while not key:
        key = check(False)
        sleep(2)
    print(f'{key["owner"]}, ты выбрал {s}')

# print(f'Владелец: {owner_info["owner"]}')
# print(f'Дата и время создания ключа: {owner_info["date_creation"]}')
# print(f'Время жизни: {owner_info["lifetime"]}')
# print(f'Уровень доступа: {owner_info["level"]}\n')
first = True
while True:
    key = check(first)
    if not key:
        sleep(5)
        continue
    first = False
    for i, e in enumerate(menu):
        if e[0] > key['level']:
            continue
        print(f'{i+1}) {e[1]}')

    select = int(input('Выберите пункт меню: '))
    if select > len(menu):
        print('Выберите правильный пункт меню')
        continue
    do(menu[select - 1][1])
    sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

    if select == 1:
        sys.exit()
    else:
        if select == 2:
            a, b = map(int, input('Введите 2 числа: ').split())
            print(f'Сумма равна {a + b}')
        if select == 3:
            a, b = map(int, input('Введите 2 числа: ').split())
            print(f'Разность равна {a - b}')
        if select == 4:
            a, b = map(int, input('Введите 2 числа: ').split())
            print(f'Произведение равно {a * b}')
        if select == 5:
            a, b = map(int, input('Введите 2 числа: ').split())
            print(f'Частное равно {a / b}')
        if select == 6:
            a = int(input('Введите число: '))
            b = int(input('Введите степень: '))
            print(f'Число {a} в степени {b} равно {pow(a, b)}')
        if select == 7:
            a = int(input('Введите число: '))
            print(f'Квадратный корень из числа {a} равен {math.sqrt(a)}')

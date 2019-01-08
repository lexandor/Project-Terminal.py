#TODO: Добавить проверку на существование базы данных
#TODO: Добавить возможность просматривать содержание
#TODO: Добавить возможность редактировать записи
#TODO: Сделать визуальное оформлнеие (цвет шрифтов)
#TODO: Реализовать поиск по записям
#TODO: Пофиксить перскок NUM при работе со списком записей



import sqlite3
import datetime

def compliteCreate(title, time, content):
    # Завершение создания записи(проверка на выход)
        cond = input('Вы увернны что хотите уйти? \n 1. - Да \n 2. - Нет \n >> ')
        if cond == '1':
            pushContent(title, time, content)
        elif cond == '2':
            content += input('Введите текст: \n >> ')
            print("new" + content)
            compliteCreate(title, time, content)  
        else:
            pass
        print(content)
        return content

def pushContent(title, time, content):
    # Отправка данных в базу
        conn = sqlite3.connect('DailyBook.sqlite')
        cursor = conn.cursor()

        cursor.execute("insert into Days (title, time, content) values ('%s','%s','%s')"%(title, time, content))
        conn.commit()

        conn.close()

def create():
    # Создание записи
    title = input('Введите Заголовок: ')
    time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    content = input('Введите текст: \n >> ')
    content = compliteCreate(title, time, content) # Проверка на выходе

    #print(title, "|", time, "|", content) #DEBUG
    
def createDEBUG():
    # Создает таблицу со значениями от 1 до 100. Нужно для дебагинга
    for i in range(100):
        title = str(i)
        time = str(i)
        content = str(i)
        pushContent(title, time, content)

def pullContent(startPos = 0, EndPos = 10):
    # Получение строк из базы
    conn = sqlite3.connect('DailyBook.sqlite')
    cursor = conn.cursor()

    cursor.execute("select * from Days order by time desc limit '%s','%s'"%(startPos, EndPos))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def printRows(rows, num = 0):
    # Вывод списка записей
    if rows is not None: 
        for row in rows:
            print(' ' + '{0: <4}'.format(str(num + 1) + ". ") + "- " + '{0: <10}'.format(str(row[0])) + " " + str(row[1]))
            #print(" " + str(row[2]))
            num += 1                   
    else:
        print('Нет записей')
    #print(num)
    return num

def read():
    # Чтение записей
    print('Выберите запись: \n >> ')

    OFFSET = 10

    rows = pullContent()
    num = printRows(rows)

    while True: # Выбор записей
        print('__________________ \n')
        action = input('<= L   Выберите запись   R =>    | 0. - Выход \n >> ')
        print(action)
        if action == '0' or action == 'e':
            break
        elif action.lower() == 'l':
            # Выводит предидущую страницу
            rows = pullContent(num, OFFSET) # отступ в базе вверх на 10
            num = printRows(rows, num)
            num -= 20
        elif action.lower() == 'r':
            # Выводит следующую страницу
            rows = pullContent(num, OFFSET) # отступ в базе вниз на 10
            num = printRows(rows, num)
        elif action == 'a' or action == 'all':
            rows = pullContent(0, 100000000)
            num = printRows(rows)
        elif action == num:
            pass
        else:
            print('Ошибка ввода')

    

def createDB():
    # Создает базу данных
    conn = sqlite3.connect('DailyBook.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE if not exists Days (title text, time text, content text)''')
    conn.close()
    print('Таблица создана!')

def MAIN():
    # Приложение
    while True:
        print('========================')
        print('Zenda Oracle \n')

        doing = input(
            " Menu: \n 1. Создать запись \n 2. Помощь \n 3. Просмотреть запись \n 4. Создать базу данных \n >> "
        )

        if doing == '1':
            create()
        elif doing == '2' or doing == 'help' or doing == 'h':
            print('\n ' + '{0: ^30}'.format('О ПРИЛОЖЕНИИ') + '''
 Приложение является реализацией старомодного терминала для записи, 
 чтения и редактирования заметок. \n
 Данный проект является тренровочным. В частности для отработки навыков работы 
 с базами данных(sqlite3) \n
 ''' + ' ' + '{0: ^30}'.format('ОБ АВТОРЕ') + '''
 author: PLEXER
 github: https://github.com/lexandor
 lang: Python 3.1.7
 ''')  
        elif doing == '3':
            read()
        elif doing == '4':
            createDB()
        elif doing == 'db':
            createDEBUG()
        elif doing == 'exit' or doing == 'e':
            break
        else:
            print('Нет такого действия')

MAIN()


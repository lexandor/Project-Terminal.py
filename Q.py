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


    rows = pullContent()
    num = printRows(rows)
    print('g: ' + str(num))

    while True: # Выбор записей
        print('__________________ \n')
        action = input('<= L   Выберите запись   R =>    | 0. - Выход \n >> ')
        print(action)
        if action == '0' or action == 'e':
            break
        elif action.lower() == 'l':
            print('l St: ' + str(num))
            rows = pullContent(num - 10, num) # отступ в базе вверх на 10
            print('l Mid ' +  str(num))
            num = printRows(rows)
            print('l End: ' + str(num))
        elif action.lower() == 'r':
            print('r St: ' + str(num))
            rows = pullContent(num, num + 10) # отступ в базе вниз на 10
            print('r Mid ' +  str(num))
            num = printRows(rows)
            print('r End: ' + str(num))
        elif action == 'a' or action == 'all':
            rows = pullContent(0, 100000000)
            num = printRows(rows)
        elif action == num:
            pass
        else:
            print('Ошибка ввода')

    

def createDB():
    conn = sqlite3.connect('DailyBook.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE if not exists Days (title text, time text, content text)''')
    conn.close()
    print('Таблица создана!')

while True:
    print('========================')
    print('Zenda Oracle \n')

    doing = input(
        " Menu: \n 1. Создать запись \n 2. Редактировать запись \n 3. Просмотреть запись \n 4. Создать базу данных \n >> "
    )

    if doing == '1':
        create()
    elif doing == '2':
        pass
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


import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# cur.execute("CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")  # создание таблицы

cycle = True
number = 4000000000000000
last_number = 0
counter1 = 0
balance = 0
all_numbers = []

while cycle:
    sum_ = 0
    print("""
1. Create an account
2. Log into account
0. Exit
>""", end='')
    cur.execute('SELECT number, pin FROM card;')
    row = cur.fetchall()
    for card_cycle in row:
        if card_cycle[0] not in all_numbers:
            all_numbers.append(card_cycle[0])
    user_input = int(input())
    if user_input == 0:
        cycle = False
        print("Bye!")

    elif user_input == 10:
        cur.execute('DELETE FROM card')
        print("all data deleted")
        conn.commit()
    elif user_input == 1:

        number = 4000000000000000                                                                # создание номера карты
        number += random.randint(0, 99999999) * 10
        for i in range(15):
            if i % 2 == 0:
                snumber = str(number)
                lnumber = list(snumber)
                lnumber[i] = int(str(lnumber[i])) * 2
                if int(lnumber[i]) > 9:
                    lnumber[i] = int(str(lnumber[i])) - 9
                sum_ += int(lnumber[i])
            elif i % 2 == 1:
                snumber = str(number)
                lnumber = list(snumber)
                sum_ += int(lnumber[i])
        last_number = 0
        if sum_ % 10 != 0:
            last_number = 10 - sum_ % 10
        sum_ = 0
        number += last_number
        numberf = str(number)

        pin = random.randint(0, 9999)                                                              # создание пина карты
        if pin < 1000:
            pinf = "0" + str(pin)
            if pin < 100:
                pinf = "00" + str(pin)
                if pin < 10:
                    pinf = "000" + str(pin)
        else:
            pinf = str(pin)

        card = [(1, numberf, pinf, 0)]
        cur.executemany("INSERT INTO card VALUES (?,?,?,?)", card)                                # введение данных в бд
        conn.commit()

        card = []
        print("Your card has been created")
        print("Your card number:")
        print(numberf)                                                                  # вывод данных о созданной карте
        print("Your card PIN:")
        print(pinf)

    elif user_input == 2:
        print("Enter your card number:")
        cnumber = input()
        # for card_cycle in row:
        if cnumber in all_numbers:                                                            # запрос авторизации
            print("Enter your PIN:")
            cpin = input()
            if cpin == row[all_numbers.index(cnumber)][1]:

                print("You have successfully logged in!")
                cycle1 = True
                while cycle1:                                                                      # список действий
                    print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>""", end='')
                    user_input1 = int(input())

                    if user_input1 == 0:
                        cycle = 0
                        cycle1 = 0                                                              # выход из программы
                        print("Bye!")

                    elif user_input1 == 1:
                        sql = 'SELECT balance FROM card WHERE number = "'+ cnumber + '"'
                        cur.execute(sql)
                        b = str(cur.fetchall())                                                # отображение баланса
                        b = int(b[2:len(b) - 3])
                        print("Balance: {}".format(b))

                    elif user_input1 == 2:
                        print("Enter income:")
                        income = int(input())
                        sql = 'SELECT balance FROM card WHERE number = "'+ cnumber + '"'
                        cur.execute(sql)
                        b = str(cur.fetchall())
                        b = int(b[2:len(b) - 3])
                        b += income
                        sql = """UPDATE card SET balance = ? WHERE number = ?"""                # пополнение баланса
                        cur.execute(sql, (b, cnumber))
                        conn.commit()
                        print("Income was added!")

                    elif user_input1 == 3:                                                 # перевод на другую карту
                        print("Transfer")
                        print("Enter card number:")
                        other_card_number = input()             # ввод номера карту на которую надо перевести деньги

                        sql = 'SELECT number FROM card WHERE number = "' + other_card_number + '"'
                        cur.execute(sql)                                                 # проверка на существование
                        exist_card = bool(cur.fetchall())

                        last_number = other_card_number[15]
                        correct_ocn = other_card_number
                        other_card_number = other_card_number[:15]
                        for i in range(14):
                            if i % 2 == 0:
                                other_card_number = list(other_card_number)
                                other_card_number[i] = int(str(other_card_number[i])) * 2
                                if int(other_card_number[i]) > 9:
                                    other_card_number[i] = int(str(other_card_number[i])) - 9
                                sum_ += int(other_card_number[i])
                            elif i % 2 == 1:                                           # проверкаа по алгоритму Луна
                                other_card_number = list(other_card_number)
                                sum_ += int(other_card_number[i])
                        if sum_ % 10 != 0:
                            last_number1 = 10 - sum_ % 10
                        else:
                            last_number1 = 0

                        sql = 'SELECT balance FROM card WHERE number = "' + cnumber + '"'
                        cur.execute(sql)
                        b = str(cur.fetchall())                                        # вывод баланса текущей карты
                        b = int(b[2:len(b) - 3])

                        if correct_ocn == cnumber:
                            print("You can't transfer money to the same account!")
                        elif not exist_card:
                            if correct_ocn[:6] != '400000':
                                print("Such a card does not exist.")
                            elif last_number != last_number1:                                     # проверка на ошибка
                                print("Probably you made a mistake in the card number. Please try again!")
                            else:
                                print("Such a card does not exist.")

                        else:
                            print("Enter how much money you want to transfer:")
                            trans_money = int(input())
                            if trans_money < b:
                                print("Success!")

                                # sql = 'SELECT balance FROM card WHERE number = "' + other_card_number + '"'
                                cur.execute('SELECT balance FROM card WHERE number = "' + correct_ocn + '"')
                                bo = str(cur.fetchall())
                                bo = int(bo[2:len(bo) - 3])

                                sql = """UPDATE card SET balance = ? WHERE number = ?"""
                                cur.execute(sql, (bo + trans_money, correct_ocn))

                                sql = 'SELECT balance FROM card WHERE number = "' + cnumber + '"'
                                cur.execute(sql)
                                b = str(cur.fetchall())
                                b = int(b[2:len(b) - 3])
                                b = b - trans_money
                                sql = """UPDATE card SET balance = ? WHERE number = ?"""
                                cur.execute(sql, (b, cnumber))
                                conn.commit()
                            else:
                                print("Not enough money!")
                        last_number1 = 0
                        last_number = 0

                    elif user_input1 == 4:
                        cur.execute('DELETE FROM card WHERE number = "' + cnumber + '"')         # удаление аккаунта
                        conn.commit()
                        print('The account has been closed!')
                        cycle1 = 0
                    elif user_input1 == 5:
                        print("You have successfully logged out!")                               # выход из аккаунта
                        cycle1 = 0

            else:
                print("Wrong card number or PIN!")
        else:
            print("Wrong card number or PIN!!!")                              # сообщения о некорректной авторизации

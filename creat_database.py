import sqlite3

# def create_database(name):
#     name_s = '%s.db'%name
#     conn = sqlite3.connect('D:\FPT_University\Spring_2023\AIP391\Test\Database\%s'%name_s)
#
#     c = conn.cursor()
#
#     c.execute(f"Drop table if exists {name}")
#
#     c.execute(f"create table {name}(id integer primary key,NameRoom text ,Address text,roomNum integer,Area text, Money float)")
#
#     nameRoom = input("Enter Name Motel: ")
#     address = input("Enter Address: ")
#     roomNum = int(input("Enter Room Number: "))
#     area = input("Enter Area: ")
#     money = float(input("Enter Money: "))
#
#     #
#     c.execute(f"Insert into {name}(NameRoom, address, roomNum, area, money) values (?, ?, ?, ?, ?)", (nameRoom ,address, roomNum, area, money,))
#
#     conn.commit()
#
#     conn.close()

def create_database(name, table):
    conn = sqlite3.connect(f'D:/Nam 2 FPT/chatbot proj/Database\{name}.db')

    c = conn.cursor()

    c.execute(f"Drop table if exists {table}")

    c.execute(f"create table {table}(id integer primary key, NameBoss text,NameRoom text ,Address text,roomNum integer,Area text, Money text,"
              f"ElectricityBill text, WaterMoney text, OtherCosts text,"
              f"Facebook text, Gmail text, SDT text)")
    #
    # nameRoom = input("Enter Name Motel: ")
    # address = input("Enter Address: ")
    # roomNum = int(input("Enter Room Number: "))
    # area = input("Enter Area: ")
    # money = float(input("Enter Money: "))
    #
    # #
    # c.execute(f"Insert into {name}(NameRoom, address, roomNum, area, money) values (?, ?, ?, ?, ?)", (nameRoom ,address, roomNum, area, money,))

    conn.commit()

    conn.close()

def replace_data(name, id, table):
    conn = sqlite3.connect(f"D:/Nam 2 FPT/chatbot proj/Database\{name}.db")

    c = conn.cursor()

    while True:
        print("1. Địa chỉ\n"
              + "2. Số lượng phòng\n"
              + "3. Giá Tiền\n"
              + "4. Diện tích\n"
              + "5. Thông tin chủ trọ\n"
              + "0. Quit")
        choice = int(input("Nhập sự lựa chọn:"))
        if choice == 1:
            id = str(id)
            address = input("Enter Address: ")
            c.execute(f"Update {table} set address = ? where NameRoom = ?", (address, id))
            conn.commit()
        elif choice == 2:
            roomNum = int(input("Enter Room Number: "))
            id = str(id)
            c.execute(f"Update {table} set roomNum = ? where NameRoom = ?", (roomNum,id))
            conn.commit()
        elif choice == 3:
            area = input("Enter Area: ")
            id = str(id)
            c.execute(f"Update {table} set Area = ? where NameRoom = ?", (area,id))
            conn.commit()
        elif choice == 4:
            id = str(id)
            money = input("Enter Money: ")
            electric_bill = input("Enter Electric Bill: ")
            water_money = input("Enter Water Money: ")
            otherCosts = input("Enter Other Costs: ")
            c.execute(f"Update {table} set Money = ? where NameRoom = ?", (money,id))
            c.execute(f"Update {table} set ElectricityBill = ? where NameRoom = ?", (electric_bill, id))
            c.execute(f"Update {table} set WaterMoney = ? where NameRoom = ?", (water_money, id))
            c.execute(f"Update {table} set OtherCosts = ? where NameRoom = ?", (otherCosts, id))
            conn.commit()
        elif choice == 5:
            id = str(id)
            nameBoss = input("Enter Name Boss: ")
            facebook = input("Enter Facebook: ")
            gmail = input("Enter Gmail: ")
            sdt = input("Enter SDt: ")
            c.execute(f"Update {table} set NameBoss = ? where NameRoom = ?", (nameBoss, id))
            c.execute(f"Update {table} set Facebook = ? where NameRoom = ?", (facebook, id))
            c.execute(f"Update {table} set Gmail = ? where NameRoom = ?", (gmail, id))
            c.execute(f"Update {table} set SDT = ? where NameRoom = ?", (sdt, id))
            conn.commit()
        elif choice == 0:
            break
        else:
            print("Not valid!")
    conn.close()



def last_data(name, name_motel,table):
    conn = sqlite3.connect(f"D:/Nam 2 FPT/chatbot proj/Database\{name}.db")

    c = conn.cursor()
    c.execute(f"SELECT * FROM {table} WHERE NameRoom = ?",(name_motel,))
    last = c.fetchone()

    return last

    conn.close()

# arr = last_data("Tro","Chí Thiện")
# print(arr)
# print(arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9])

def list_name(name, nameCol, table):
    list_m = []
    conn = sqlite3.connect(f"D:/Nam 2 FPT/chatbot proj/Database\{name}.db")

    c = conn.cursor()
    # NameRoom
    c.execute(f"Select {nameCol} from {table}")
    list_motel = c.fetchall()
    conn.commit()
    for i in list_motel:
        list_m.append(i[0])
    return list_m

# print(list_name("Tro", "NameRoom"))

def add_database(name, nameRoom):

    conn = sqlite3.connect(f"D:/Nam 2 FPT/chatbot proj/Database\{name}.db")

    c = conn.cursor()
    # nameBoss = input("Enter Name Boss:")
    # address = input("Enter Address: ")
    # roomNum = int(input("Enter Number Room: "))
    # area = input("Enter Area: ")
    # money = input("Enter Money: ")
    # electricBill = input("Enter Electric Bill: ")
    # waterMoney = input("Enter Water Money: ")
    # otherCost = input("Enter Orther Costs: ")
    # facebook = input("Enter Facebook: ")
    # gmail = input("Enter Gmail: ")
    # sdt = input("Enter Number Phone: ")
    # c.execute(f"insert into tro (NameBoss, NameRoom, Address, roomNum, Area, Money,"
    #           f"ElectricityBill, WaterMoney, OtherCosts, Facebook, Gmail, SDT) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #           (nameBoss, nameRoom, address, roomNum, area, money, electricBill, waterMoney, otherCost, facebook, gmail,sdt,))

    c.execute(f"insert into tro (NameRoom) values (?)",
              (nameRoom,))

    conn.commit()
    conn.close()

# add_database("List_Motel")

def delete_database(name,name_t,table):
    conn = sqlite3.connect(f'D:/Nam 2 FPT/chatbot proj/Database\{name}.db')
    c = conn.cursor()
    c.execute(f"delete from {table} where NameRoom = ?",(name_t,))
    conn.commit()

    conn.close()

# delete_database("List_Motel","Bảo Anh","tro")
# delete_database("accommodation_list")

def delete_database2(name,name_t,table):
    conn = sqlite3.connect(f'D:/Nam 2 FPT/chatbot proj/Database\{name}.db')
    c = conn.cursor()
    c.execute(f"delete from {table} where Account = ?",(name_t,))
    conn.commit()

    conn.close()

def create_database_2(name, account, table):
    conn = sqlite3.connect(f'D:/Nam 2 FPT/chatbot proj/Database\{name}.db')

    c = conn.cursor()

    # c.execute(f"Drop table if exists {table}")
    #
    # c.execute(f"create table {table}(id integer primary key,Account text)")

    c.execute(f"Insert into {table}(Account) values (?)", (account,))

    conn.commit()

    conn.close()

# create_database_2("Waiting_cf","Bảo Anh","Account")
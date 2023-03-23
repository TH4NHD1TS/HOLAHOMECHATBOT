from webbrowser import get

from scipy.signal import lti
from sqlalchemy.sql.util import _repr_base

from creat_database import *
# from function_project import get_file
import re
import io
import json

namedb = "List_Motel"

def creat_acc(arr1, arr2, arr3, arr4, arr5):

    address = input("Enter Address:")
    arr1.append(address)
    roomNum = input("Enter Room Number:")
    arr2.append(roomNum)
    money = input("Enter Money:")
    arr3.append(money)
    area = input("Enter Area:")
    arr4.append(area)
    facebook = input("Facebook:")
    mail = input("Mail:")
    phone = input("Number phone:")
    arr5.append([facebook, mail, phone])

    yield arr1
    yield arr2
    yield arr3
    yield arr4
    yield arr5

def check_validate():
    pat = re.compile(r'[A-Za-z0-9 ]+', re.UNICODE)

    while True:
        Id = input("Enter ID:")
        try:
            if re.match(pat, Id):
                return Id
            print("Re-enter!")
        except:
            print("Re-enter! Please!")

def creat_form(namedb, name,table):
    lt_data = last_data(namedb,name,table)
    form = f"Địa chỉ: {lt_data[3]}\n\tSố lượng phòng: {lt_data[4]}\n\tDiện tích: {lt_data[5]}\n\tGiá tiền: {lt_data[6]}\n\tTiền Điện: {lt_data[7]}\n\tTiền Nước: {lt_data[8]}\n\tChi phí khác: {lt_data[9]}"

    return form

def creat_form_s(Id, arr,table):
    form = {'tag': Id, 'patterns':[Id], 'responses':arr,
            'Forder': [creat_form(namedb, Id, table)]}
    return form

def creat_infor(namedb, name, table):
    lt_data = last_data(namedb, name,table)
    form = f"Tên chủ trọ: {lt_data[1]}\n\tFacebook: {lt_data[10]}\n\tEmail: {lt_data[11]}\n\tSố Điện Thoại: {lt_data[12]}"
    return form

def creat_infor_s(name, arr,table):
    form = {'tag': f"Chủ trọ {name}", 'patterns': [f"Chủ trọ {name}"],
            'responses': arr, 'Forder':[creat_infor(namedb,name,table)]}
    return form

def get_file(path):
    with io.open('intents-_2.json', 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data

# arr_tro = ['MinhAnh', 'TuấnCường', 'CânThủy', 'Kiều Quyên']
def main():
    Id = check_validate()
    arr_responses = ["Đây là thông tin về trọ "]
    arr_responses_2 = ["Dưới đây là thông tin của chủ trọ ", "Tôi gửi bạn các thông tin về chủ trọ ",
            "Đây là các thông tin bạn biết về chủ trọ "]
    list_motel = list_name(namedb, "NameRoom","tro")

    if Id in list_motel:
        data = get_file('intents-_2.json')
        for i in data['intents']:
            if Id == i['tag']:
                replace_data(namedb, Id,"tro")
                if i['tag'] == "Chủ trọ " + Id:
                    i['Forder'][0] = creat_infor(namedb, Id,"tro")
                i['Forder'][0] = creat_form(namedb,Id,"tro")
                with open('intents-_2.json', 'w', encoding='UTF-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        if Id in list_name("accommodation_list","NameRoom","accommodation_list"):
            add_database(namedb)
            data = get_file('intents-_2.json')
            for i in data['intents']:
                if i['tag'] == 'Trọ':
                    i['Forder'][0] += '\n\t'+Id

            form = creat_form_s(Id,arr_responses,"tro")
            data['intents'].append(form)
            form_2 = creat_infor_s(Id,arr_responses_2,"tro")
            data['intents'].append(form_2)
            with open('intents-_2.json', 'w', encoding='UTF-8') as f:
                json.dump(data, f,ensure_ascii=False, indent= 4)

        else:
            print("Account not existed!")


if __name__== '__main__':
    main()
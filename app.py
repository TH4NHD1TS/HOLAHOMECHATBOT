from webbrowser import get

from flask import Flask, render_template, request, jsonify, session, flash,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from function_project import *
from creat_database import *
import pickle

from update import creat_infor, creat_form, creat_form_s, creat_infor_s

app = Flask(__name__)
app.config["SECRET_KEY"] = "quyhtfptuniversity"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Nam 2 FPT/chatbot proj/DatabaseList_Motel.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Nam 2 FPT/chatbot proj/Database/Waiting_cf.db'
db = SQLAlchemy(app)

class Tro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NameBoss = db.Column(db.Text)
    NameRoom = db.Column(db.Text)
    Address = db.Column(db.Text)
    roomNum = db.Column(db.Integer)
    Area = db.Column(db.Text)
    Money = db.Column(db.Text)
    ElectricityBill = db.Column(db.Text)
    WaterMoney = db.Column(db.Text)
    OtherCosts = db.Column(db.Text)
    Facebook = db.Column(db.Text)
    Gmail = db.Column(db.Text)
    SDT = db.Column(db.Text)
    # def __init__(self, id, email, phone):
    #     self.name = name
    #     self.email = email
    #     self.phone = phone

    def __repr__(self):
        return f"<Tro {self.id} {self.NameBoss} {self.NameRoom} {self.Address} {self.roomNum} {self.Area} {self.Money}" \
               f" {self.ElectricityBill} {self.WaterMoney} {self.OtherCosts} " \
               f"{self.Facebook} {self.Gmail} {self.SDT}"

class Waitingcf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Account = db.Column(db.Text)

    def __repr__(self):
        return f"Account {self.id} {self.Account}"

# @app.get("/")
@app.route('/user')
def hello_user():
    return render_template("base_t.html")

@app.post("/predict")
def predict():
    arr_tro = list_name("List_Motel","NameRoom","tro")
    context = {}
    data = pickle.load(open("models/training_data", "rb"))
    words = data['words']
    classes = data['classes']
    x_train = data['x_train']
    y_train = data['y_train']
    models = model_training(x_train, y_train)
    models.load('models/model.tflearn')
    text = request.get_json().get("message")
    account_list = list_name("Account","Account","Account")
    filename = account_list[len(account_list)-1]
    filename_s = f"{filename}.txt"
    save_file_comunication('D:/Nam 2 FPT/chatbot proj/demo/Comunication', filename_s,
                           '%s: %s' %(filename, text))
    classes_s = classify(text,classes,models,words)
    response_s = response(classes_s,arr_tro,get_file('intents-_2.json'),context)
    save_file_comunication('D:/Nam 2 FPT/chatbot proj/demo/Comunication', filename_s,
                           'Bot:%s' %response_s)
    message = {"answer": response_s}
    return  jsonify(message)

@app.route('/home')
@app.route('/')
def home():
    return render_template("button_s.html")

@app.route('/admin/login_admin', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':
        NameRoom = request.form['NameRoom']
        tro = Tro.query.filter_by(NameRoom=NameRoom).first()
        if tro:
            return render_template('edit.html', tro=tro)
        else:
            return render_template('index_admin.html')

@app.route('/admin')
def index():
    return render_template('index_admin.html')

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    NameBoss = request.form['NameBoss']
    NameRoom = request.form['NameRoom']
    Address = request.form['Address']
    roomNum = request.form['roomNum']
    Area = request.form['Area']
    Money = request.form['Money']
    ElectricityBill = request.form['ElectricityBill']
    WaterMoney = request.form['WaterMoney']
    OtherCosts = request.form['OtherCosts']
    Facebook = request.form['Facebook']
    Gmail = request.form['Gmail']
    SDT = request.form['SDT']
    tro = Tro.query.filter_by(NameRoom=NameRoom).first()
    tro.NameBoss = NameBoss
    tro.NameRoom = NameRoom
    tro.Address = Address
    tro.roomNum = roomNum
    tro.Area = Area
    tro.Money = Money
    tro.ElectricityBill = ElectricityBill
    tro.WaterMoney = WaterMoney
    tro.OtherCosts = OtherCosts
    tro.Facebook = Facebook
    tro.Gmail = Gmail
    tro.SDT = SDT
    db.session.commit()
    data = get_file('intents-_2.json')
    flag = False
    arr_responses = ["Đây là thông tin về trọ "]
    arr_responses_2 = ["Dưới đây là thông tin của chủ trọ ", "Tôi gửi bạn các thông tin về chủ trọ ",
                       "Đây là các thông tin bạn biết về chủ trọ "]
    for i in data['intents']:
        if NameRoom == i['tag']:
            flag = True
            i['Forder'][0] = creat_infor("List_Motel",NameRoom,"tro")
            if i['tag'] == "Chủ trọ " + NameRoom:
                i['Forder'][0] = creat_form("List_Motel",NameRoom,"tro")
            with open('intents-_2.json', 'w', encoding='UTF-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            flag = False
            if i['tag'] == 'Trọ':
                i['Forder'][0] =""
                for j in list_name("List_Motel","NameRoom","tro"):
                    i['Forder'][0] += j + ","
    if flag == False:
        form = creat_form_s(NameRoom, arr_responses, "tro")
        data['intents'].append(form)
        form_2 = creat_infor_s(NameRoom,arr_responses_2,"tro")
        data['intents'].append(form_2)
        with open('intents-_2.json', 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    success = "Update thành công!"
    return render_template('index_admin.html', success=success)

@app.route('/add_account')
def index2():
    return render_template('add_account.html')

@app.route('/add_account/convert', methods=['POST', 'GET'])
def add_accoount():
    if request.method == 'POST':
        account = request.form['account']
        list_wait = list_name("Waiting_cf","Account","Account")
        if account in list_wait:
            add_database("List_Motel",account)
            delete_database2("Waiting_cf",account,"Account")
            tro = Tro.query.filter_by(NameRoom=account).first()
            return render_template('edit.html', tro=tro)
        else:
            return render_template('add_account.html')

@app.route('/login', methods=["GET", "POST"])
@app.route("/")
def login():
    if request.method == "POST":
        user_name = request.form["name"]
        # with open('D:\FPT_University\Spring_2023\AIP391\Demo\Account_Management\Account.txt', mode='r', encoding='UTF-8') as f:
        #     line = f.readlines()
        account_list = list_name("Account", "Account", "Account")
        if user_name not in account_list:
            # save_file_comunication('D:\FPT_University\Spring_2023\AIP391\Demo\Account_Management', 'Account.txt',
            #                        user_name)
            create_database_2("Account",user_name,"Account")
            return redirect(url_for("hello_user",name=user_name))
        else:
            error_message = "Username vaild! Please re-enter!"
            return render_template("login.html",error_message=error_message)
    return render_template("login.html")


if __name__ =="__main__":
    app.run(debug=True)


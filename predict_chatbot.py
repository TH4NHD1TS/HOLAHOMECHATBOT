from function_project import *
import pickle
from creat_database import list_name
from time import sleep
import sys

data = pickle.load(open("models/training_data", "rb"))
words = data['words']
classes = data['classes']
x_train = data['x_train']
y_train = data['y_train']

intents = get_file('intents-_2.json')

model = model_training(x_train, y_train)

# print(model)

model.load('models/model.tflearn')

context = {}

user_id = check_validate_User_ID('D:\FPT_University\Spring_2023\AIP391\Demo\Account_Management\Account.txt', "Enter Name:")

filename = '%s.txt'%(user_id)
arr_tro = list_name("accommodation_list","NameRoom","accommodation_list")
while True:
    question = input()
    if question == 'ok' or question == 'bye':
        # line = "Cảm ơn cậu nhiều"
        print("Cảm ơn cậu nhiều")
        # chat_delay(line)
        break
    save_file_comunication('D:\FPT_University\Spring_2023\AIP391\Demo\Comunication', filename,
                           '%s: %s' % (user_id, question))
    return_list = classify(question,classes,model,words)
    # print(return_list)
    print(response(return_list, arr_tro, intents, context))
    # chat_delay(response(return_list, arr_tro, intents, context))
    save_file_comunication('D:\FPT_University\Spring_2023\AIP391\Demo\Comunication', filename,
                           'Bot:%s' % response(return_list, arr_tro, intents, context))

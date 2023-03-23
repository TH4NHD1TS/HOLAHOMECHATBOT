import nltk
from nltk.stem.lancaster import LancasterStemmer
# from nltk.stem import PorterStemmer
from pyvi import ViTokenizer

stemmer = LancasterStemmer()
# stemmer = PorterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random

import nltk
nltk.download('punkt')

import codecs

from time import sleep
import sys

import json

import re
import os

def get_file(path):
    json_data = codecs.open(path, 'r', 'utf8').read()
    intents = json.loads(json_data)

    return intents

def filter_data(intents, ignore_words):
    words = []
    classes = []
    documents = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            documents.append((w, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]

    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))

    yield words
    yield classes
    yield documents

def prepare_training(words, classes, documents):
    training = []
    output = []

    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    random.shuffle(training)
    # print(len(training))
    training = np.array(training, dtype=object)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    yield train_x
    yield train_y

# intents = get_file('intents-_2.json')
# ignore_words = ['?']
#
# words, classes, documents = filter_data(intents,ignore_words)
# training, x_train, y_train = prepare_training(words, classes, documents)
# print(words)
# print(documents)
# print(classes)
# print(x_train, '\n',y_train)

def model_training(x_train, y_train):
    net = tflearn.input_data(shape=[None, len(x_train[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(y_train[0]), activation='softmax')
    net = tflearn.regression(net, optimizer='adam',loss='categorical_crossentropy')

    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

    return model

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)

    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def classify(sentence, classes,model, words, ERROR_THRESHOLD = 0.25):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # print(results)
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

def response(return_list ,arr_tro,intents ,context ,userID='1', show_details=False):
    if return_list:
        while return_list:
            for i in intents['intents']:
                if i['tag'] == return_list[0][0]:
                    # print(return_list[0][0])
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']
                    if not 'context_set' in i or \
                        (userID in context and 'context_set' in i and i['context_set'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # return print(random.choice(i['responses']))
                        for w in arr_tro:
                            if i['tag'] == w:
                                return (random.choice(i['responses']) + w + random.choice(i['Forder']))
                            if i['tag'] == "Chủ trọ " + w:
                                return (random.choice(i['responses']) + w + random.choice(i['Forder']))
                            continue
                        return random.choice(i['responses']) + random.choice(i['Forder'])
            return_list.pop(0)

def get_files(path):
    lines = []
    with open(path, mode='r', encoding='UTF-8') as f:
        line = f.readlines()
    for i in line:
        i=i.rstrip()
        lines.append(i)
    return lines[len(lines)-1]

# print(get_files('D:\FPT_University\Spring_2023\AIP391\Demo\Account_Management\Account.txt'))

def check_validate_User_ID(path, name,mode='r'):
    pat = re.compile(r"[A-Za-z0-9]{8,12}")
    while True:
        user_id = input(name+"\n")
        try:
            if re.fullmatch(pat, user_id):
                with open(path, mode, encoding='UTF-́8') as f:
                    line = f.readlines()
                # if user_id not in line:
                #     return user_id
                user_ID = user_id+'\n'

                if user_ID not in line:
                    save_file_comunication('D:/Nam 2 FPT/chatbot proj/demo/manage_account', 'Account.txt', user_id)
                    return user_id
                else: print("User name existed! Please re-enter!")
        except:
            print("Re-enter! Please")

def save_file_comunication(path, filename, file_content, mode='a+'):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path,filename),mode,encoding='UTF-8') as f:
        f.write('%s\n'%file_content)

def chat_delay(line):
    for word in line:
        print(word, end='')
        sys.stdout.flush()
        sleep(0.1)
    print()


from function_project import *

intents = get_file('intents-_2.json')
ignore_words = ['?']

words, classes, documents = filter_data(intents,ignore_words)

x_train, y_train = prepare_training(words, classes, documents)

tf.compat.v1.reset_default_graph()

model = model_training(x_train,y_train)

model.fit(x_train, y_train, n_epoch=1000, batch_size=8, show_metric=True)
model.save('models/model.tflearn')

import pickle
pickle.dump( {'words':words, 'classes':classes, 'x_train':x_train, 'y_train':y_train}, open( "models/training_data", "wb" ) )


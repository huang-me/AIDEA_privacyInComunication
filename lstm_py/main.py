'''
checkfile: Check if the input file has been extracted
formatfile: Format the file and save into .out file
load_out: Load the .out file and return content, tag list

ps: All input should be the header of filename.
eg. train_1.txt need train_1, and word-tag file will be train_1.out
'''
# import import_ipynb
import format_data as fd

fd.checkfile('../data/train_2')
contents, tags = fd.load_out('../data/train_2')

predx = fd.loadpred('../data/development_2.txt')

import form_dict
tag2idx, idx2tag, word2idx, idx2word = form_dict.dicts(contents, tags)

import random
import numpy as np
data = []
tag_data = []
x_data = []
for content in contents:
	content_ = [word2idx[char] if char in word2idx else random.choice(list(word2idx.values())) for char in content]
	data.append(content_)
for tag in tags:
	tag_ = [tag2idx[t] for t in tag]
	tag_data.append(tag_)
for article in predx:
	article_ = [word2idx[char] if char in word2idx else random.choice(list(word2idx.values())) for char in article]
	x_data.append(article_)

pred_x = x_data

import keras
from keras.models import Sequential
from keras.models import Model
from keras.layers import Masking, Embedding, Bidirectional, LSTM, Dense, Input, TimeDistributed, Activation
from keras.preprocessing import sequence
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy, crf_accuracy
from keras import backend as K
from keras.callbacks import EarlyStopping
import tensorflow as tf

# config = tf.compat.v1.ConfigProto()
# config.gpu_options.allow_growth = True
# sess = tf.compat.v1.Session(config=config)

# CONSTANTS
EPOCHS = 100
BATCH_SIZE = 16
EMBED_DIM = 30
HIDDEN_SIZE = 16
MAX_LEN = max(max([len(x) for x in contents]), max([len(x) for x in x_data]))
VOCAB_SIZE = len(word2idx)
TAG_NUM = len(tag2idx)

train_data = sequence.pad_sequences(data, maxlen = MAX_LEN, value=VOCAB_SIZE-1, padding='post')
train_label = sequence.pad_sequences(tag_data, maxlen = MAX_LEN, value=TAG_NUM-1, padding='post')
print('train_data.shape: ', train_data)

train_label = keras.utils.to_categorical(train_label, TAG_NUM)
print(train_label.shape)

input = Input(shape=(MAX_LEN,))
model = Embedding(input_dim=VOCAB_SIZE,
				  output_dim=EMBED_DIM,
				  input_length=MAX_LEN,
				  mask_zero=True)(input)  # 20-dim embedding
model = Bidirectional(LSTM(units=50, 
					  return_sequences=True, 
					  recurrent_dropout=0.5))(model)  # variational biLSTM
model = TimeDistributed(Dense(50, activation="tanh"))(model)  # a dense layer as suggested by neuralNer
crf = CRF(TAG_NUM)	# CRF layer
out = crf(model)  # output

model = Model(input, out)
# model.compile(optimizer="rmsprop", loss=crf_loss, metrics=[crf.accuracy])
model.compile(optimizer="rmsprop", loss=crf_loss, metrics=[crf_accuracy])
model.summary()

his = model.fit(train_data, 
				train_label, 
				batch_size=BATCH_SIZE,
				epochs=EPOCHS, 
				validation_split=0.33,
				verbose=1)

model.save('model.h5')

x_pred = sequence.pad_sequences(pred_x, maxlen = MAX_LEN, padding='post', value=VOCAB_SIZE-1)

y_pred = model.predict(x_pred)

import numpy as np
def extractRes(y_pred):
	y_label = np.argmax(y_pred, axis=2)
	result = []
	for label in y_label:
		result.append([idx2tag[i] for i in label])
	return result
result = extractRes(y_pred)
print(result[0])

fd.output(predx, result)

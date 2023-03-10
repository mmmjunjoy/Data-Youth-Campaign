# -*- coding: utf-8 -*-
"""fashion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aBxBlY9Md47VAYuX0mpLIsrwXz4PeJfm
"""

##파이썬 라이브러리 로딩

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

##fashion mnist 데이터셋 텐서플로우에서 로딩

fashion_mnist = keras.datasets.fashion_mnist
(train_images,train_labels),(test_images,test_labels)=fashion_mnist.load_data()

class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shit','Sneaker','Bag','Ankle boot']

train_images.shape     ##데이터 점검
test_images.shape

##픽셀값의 범위가 0~~255 라는 것을 확인

plt.figure()
plt.imshow(train_images[3])
plt.colorbar()
plt.grid(False)
plt.show()

##Training/Test set 모두 255로 나누어 , 범위값 0~1 사이로 표준화
train_images = train_images/255.0
test_images =  test_images/255.0

##데이터 포맷 확인을 위해 , Training set에서 처음 25개 이미지 및 클래스 출력

plt.figure(figsize=(10,10))
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(train_images[i],cmap=plt.cm.binary)
  plt.xlabel(class_names[train_labels[i]])
plt.show()

##모델층 설정

#keras.layers.Flatten로 첫번째 층 생성 후 , 두개의 keras.layers.dense층에 연결

model=keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128,activation='relu'),
    keras.layers.Dense(10,activation='softmax')
    
])
model

##모델 컴파일

model.compile(optimizer='adam',
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

#모델 학습시키기

from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping()

EarlyStopping(monitor = 'val_accuracy',min_delta=0,patience = 0,mode ='auto')

model.fit(train_images,train_labels,epochs=20,batch_size=5,callbacks = [early_stopping])

##정확도 평가

test_loss,test_acc = model.evaluate(test_images,test_labels,verbose=2)

##예측실행

predictions = model.predict(test_images)
predictions[0]

np.argmax(predictions[0])

test_labels[0]

##이미지 클래스를 예측하여 그래프/신뢰도를 출력하는 함수 정의

def plot_image(i,predictions_array,true_label,img):
  predictions_array,true_label,img = predictions_array[i],true_label[i],img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img,cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'

  else:
    color ='red'

  plt.xlabel("{}{:2.0f}% ({})".format(class_names[predicted_label],100*np.max(predictions_array),class_names[true_label]),color=color)

def plot_value_array(i, predictions_array,true_label):
  predictions_array,true_label = predictions_array[i],true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10),predictions_array,color = "#777777")
  plt.ylim([0,1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color("red")
  thisplot[true_label].set_color("blue")

#올바른 예측은 파란색,잘못 예측은 빨강색
#숫자는 예측 레이블의 신뢰도 퍼센트

num_rows =5
num_cols= 3
num_images=num_rows*num_cols
plt.figure(figsize=(2*2*num_cols,2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows,2*num_cols,2*i+1)
  plot_image(i,predictions,test_labels,test_images)
  plt.subplot(num_rows,2*num_cols,2*i+2)
  plot_value_array(i,predictions,test_labels)

plt.show()

img = test_images[0]

img =(np.expand_dims(img,0))

predictions_single = model.predict(img)
plot_value_array(0,predictions_single,test_labels)
_=plt.xticks(range(10),class_names,rotation=45)


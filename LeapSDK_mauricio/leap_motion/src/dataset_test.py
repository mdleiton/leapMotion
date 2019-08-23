import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from PIL import Image
import pyautogui
import test as ts

mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()
imagen = 'screenshot1.png'
arrayimg=np.array(ts.convertirImagen(imagen))#imagen se convierte a un arreglo como estan en mnist

arrayimg_norm = np.array([tf.keras.utils.normalize(arrayimg,axis=1)]) #arreglo de la imagen entre 0 y 1, mas eficiente y rapido para el tensorflow
#plt.imshow(arrayimg)
#plt.show()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
x_test7 = np.array([x_test[84]])
#print(np.where(y_test == 8))
#print(x_test.shape)
#print(arrayimg_norm.shape)
#print(x_test7)
plt.imshow(x_test7[0],cmap=plt.cm.binary)
plt.show()
#modelo que va a entrenar

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128,activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128,activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10,activation=tf.nn.softmax))

model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

model.fit(x_train,y_train,epochs=5)
model.save('modelo_erick/modelo_test.model') #guardamos el modelo que entreno

new_model = tf.keras.models.load_model('modelo_erick/modelo_test.model') #abro mi modelo que aprendio
#load_data
val_loss, val_acc = new_model.evaluate(x_test, y_test)
#print(val_acc)

#prediction = new_model.predict(x_test7)[0] #obtengo el primer y unico elemento porque solo estoy prediciendo una imagen
prediction = new_model.predict(arrayimg_norm)[0]
print("Prediccion: %d"%np.argmax(prediction))
#print(predictions)

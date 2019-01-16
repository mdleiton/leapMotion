# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
mnist=input_data.read_data_sets('MNIST_data',one_hot=True)
import matplotlib.pyplot as plt 
import time
#print("Numero de ejemplos de entrenamiento: ",mnist.train.images.shape[0])
#print("Numero de ejemplos de validacion ",mnist.validation.images.shape[0])
#print("Numero de ejemplos de prueba: ",mnist.test.images.shape[1])
#print("sze de cada etiqueta: ",mnist.train.labels.shape[1])


def muestra_digito(x):
	plt.axis("off")
	plt.imshow(x.reshape((28,28)),cmap=plt.cm.gray)
	plt.show()
	return
def vis_imagen(i,conjunto="train"):
	if(conjunto=="train"):
		muestra_digito(mnist.train.images[i,])
		label=np.argwhere(mnist.train.labels[i])[0][0]
	elif(conjunto=="test"):
		muestra_digito(mnist.test.images[i,])
		label=np.argwhere(mnist.test.labels[i])[0][0]
	else:
		muestra_digito(mnist.validation.images[i,])
		label=np.argwhere(mnist.validation.labels[i])[0][0]
	print("Label "+ str(label))
#vis_imagen(0,"train")
#vis_imagen(132,"validation")
#vis_imagen(32,"test")
#vis_imagen(50000,"train")
#ENTRENAMIENTO

x=tf.placeholder(tf.float32,shape=[None,784])
y=tf.placeholder(tf.float32,shape=[None,10])
#capa 1
W_1=tf.Variable(tf.truncated_normal(shape=[784,512],stddev=0.2))
b_1=tf.Variable(tf.zeros([512]))

#capa 2
W_2= tf.Variable(tf.truncated_normal(shape=[512,10],stddev=0.2))
b_2=tf.Variable(tf.zeros([10]))

def NN(x):
	z_1=tf.matmul(x,W_1)+b_1
	a_1=tf.nn.relu(z_1)

	z_2=tf.matmul(a_1,W_2)+b_2
	return z_2



#COSTO

with tf.Session() as sess:
	y_=NN(x)

	
	cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = y_, labels = y))
	train_pred = tf.nn.softmax(y_)
	y_valid = NN(mnist.validation.images)
	valid_pred = tf.nn.softmax(y_valid)

	opt = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
#sess = tf.Session() #Crea una sessión
#sess.run(tf.global_variables_initializer())



def precision(predicciones, etiquetas):
    return (100.0 * np.sum(np.argmax(predicciones, 1) == np.argmax(etiquetas, 1))
          / predicciones.shape[0])






#ENTRENAMIENTO
pasos = 5000
def entrenar(sess,pasos=5000):
	import os
	sess = tf.Session() #Crea una sessión
	sess.run(tf.global_variables_initializer())
	path="modelo"
	modelo=path+r"/"+"red_numeros"
	saver=tf.train.Saver()		
	print("Entrenamiento:")
	for i in range(pasos):
   		 batch = mnist.train.next_batch(100)
		 _,costo,predicciones =  sess.run([opt, cross_entropy, train_pred],  feed_dict={x: batch[0], y: batch[1]})
    
   		 if (i % 500 == 0):
      		 	print("Costo del minibatch hasta el paso %d: %f" % (i, costo))
      		 	print("Precisión en el conjunto de entrenamiento: %.1f%%" % precision(predicciones, batch[1]))
       		 	print("Precision en el conjunto de validación: %.1f%%" % precision(
       		 	valid_pred.eval(session=sess), mnist.validation.labels))
   		 if (i%100==0):
			if not os.path.isdir(path):
 				os.mkdir(path)
	
			saver.save(sess,save_path=modelo,global_step=i)


with tf.Session() as sess:
	entrenar(sess,pasos=5000)

#y_test = NN(mnist.test.images)
#test_prediction = tf.nn.softmax(y_test)
#print("Precisión en el conjunto de PRUEBA: %.1f%%" % precision(test_prediction.eval(session = sess), mnist.test.labels))



#indice = 251
#p = tf.argmax(NN(mnist.test.images[indice:indice+1]).eval(session = sess),1)
#print("Predicción:", sess.run(p)[0])
#vis_imagen(indice, conjunto="test")


def remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency 
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL 
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format

        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im



from PIL import Image
def adivinar(sess,imagen):
	#imagen = "numero8.png"
	img = Image.open(imagen)
	img = remove_transparency(img).convert('L')
	sess = tf.Session() #Crea una sessión
	sess.run(tf.global_variables_initializer())
	if  img.size != (28,28):
	    
	    img.thumbnail((28,28), Image.ANTIALIAS)
	print(img.size)
	entrada = np.array(img, dtype = np.float32)
	entrada = entrada.reshape((1,784))
	entrada = entrada/255.0
        
	p = tf.argmax(NN(entrada).eval(session = sess),1)
	print("Imágen:{}".format(imagen))
	#img.show()
	print(sess.run(p))
	#print("Predicción:", sess.run(p)[0])
	return sess.run(p)[0]
#imagen="numero8.png"

#adivinar(imagen)





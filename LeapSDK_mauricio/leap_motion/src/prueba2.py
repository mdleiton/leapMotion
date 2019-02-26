from mlxtend.data import loadlocal_mnist
import numpy as np
train_images, train_labels = loadlocal_mnist(
        images_path='/home/karina/Documentos/dataset/MNIST_data/train-images.idx3-ubyte', 
        labels_path='/home/karina/Documentos/dataset/MNIST_data/train-labels.idx1-ubyte')

test_images,test_labels=loadlocal_mnist(
        images_path='/home/karina/Documentos/dataset/MNIST_data/t10k-images.idx3-ubyte', 
        labels_path='/home/karina/Documentos/dataset/MNIST_data/t10k-labels.idx1-ubyte')

def getTrain():
	tr=train_images.astype('float32')
	lbl=crearArray(train_labels)
	return tr,lbl

def getTest():
	ts=test_images.astype('float32')
	lbl=crearArray(test_labels)
	return ts,lbl
#print(train_images[0:10].shape)
#print(getTrain()[1][:10])
def crearArray(arraynumero):
	arreglo= np.zeros((len(arraynumero),10),dtype='float32')
	i=0
	for pos in arraynumero:
		arreglo[i,pos]=1
		i+=1
	return arreglo
print(crearArray(train_labels)[0])

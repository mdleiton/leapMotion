# -*- coding: utf-8 -*-
import os, sys, inspect, thread, time

import pyautogui
import tensorflow as tf
from PIL import Image
import numpy as np
import tkSimpleDialog as sp


src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))

from Tkinter import Frame, Canvas, YES, BOTH,Button,TOP,BOTTOM,LEFT,RIGHT
import tkMessageBox
#import numeros as num
import Leap
from time import sleep
import test as ts
import matplotlib.pyplot as plt

import dataset_test as dt



"""
Cambios:
-numeros.py:144 -> antes el reshape se lo hacia de (1,784), ahora es de (1,756)
-prediccion_erick.py -> size_height cambio de 760 a 740
"""



on_prediction = False

i = 0
size_width=760
size_height=760

class TouchPointListener(Leap.Listener):

    def on_init(self, controller):
        print("Inicializado.")

    def on_connect(self, controller):
        print("Conectado.")

    def on_frame(self, controller):
        #self.paintCanvas.delete("all")
        global i, on_prediction
        frame = controller.frame()
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                self.paintCanvas.delete("all")
                sleep(2)

        interactionBox = frame.interaction_box
        if on_prediction:
            return
        for hand in frame.hands:
            for finger in hand.fingers:
                if finger.type == 1:
                    normalizedPosition = interactionBox.normalize_point(finger.tip_position)
                    if hand.is_right:
                        """if(finger.touch_distance > 0 and finger.touch_zone != Leap.Pointable.ZONE_NONE):
                            color = self.rgb_to_hex((0, 255 - 255 * finger.touch_distance, 0))
                        elif(finger.touch_distance <= 0):
                            color = self.rgb_to_hex((-255 * finger.touch_distance, 0, 0))
                        else:
                            color = self.rgb_to_hex((0,0,200))"""
                        if(finger.touch_distance <= 0.55 and finger.touch_zone != Leap.Pointable.ZONE_NONE):
                            self.draw(normalizedPosition.x * 500, 500 - normalizedPosition.y * 500, 20, 20, "black")
                    else:
                        self.draw(normalizedPosition.x * 500, 500 - normalizedPosition.y * 500, 20, 20, "white")


    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval( x-width, y-height,x+width , y+height, fill = color, outline = "")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas

    def rgb_to_hex(self, rgb):
       # return '#%02x%02x%02x' % rgb
       return '#%02x%02x%02x' % (0,0,0)


    def limpiar(self):
        self.paintCanvas.delete("all")



        #Capturar Canvas y guardarlo a un png
    def capturar(self):
        self.paintCanvas.postscript(file='canvas_im.eps')
        img = Image.open("canvas_im.eps")
        #img = img.crop((50,50,400,400))
        img.save("screenshot1.png","png")
        os.remove("canvas_im.eps")
        global on_prediction
        #on_prediction = True
        imagen="screenshot1.png"

        """LA PREDICCION AUN NO ESTA IMPLEMENTADA PARA EL LEAP MOTION"""
        """with tf.Session() as sess:
            numero=num.adivinar(sess,imagen)"""
        numero = dt.adivinar_erick(imagen)
        mensaje="Su numero es %d "%numero
        result = tkMessageBox.askyesno("Número",mensaje + "Es correcto?")
        if not result:
            numero=sp.askinteger('Ingreso número', 'Ingrese el número')
            arrayimg=np.array([ts.convertirImagen(imagen)])
            dt.reentrenar(arrayimg,np.array([numero]))
        #plt.imshow(arrayimg,cmap=plt.cm.binary)
        #plt.show()
        #arraylbl=np.zeros((10,1),dtype="float32")#se hace el arreglo del label asi como estan los labels en mnist data
        #arraylbl[numero]=1
        #on_prediction = False

class PaintBox(Frame):

    def __init__( self ):
        Frame.__init__( self )
        self.place(x=0,y=0)
        self.leap = Leap.Controller()
        self.painter = TouchPointListener()

        self.botonLimpiar=Button(self,text="Limpiar",fg="white",bg="red",command=self.painter.limpiar)
        self.botonLimpiar.pack(side=TOP)

        self.botonCapturar=Button(self,text="Identificar Numero",fg="blue",bg="white",command=self.painter.capturar)
        self.botonCapturar.pack(side=TOP)

        self.leap.add_listener(self.painter)
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "Prueba 1" )
        self.master.geometry( "500x500+0+0" )


        self.leap.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        self.leap.config.set("Gesture.Swipe.MinLength", 100.0)
        self.leap.config.set("Gesture.Swipe.MinVelocity", 750)
        self.leap.config.save()

        self.paintCanvas = Canvas( self, width = "500", height = "500" ,bg="white")

        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)


def main():
    PaintBox().mainloop()

if __name__ == "__main__":
    main()

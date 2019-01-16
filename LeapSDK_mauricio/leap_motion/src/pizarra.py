# -*- coding: utf-8 -*-
import os, sys, inspect, thread, time

import pyautogui
import tensorflow as tf
from PIL import Image
import numpy as np


src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))

from Tkinter import Frame, Canvas, YES, BOTH,Button,TOP,BOTTOM,LEFT,RIGHT
import tkMessageBox 
import numeros as num
import Leap
from time import sleep



#IMPORTANDO EL MODELO
#path = "modelo"
#modelo = path + r"/" + "red_numeros"

#saver = tf.train.Saver()

#with tf.Session() as sess:
    
    
    #Carga el modelo.
 #   print('Cargando el modelo ...')
 #   ckpts = tf.train.get_checkpoint_state(path)
  #  print(ckpts)
 #  print("Ruta del último Checkpoint ", ckpts.model_checkpoint_path)
    
    #Utiliza el último modelo guardado
  #  saver.restore(sess,save_path = ckpts.model_checkpoint_path)





i = 0
size_width=700
size_height=700

class TouchPointListener(Leap.Listener):
    
    def on_init(self, controller):
        print("Inicializado.")

    def on_connect(self, controller):
        print("Conectado.")

    def on_frame(self, controller):
        #self.paintCanvas.delete("all")
        
        frame = controller.frame()
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                global i
                swipe = Leap.SwipeGesture(gesture)
                self.paintCanvas.delete("all")
                sleep(2)
        
        interactionBox = frame.interaction_box

        for hand in frame.hands:
            for finger in hand.fingers:
                if finger.type == 1:
                    normalizedPosition = interactionBox.normalize_point(finger.tip_position)
                    if hand.is_right:
                        if(finger.touch_distance > 0 and finger.touch_zone != Leap.Pointable.ZONE_NONE):
                            color = self.rgb_to_hex((0, 255 - 255 * finger.touch_distance, 0))            
                        elif(finger.touch_distance <= 0):
                            color = self.rgb_to_hex((-255 * finger.touch_distance, 0, 0))                
                        else:
                            color = self.rgb_to_hex((0,0,200))
                        self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 15, 15, color)
                    else:
                        self.draw(normalizedPosition.x * 800, 600 - normalizedPosition.y * 600, 15, 15, "white")


    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval( x, y, x + width, y + height, fill = color, outline = "")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas
        
    def rgb_to_hex(self, rgb):
       # return '#%02x%02x%02x' % rgb
	return '#%02x%02x%02x' % (0,0,0)


    def limpiar(self):
        self.paintCanvas.delete("all")

    


    def capturar(self):
       screenshot=pyautogui.screenshot(region=(70,70,size_width,size_height))
       screenshot.save("screenshort.png")
       imagen="screenshort.png"
       
       with tf.Session() as sess:
            numero=num.adivinar(sess,imagen)
       mensaje="Su numero es %d"%(numero)
       tkMessageBox.showinfo(message=mensaje, title="Numero")

    

    


class PaintBox(Frame):

    def __init__( self ):
        Frame.__init__( self )
	self.place(x=0,y=0)
        self.leap = Leap.Controller()
        self.painter = TouchPointListener()

        self.botonLimpiar=Button(self,text="Limpiar",fg="white",bg="red",command=self.painter.limpiar)
        self.botonLimpiar.pack(side=TOP)

        self.botonCapturar=Button(self,text="Identificar Numero",fg="blue",bg="white",command=self.painter.capturar)
        self.botonCapturar.pack(side=RIGHT)

        self.leap.add_listener(self.painter)
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "Prueba 1" )
        self.master.geometry( "800x800+0+0" )
	
      	
        self.leap.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        self.leap.config.set("Gesture.Swipe.MinLength", 100.0)
        self.leap.config.set("Gesture.Swipe.MinVelocity", 750)
        self.leap.config.save()

        self.paintCanvas = Canvas( self, width = "800", height = "800" ,bg="white")
	
        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)
       

def main():
    PaintBox().mainloop()

if __name__ == "__main__":
    main()


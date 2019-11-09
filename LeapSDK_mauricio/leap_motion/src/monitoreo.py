# -*- coding: utf-8 -*-
import os, sys, inspect, time

from PIL import Image
import numpy as np
import tkSimpleDialog as sp
import matplotlib.pyplot as plt
from Tkinter import Frame, Canvas, YES, BOTH, Button, TOP, BOTTOM, LEFT, RIGHT
import tkMessageBox
import csv

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))
import Leap

onSave = False
writerFile = None
counter = 0

class TouchPointListener(Leap.Listener):

    def on_init(self, controller):
        print("Inicializado.")

    def on_exit(self, controller):
        global writerFile
        writerFile.close()
        print("Finalizado correctamente.")

    def on_disconnect(self, controller):
        print("Desconectado.")

    def on_connect(self, controller):
        print("Conectado.")

    def on_frame(self, controller):
        global writerFile, onSave, counter
        counter = counter + 1
        if counter > 360:
            counter = 0
            self.limpiar()
        if onSave:
            frame = controller.frame()
            for gesture in frame.gestures():
                if gesture.type is Leap.Gesture.TYPE_SWIPE:
                    swipe = Leap.SwipeGesture(gesture)
                    self.limpiar()
                    time.sleep(2)
            interactionBox = frame.interaction_box
            
            for hand in frame.hands:
                for finger in hand.fingers:
                    if finger.type == 1:
                        normalizedPosition = interactionBox.normalize_point(finger.tip_position)
                        if hand.is_right:
                            if finger.touch_distance <= 0.55 and finger.touch_zone != Leap.Pointable.ZONE_NONE and finger.type != 2:
                                self.draw(normalizedPosition.x * 500, 500 - normalizedPosition.y * 500, 15, 15, "black")
                        else:
                            self.draw(normalizedPosition.x * 500, 500 - normalizedPosition.y * 500, 15, 15, "white")
                        writerFile.write(str(time.time()) + "," + 
                                         str(finger.touch_distance) + "," + 
                                         str(finger.touch_zone) + "," + 
                                         str(finger.tip_velocity) + "," + 
                                         str(finger.tip_position) + "\n")

    def draw(self, x, y, width, height, color):
        self.paintCanvas.create_oval(x - width, y - height, x + width, y + height, fill=color, outline="")

    def set_canvas(self, canvas):
        self.paintCanvas = canvas

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % (0, 0, 0)

    def limpiar(self):
        """ Cuando se da clic en el botón limpiar se borran
         todo los que se encuentre en el canvas. """
        self.paintCanvas.delete("all")
        self.circulo(250, 230, 150)

    def iniciarMonitoreo(self):
        """ solicita un nombre para el csv e iniciar a capturar los datos"""
        nombre = sp.askstring('Experimento', 'Por favor ingreso nombre de prueba.')
        global writerFile, onSave
        if nombre is not None:
            writerFile = open(nombre + ".csv","w+")      
            onSave = True

    def guardarImagen(self):
        """ Capturar el actual canvas y contenido para guardarlo a un png"""
        self.paintCanvas.postscript(file='canvas_im.eps')
        img = Image.open("canvas_im.eps")
        img.save("screenshot1.png","png")
        os.remove("canvas_im.eps")

    def circulo(self, x, y, radio):
        """  Crea un circulo con centro en x, y. Y de radio r. """
        x0 = x - radio
        y0 = y - radio
        x1 = x + radio
        y1 = y + radio
        return self.paintCanvas.create_oval(x0, y0, x1, y1)

class PaintBox(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.place(x=0, y=0)
        self.leap = Leap.Controller()
        self.painter = TouchPointListener()

        self.botonLimpiar = Button(self, text="Limpiar", fg="white",
                                   bg="red", command=self.painter.limpiar)
        self.botonLimpiar.pack(side=TOP)

        self.botonCapturar = Button(self, text="Iniciar", fg="blue",
                                    bg="white",
                                    command=self.painter.iniciarMonitoreo)
        self.botonCapturar.pack(side=TOP)

        self.leap.add_listener(self.painter)
        self.pack(expand=YES, fill=BOTH)
        self.master.title("MIC")
        self.master.geometry("500x500+0+0")

        self.leap.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        self.leap.config.set("Gesture.Swipe.MinLength", 100.0)
        self.leap.config.set("Gesture.Swipe.MinVelocity", 750)
        self.leap.config.save()

        self.paintCanvas = Canvas(self, width="500", height="500", bg="white")

        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)
        self.painter.circulo(250, 230, 150)


def main():
    PaintBox().mainloop()

if __name__ == "__main__":
    main()

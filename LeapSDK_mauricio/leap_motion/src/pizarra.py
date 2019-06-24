import os, sys, inspect, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, lib_dir)))
import Leap
from Tkinter import Frame, Canvas, YES, BOTH,Button,TOP

from time import sleep

i = 0

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
        return '#%02x%02x%02x' % rgb

    def limpiar(self):
        self.paintCanvas.delete("all")

class PaintBox(Frame):

    def __init__( self ):
        Frame.__init__( self )
        self.leap = Leap.Controller()
        self.painter = TouchPointListener()

        self.botonLimpiar=Button(self,text="Limpiar",fg="blue",command=self.painter.limpiar)
        self.botonLimpiar.pack(side=TOP)

        self.leap.add_listener(self.painter)
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "Prueba 1" )
        self.master.geometry( "800x600" )
      	
        self.leap.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        self.leap.config.set("Gesture.Swipe.MinLength", 100.0)
        self.leap.config.set("Gesture.Swipe.MinVelocity", 750)
        self.leap.config.save()

        self.paintCanvas = Canvas( self, width = "800", height = "600" ,bg="white")
        self.paintCanvas.pack()
        self.painter.set_canvas(self.paintCanvas)
       

def main():
    PaintBox().mainloop()

if __name__ == "__main__":
    main()

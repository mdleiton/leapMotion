# -*- coding: utf-8 -*-
import Leap, sys, math
from Leap import SwipeGesture

class LeapMotionListener(Leap.Listener):

    
    def on_connect(self, controller):
        print "Motion Sensor Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor disconnect"

    def on_exit(self, controller):
        print "Exited"
    
    def on_frame(self, controller):
        frame = controller.frame()

        for gesture in frame.gestures():

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                swipeDirection = swipe.direction
                if (swipeDirection.x > 0 and math.fabs(swipeDirection.x) > math.fabs(swipeDirection.y)):
                    print "Swiped right"
                elif (swipeDirection.x < 0 and math.fabs(swipeDirection.x) > math.fabs(swipeDirection.y)):
                    print "Swiped left"
                elif (swipeDirection.y > 0 and math.fabs(swipeDirection.x) < math.fabs(swipeDirection.y)):
                    print "Swiped up"
                elif (swipeDirection.y < 0 and math.fabs(swipeDirection.x) < math.fabs(swipeDirection.y)):
                    print "Swiped down"

def main():
    listener  = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press enter to quit"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
    

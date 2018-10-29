import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    bone_names = ["Metacarpal", "Proximal", "Intermediate", "Distal"]
    state_names = ["STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"]

    def on_init(self, controller):
        print "Initialized"
    
    def on_connect(self, controller):
        print "Motion Sensor Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor disconnect"

    def on_exit(self, controller):
        print "Exited"
    
    def on_frame(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            handType = "Left" if hand.is_left else "Right"

            print  handType + " Hand ID "+ str(hand.id) + " Palm Position" + str(hand.palm_position)

            normal = hand.palm_normal #vector normal a la palma

            direction = hand.direction #vector direction 

            print "Pitch: "  + str(direction.pitch + Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll + Leap.RAD_TO_DEG) + "Yaw: " + str(direction.yaw + normal.roll + Leap.RAD_TO_DEG)

            


            # each hand has its id, and change if you go far away with it
            # palm position has its own coordinates : x -> right , left : y -> up, down, z -> depth
            #pitch : rotation around X axis , roll: rotation around Z axis, yaw: rotation around Y axis

            

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
    

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class LedSet(Node):
    def __init__(self):
        super().__init__("led_set")

        self.LPub = self.create_publisher(Bool,"/led/left", 10)
        self.RPub = self.create_publisher(Bool,"/led/right", 10)

    def ledSet(self, left, right):
        
        if left is True: 
            lmsg = True
        else: 
            lmsg = False 
            
        if right is True: 
            rmsg = True
        else: 
            rmsg = False 

        self.LPub.publish(lmsg)
        self.RPub.publish(rmsg)

#end me

#is this working?

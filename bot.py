import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Wander(Node):
    def __init__(self):
        super().__init__("left_wall_follower")
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.sub = self.create_subscription(LaserScan, "scan", self.lasercallback, 10)
        self.create_timer(0.1, self.bot)
        self.minangle = 0.0
        self.maxrange = 0.0
        self.minrange = 0.0
        self.deltaangle = 0.0
        self.laserdata = 0.0
        self.get_logger().info('KillBot node has been created.')

    def lasercallback(self, data):
        self.minangle = data.angle_min
        self.maxangle = data.angle_max
        self.deltaangle = data.angle_increment
        self.maxrange = data.range_max
        self.laserdata = data.ranges
        self.lastFront = 0.0
        self.lastBack = 0.0
        self.lastRight = 0.0
        self.lastLeft = 0.0
        #for i in range(len(self.laserdata)):
        #    if math.isinf(self.laserdata[i]):
        #        self.laserdata[i] = self.maxrange        

        # Initialize an empty list to collect laser data
        all_laser_data = []
        cnt = 0
        while math.isinf(self.laserdata[cnt]):
            cnt += 1
        temp = 0
        if self.laserdata[cnt] > self.maxrange / 2:
            temp = self.maxrange
        else:
            temp = self.minrange
        
        cnt2 = 0
        while cnt2 < cnt:
            self.laserdata[cnt2] = temp
        
        for i in range(len(self.laserdata)):
            if math.isinf(self.laserdata[i]):
            	if self.all_laser_data[i-1] > self.maxrange / 2:
            		all_laser_data.append(self.maxrange)
            	else:
            		all_laser_data.append(0)
            all_laser_data.append(self.laserdata[i])

 
        angles_of_interest = [0, 90, 180, 270]
        last_angles = [self.lastFront, self.lastBack, self.lastRight, self.lastLeft]
        for angle in angles_of_interest:
            index = self.angletoindex(math.floor(angle * math.pi / 180))
            
            #if all_laser_data[index]:
            self.get_logger().info(str(angle) + "= " + str(all_laser_data[index]))
            

    def bot(self):
        # Print laser data values at specific angles
        pass

    def angletoindex(self, angle):
        if self.deltaangle != 0:
            index = math.floor((angle - self.minangle) / self.deltaangle)
            return max(0, min(index, len(self.laserdata) - 1))
        return 0

    def indextoangle(self, index):
        return (index * self.deltaangle) + self.minangle

def main(args=None):
    rclpy.init(args=args)
    killbot = Wander()
    rclpy.spin(killbot)
    killbot.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

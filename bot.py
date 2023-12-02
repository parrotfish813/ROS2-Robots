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
        self.saniLaser = []
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

        # Initialize an empty list to collect laser data
        self.saniLaser = []

        # Handle the case where self.laserdata has zero length
        if len(self.laserdata) > 0:
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
                cnt2 += 1
            
            for i in range(1, len(self.laserdata)):
                if math.isinf(self.laserdata[i -1]):
                    if self.laserdata[i-1] >= self.maxrange / 2:
                        self.saniLaser.append(self.maxrange)
                    elif self.laserdata[i-1] < self.maxrange / 2:
                        self.saniLaser.append(self.minrange)
                else:import rclpy
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
        self.sani_laser_data = []
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

        # Initialize an empty list to collect laser data
        self.sani_laser_data = []

        # Handle the case where self.laserdata has zero length
        if len(self.laserdata) > 0:
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
                cnt2 += 1
            
            for i in range(len(self.laserdata) ):
                if math.isinf(self.laserdata[i]):
                    if self.laserdata[i - 1] >= self.maxrange / 2:
                        self.sani_laser_data.append(self.maxrange)
                    elif self.laserdata[i - 1] < self.maxrange / 2:
                        self.sani_laser_data.append(self.minrange)
                else:
                     self.sani_laser_data.append(self.laserdata[i])

        angles_of_interest = [0, 90, 180, 270]
        index = self.angletoindex(math.floor(90 * math.pi / 180))
        self.get_logger().info(str(90) + ", index: " + str(index) + "= " + str(self.sani_laser_data[index]))

    def bot(self):
        # Print laser data values at specific angles
        # print("Bot method called")
        pass

    def angletoindex(self, angle):
        if self.deltaangle != 0:
            index = math.floor((angle - self.minangle) / self.deltaangle)
            return index
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
                    self.saniLaser.append(self.laserdata[i])

        angles_of_interest = [0, 90, 180, 270]
        index = self.angletoindex(math.floor(90 * math.pi / 180))
        self.get_logger().info(str(90) + ", index: " + str(index) + "= " + str(self.saniLaser[index]))

    def bot(self):
        # Print laser data values at specific angles
        # print("Bot method called")
        pass

    def angletoindex(self, angle):
        if self.deltaangle != 0:
            index = math.floor((angle - self.minangle) / self.deltaangle)
            return index
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

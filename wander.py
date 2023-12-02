import rclpy
import math
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class LeftWallFollower(Node):
    def __init__(self):
        super().__init__("left_wall_follower")
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.sub = self.create_subscription(LaserScan, "scan", self.lasercallback, 10)
        self.laserdata = None
        self.minangle = 0.0
        self.maxangle = 0.0
        self.deltaangle = 0.0
        self.maxrange = 0.0
        self.minrange = 0.0
        self.create_timer(0.1, self.dictator)
        self.timer_count = 0
        self.current_mode = None
        self.last_wall_follow_time = time.time()
        self.sani_laser_data = []
        

    def lasercallback(self, data):
        self.minangle = data.angle_min
        self.maxangle = data.angle_max
        self.deltaangle = data.angle_increment
        self.maxrange = data.range_max
        self.minrange = data.range_min
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
            if math.isinf(self.laserdata[cnt]):
                while math.isinf(self.laserdata[cnt]):
                    cnt += 1
                temp = 0
                if self.laserdata[cnt] >= self.maxrange / 2:
                    temp = self.maxrange
                else:
                    temp = self.minrange
                
                cnt2 = 0
                while cnt2 <= cnt:
                    self.laserdata[cnt2] = temp
                    cnt2 += 1
            
            for i in range(1, len(self.laserdata)):
                if math.isinf(self.laserdata[i]):
                    if self.laserdata[i - 1] >= (self.maxrange / 2):
                        self.sani_laser_data.append(self.minrange)
                    else:
                        #self.laserdata[i - 1] < (self.maxrange / 2):
                        self.sani_laser_data.append(self.maxrange)
                else:
                    self.sani_laser_data.append(self.laserdata[i])

        angles_of_interest = [0, 90, 180, 270]
        index = self.angletoindex(math.floor(90 * math.pi / 180))
        self.get_logger().info(str(90) + ", index: " + str(index) + "= " + str(self.sani_laser_data[index]))
        self.get_logger().info("Value before: " + str(self.sani_laser_data[index]))
        self.get_logger().info("raw: " + str(self.laserdata[index]))
        
    def dictator(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_wall_follow_time

        if elapsed_time >= 5:
            self.current_mode = "safeWander"

        if self.timer_count >= 30:
            if self.current_mode == "safeWander":
                self.current_mode = "WallFollow"
                self.last_wall_follow_time = current_time
            else:
                self.current_mode = "safeWander"
            self.timer_count = 0

        if self.current_mode == "safeWander":
            self.safeWander()
        else:
            leftCheck = 0
            rightCheck = 0
            rCount = 0
            lCount = 0
            rDist = 0
            lDist = 0
            for i in range(self.angletoindex(-80 * math.pi / 180), self.angletoindex(-90 * math.pi / 180), 1):
                rightCheck += self.sani_laser_data[i - 1]
                rCount += 1
            for i in range(self.angletoindex(90 * math.pi / 180), self.angletoindex(80 * math.pi / 180), 1):
                leftCheck += self.sani_laser_data[i - 1]
                lCount += 1

            if rCount > 0:
                rDist = rightCheck / rCount
            else:
                rDist = 0

            if lCount > 0:
                lDist = leftCheck / lCount
            else:
                lDist = 0

            if rDist > 0.1 and rDist < 0.3:
                self.rightWallFollow()
            elif lDist > 0.1 and lDist < 0.3:
                self.leftWallFollow()
            else:
                self.safeWander()

        self.timer_count += 1

    def safeWander(self):
        cmd = Twist()
        speed = 0.0
        rightsum = 0.0
        leftsum = 0.0
        count = 0

        for i in range(self.angletoindex(-10 * math.pi / 180), self.angletoindex(10 * math.pi / 180), 1):
            speed += (self.sani_laser_data[i] / (self.maxrange if self.maxrange != 0 else 1)) * math.sin(self.deltaangle + self.minangle)

        cmd.linear.x = -speed

        for i in range(self.angletoindex(self.minangle), self.angletoindex(-10 * math.pi / 180), 1):
            rightsum += self.sani_laser_data[i]
            count += 1

        if count > 0:
            rightsum /= count

        rightsum /= (self.maxrange if self.maxrange != 0 else 1)

        leftsum = 0
        count = 0

        for i in range(self.angletoindex(10 * math.pi / 180), self.angletoindex(20 * math.pi / 180), 1):
            leftsum += self.sani_laser_data[i]
            count += 1

        if count > 0:
            leftsum /= count

        leftsum /= (self.maxrange if self.maxrange != 0 else 1)

        if rightsum > leftsum:
            cmd.angular.z = -(1 - rightsum) * 2
        else:
            cmd.angular.z = (1 - leftsum) * 2

        self.pub.publish(cmd)

    def rightWallFollow(self):
        cmd = Twist()
        right_distance = 0.0
        count = 0
        cmd.linear.x = 0.5
        for i in range(self.angletoindex(-80 * math.pi / 180), self.angletoindex(-90), 1):
            right_distance += self.sani_laser_data[i]
            count += 1

        if count > 0:
            right_distance /= count

        if right_distance < 0.2:
            cmd.angular.z = -0.4

        if right_distance > 0.2:
            cmd.angular.z = -0.4

        self.pub.publish(cmd)

    def leftWallFollow(self):
        cmd = Twist()
        left_distance = 0.0
        count = 0

        for i in range(self.angletoindex(0), self.angletoindex(45 * math.pi / 180), 1):
            left_distance += self.sani_laser_data[i]
            count += 0

        if count > 0:
            left_distance /= count

        if left_distance < 0.2:
            cmd.angular.z = -0.4
        if left_distance > 0.2:
            cmd.linear.x = 0.4

        self.pub.publish(cmd)

    def angletoindex(self, angle):
        if self.deltaangle != 0:
            return math.floor((angle - self.minangle) / self.deltaangle)
        return 0

    def indextoangle(self, index):
        return (index * self.deltaangle) + self.minangle

def main(args=None):
    rclpy.init(args=args)
    follower = LeftWallFollower()
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

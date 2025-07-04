#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
import math

class TurtleBot3:
    def __init__(self):
        rospy.init_node('turtlebot3_linear_controller', anonymous=True)
      
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.update_position)
        
        self.current_position = Point()
        self.rate = rospy.Rate(10) 
        self.distance_tolerance = 0.1  
        
    def update_position(self, odom_msg):
        self.current_position = odom_msg.pose.pose.position
        
    def get_distance_to_target(self, target_point):
        dx = target_point.x - self.current_position.x
        dy = target_point.y - self.current_position.y
        return math.sqrt(dx**2 + dy**2)
    
    def move_to_point(self, target_point):
        velocity_msg = Twist()
        
        rospy.loginfo("Hedef noktaya hareket ediliyor: x=%.2f, y=%.2f", target_point.x, target_point.y)
        
        while not rospy.is_shutdown():
            distance = self.get_distance_to_target(target_point)
            
            if distance > self.distance_tolerance:
                
                linear_speed = 0.3 * distance 
            
                linear_speed = min(linear_speed, 0.22)  
                
                velocity_msg.linear.x = linear_speed
                velocity_msg.angular.z = 0.0  
                
                rospy.loginfo_throttle(1, "Mesafe: %.2f m, Hız: %.2f m/s", distance, linear_speed)
                
            else:
               
                velocity_msg.linear.x = 0.0
                velocity_msg.angular.z = 0.0
                rospy.loginfo("Hedef noktaya ulaşıldı!")
                break
        
            self.velocity_publisher.publish(velocity_msg)
            self.rate.sleep()
      
        velocity_msg.linear.x = 0.0
        velocity_msg.angular.z = 0.0
        self.velocity_publisher.publish(velocity_msg)

if __name__ == '__main__':
    try:
        controller = TurtleBot3()
        rospy.sleep(1)
        
        target = Point()
        target.x = 2.0  
        target.y = 1.5  
        target.z = 0.0
        
        controller.move_to_point(target)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("Program kullanıcı tarafından durduruldu")
    except Exception as e:
        rospy.logerr("Hata oluştu: %s", str(e))
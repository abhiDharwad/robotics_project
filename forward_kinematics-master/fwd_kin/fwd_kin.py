import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

class RobotKinematics:
    def __init__(self):
        self.theta1, self.theta2, self.theta3, self.theta4 = sp.symbols('theta1 theta2 theta3 theta4')
        
        # DH parameters: [a, alpha, d, theta]
        self.dh_params = [
            [0, np.deg2rad(90), 0, self.theta1],
            [1, np.deg2rad(-90), 0, self.theta2],
            [1, np.deg2rad(90), 0, self.theta3],
            [1, np.deg2rad(-90), 0, self.theta4],
            [1, np.deg2rad(0), 0, 0]  # End effector
        ]
        
    def dh_matrix(self, a, alpha, d, theta):
     
        return sp.Matrix([
            [sp.cos(theta), -sp.sin(theta)*sp.cos(alpha), sp.sin(theta)*sp.sin(alpha), a*sp.cos(theta)],
            [sp.sin(theta), sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha), a*sp.sin(theta)],
            [0, sp.sin(alpha), sp.cos(alpha), d],
            [0, 0, 0, 1]
        ])
    
    def forward_kinematics(self, joint_angles_deg):
       
        # Convert to radians
        theta_values_rad = [np.deg2rad(t) for t in joint_angles_deg]
        
        # Create substitution dictionary
        subs_dict = {
            self.theta1: theta_values_rad[0],
            self.theta2: theta_values_rad[1], 
            self.theta3: theta_values_rad[2],
            self.theta4: theta_values_rad[3]
        }
        
        # Compute transformation matrices
        T = sp.eye(4)
        transformations = []
        
        for i, (a, alpha, d, theta) in enumerate(self.dh_params):
            T_i = self.dh_matrix(a, alpha, d, theta)
            T = T * T_i
            transformations.append(T.evalf(subs=subs_dict))
        
        return transformations[-1]  
    
    def rotation_to_rpy(self, R):
        
        R = np.array(R, dtype=float)
        
        # Extract matrix elements
        r11, r12, r13 = R[0, 0], R[0, 1], R[0, 2]
        r21, r22, r23 = R[1, 0], R[1, 1], R[1, 2]
        r31, r32, r33 = R[2, 0], R[2, 1], R[2, 2]
        
        # Calculate RPY angles
        pitch = np.arctan2(-r31, np.sqrt(r11**2 + r21**2))
        yaw = np.arctan2(r21, r11)
        roll = np.arctan2(r32, r33)
        
        return np.rad2deg([roll, pitch, yaw])

def vizulization(x_pos, y_pos, z_pos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = x_pos
    y = y_pos
    z = z_pos
    ax.scatter(x, y, z, color='red', s=100)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.show()


if __name__ == "__main__":
    robot = RobotKinematics()
    
    # Get joint angles from user
    theta_values_deg = []
    for i in range(1, 5):
        angle = float(input(f"Angle of joint {i} in deg = "))
        theta_values_deg.append(angle)
    
    # Calculate forward kinematics
    T_final = robot.forward_kinematics(theta_values_deg)
    
    # Extract position and orientation
    R = T_final[:3, :3]
    P = T_final[:3, 3]
    roll, pitch, yaw = robot.rotation_to_rpy(R)
    

    print("FORWARD KINEMATICS RESULTS\n")
    print(f"Input joint angles (deg): {theta_values_deg}")
    print(f"\nEnd Effector Position:")
    print(f"  X: {float(P[0]):.4f} units")
    print(f"  Y: {float(P[1]):.4f} units") 
    print(f"  Z: {float(P[2]):.4f} units")
    print(f"\nEnd Effector Orientation (RPY):")
    print(f"  Roll:  {roll:.3f}°")
    print(f"  Pitch: {pitch:.3f}°")
    print(f"  Yaw:   {yaw:.3f}°")

    vizulization(P[0], P[1], P[2])

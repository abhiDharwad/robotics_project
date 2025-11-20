from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def user_input():
    print("Select the conversion you want")
    ip = int(input("1. euler to quaternion\n2. quaternion to euler\n\nChoice: "))

    if ip == 1:
        eular_angles = []
        for axis in ['X', 'Y', 'Z']:
            val = float(input(f"Enter {axis} angle (degrees): "))
            eular_angles.append(val)
        
        # Ask for euler sequence and convention
        print("\nRotation Convention:")
        print("1. Intrinsic (rotating axes) - lowercase 'xyz'")
        print("2. Extrinsic (fixed axes) - uppercase 'XYZ'")
        conv = input("Choose convention (1 or 2): ")
        
        print("\nEnter Euler sequence (xyz, zyx, etc.):")
        seq = input("Sequence: ").lower()
        
        if conv == '2':
            seq = seq.upper()  # Uppercase for extrinsic
        
        convert_eular_quat(eular_angles, seq, degrees=True)
        
    elif ip == 2:
        quat_angles = []
        print("\nEnter Quaternion components (x, y, z, w):")
        for comp in ['x', 'y', 'z', 'w']:
            val = float(input(f"Enter {comp}: "))
            quat_angles.append(val)
        
        # Ask for euler sequence for output
        print("\nEnter desired Euler sequence for output (e.g., 'xyz', 'zyx'):")
        quat_sequence = input("Sequence: ").lower()
        
        convert_quat_eular(quat_angles, quat_sequence, degrees=True)
    else:
        print("Invalid choice.")
        return


def visualize_rotation(rotation_matrix, title="Rotated Coordinate Frame"):
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Original axes (world frame)
    origin = np.array([0, 0, 0])
    original_axes = np.eye(3)
    
    # Rotated axes
    rotated_axes = rotation_matrix @ original_axes
    
    # Plot original frame 
    ax.quiver(origin[0], origin[1], origin[2], 
              original_axes[0, 0], original_axes[1, 0], original_axes[2, 0],
              color='lightcoral', arrow_length_ratio=0.15, linewidth=2, 
              alpha=0.3, label='Original X')
    ax.quiver(origin[0], origin[1], origin[2],
              original_axes[0, 1], original_axes[1, 1], original_axes[2, 1],
              color='lightgreen', arrow_length_ratio=0.15, linewidth=2,
              alpha=0.3, label='Original Y')
    ax.quiver(origin[0], origin[1], origin[2],
              original_axes[0, 2], original_axes[1, 2], original_axes[2, 2],
              color='lightblue', arrow_length_ratio=0.15, linewidth=2,
              alpha=0.3, label='Original Z')
    
    # Plot rotated frame 
    ax.quiver(origin[0], origin[1], origin[2],
              rotated_axes[0, 0], rotated_axes[1, 0], rotated_axes[2, 0],
              color='red', arrow_length_ratio=0.15, linewidth=3,
              label="Rotated X'")
    ax.quiver(origin[0], origin[1], origin[2],
              rotated_axes[0, 1], rotated_axes[1, 1], rotated_axes[2, 1],
              color='green', arrow_length_ratio=0.15, linewidth=3,
              label="Rotated Y'")
    ax.quiver(origin[0], origin[1], origin[2],
              rotated_axes[0, 2], rotated_axes[1, 2], rotated_axes[2, 2],
              color='blue', arrow_length_ratio=0.15, linewidth=3,
              label="Rotated Z'")
    
    # labels and limits
    ax.set_xlabel('X', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y', fontsize=12, fontweight='bold')
    ax.set_zlabel('Z', fontsize=12, fontweight='bold')
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=10)
    

    ax.set_box_aspect([1,1,1])
    
    plt.tight_layout()
    plt.show()


def visualize_rotation_steps(eular_angles, eular_sequence, degrees=True):
    fig = plt.figure(figsize=(16, 5))
    
    convention = "Extrinsic" if eular_sequence.isupper() else "Intrinsic"
    seq_lower = eular_sequence.lower()
    
    # Initial frame
    ax1 = fig.add_subplot(141, projection='3d')
    plot_frame(ax1, np.eye(3), "Initial Frame")
    

    cumulative_rot = np.eye(3)
    
    for i, (axis_char, angle) in enumerate(zip(seq_lower, eular_angles)):
        axis_idx = {'x': 0, 'y': 1, 'z': 2}[axis_char]
        

        single_angles = [0, 0, 0]
        single_angles[axis_idx] = angle
        
        if eular_sequence.isupper():  # Extrinsic

            rot = R.from_euler(axis_char.upper(), angle, degrees=degrees)
            cumulative_rot = rot.as_matrix() @ cumulative_rot
        else:  # Intrinsic

            rot = R.from_euler(axis_char, angle, degrees=degrees)
            cumulative_rot = cumulative_rot @ rot.as_matrix()
        
        ax = fig.add_subplot(142 + i, projection='3d')
        plot_frame(ax, cumulative_rot, 
                  f"After {axis_char.upper()}={angle:.0f}°\n({convention})")
    
    plt.suptitle(f"Rotation Sequence: {eular_sequence} ({convention})", 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_frame(ax, rotation_matrix, title):

    origin = np.array([0, 0, 0])
    original_axes = np.eye(3)
    rotated_axes = rotation_matrix @ original_axes
    

    ax.quiver(0, 0, 0, 1, 0, 0, color='lightcoral', 
              arrow_length_ratio=0.15, linewidth=1.5, alpha=0.2)
    ax.quiver(0, 0, 0, 0, 1, 0, color='lightgreen',
              arrow_length_ratio=0.15, linewidth=1.5, alpha=0.2)
    ax.quiver(0, 0, 0, 0, 0, 1, color='lightblue',
              arrow_length_ratio=0.15, linewidth=1.5, alpha=0.2)
    

    ax.quiver(0, 0, 0, rotated_axes[0, 0], rotated_axes[1, 0], rotated_axes[2, 0],
              color='red', arrow_length_ratio=0.15, linewidth=2.5)
    ax.quiver(0, 0, 0, rotated_axes[0, 1], rotated_axes[1, 1], rotated_axes[2, 1],
              color='green', arrow_length_ratio=0.15, linewidth=2.5)
    ax.quiver(0, 0, 0, rotated_axes[0, 2], rotated_axes[1, 2], rotated_axes[2, 2],
              color='blue', arrow_length_ratio=0.15, linewidth=2.5)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_box_aspect([1,1,1])


def convert_eular_quat(eular_angles, eular_sequence, degrees=True):
    rot = R.from_euler(eular_sequence, eular_angles, degrees=degrees)
    quat = rot.as_quat() 
    
    convention = "Extrinsic (fixed axes)" if eular_sequence.isupper() else "Intrinsic (rotating axes)"
    
    print("\n" + "="*50)
    print("EULER TO QUATERNION CONVERSION")
    print("="*50)
    print(f"Convention: {convention}")
    print(f"Euler sequence: {eular_sequence}")
    print(f"Euler angles: X={eular_angles[0]:.2f}°, Y={eular_angles[1]:.2f}°, Z={eular_angles[2]:.2f}°")
    print(f"\nQuaternion: x={quat[0]:.6f}, y={quat[1]:.6f}, z={quat[2]:.6f}, w={quat[3]:.6f}")
    print("="*50)
    

    rotation_matrix = rot.as_matrix()
    visualize_rotation(rotation_matrix, 
                      f"Final Rotation: {eular_sequence} ({convention})")
    

    print("\nShowing step-by-step rotation visualization...")
    visualize_rotation_steps(eular_angles, eular_sequence, degrees)


def convert_quat_eular(quat_angles, quat_sequence, degrees=True):

    rot = R.from_quat(quat_angles)
    eular = rot.as_euler(quat_sequence, degrees=degrees)
    
    print("\n" + "="*50)
    print("QUATERNION TO EULER CONVERSION")
    print("="*50)
    print(f"Quaternion: x={quat_angles[0]:.6f}, y={quat_angles[1]:.6f}, z={quat_angles[2]:.6f}, w={quat_angles[3]:.6f}")
    print(f"\nEuler sequence: {quat_sequence.upper()}")
    
    # Map the euler angles to their correct axes based on sequence
    axis_map = {0: 'X', 1: 'Y', 2: 'Z'}
    for i, axis_char in enumerate(quat_sequence):
        axis_name = axis_char.upper()
        print(f"{axis_name} = {eular[i]:.2f}°")
    
    print("="*50)
    
    # Visualize the rotation
    rotation_matrix = rot.as_matrix()
    visualize_rotation(rotation_matrix, 
                      f"Rotation from Quaternion")


if __name__ == "__main__":
    user_input()
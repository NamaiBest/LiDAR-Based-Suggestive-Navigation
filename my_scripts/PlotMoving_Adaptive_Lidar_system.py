#!/usr/bin/env python3
"""
Moving Suggestive LiDAR Navigation - Auto-scaling View
Real-time polar plot with dynamic scaling based on detected objects
"""
import os
import ydlidar
import time
import sys
from matplotlib.patches import Arc, FancyArrow, Wedge, Rectangle
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# ============== CONFIGURATION PARAMETERS ==============
RMAX_ABSOLUTE = 8.0  # Absolute maximum display range in meters - EASILY ADJUSTABLE
RMIN_DISPLAY = 2.0   # Minimum display range (won't zoom closer than this)
MAX_SENSING_DISTANCE = 8.0  # Maximum sensing distance in meters - EASILY ADJUSTABLE

# Wheelchair footprint parameters
WHEELCHAIR_WIDTH = .50   # Width in meters - EASILY ADJUSTABLE
WHEELCHAIR_LENGTH = .60  # Length in meters - EASILY ADJUSTABLE

# LiDAR position relative to wheelchair footprint (x, y in meters)
LIDAR_X = 0.25  # X position (0.5m = center of 1m width) - EASILY ADJUSTABLE
LIDAR_Y = 0.3  # Y position (0.5m = center of 1m length) - EASILY ADJUSTABLE

# Color coding thresholds for proximity warning
DANGER_ZONE = 0.20  # Distance in meters - RED zone (very close, 10-20cm from wheelchair)
CAUTION_ZONE = 0.70  # Distance from wheelchair boundary - YELLOW zone starts here
# GREEN zone is beyond CAUTION_ZONE (safe distance)

# Auto-scaling parameters
SCALE_MARGIN = 1.2  # Add 20% margin to furthest point for better visibility
SMOOTHING_FACTOR = 0.3  # Smoothing for scale changes (0=instant, 1=no change)
# ======================================================

# Create figure with dark theme
fig = plt.figure(figsize=(10, 10), facecolor='#0a1929')  # Dark navy background
fig.canvas.manager.set_window_title('Moving Suggestive LiDAR Navigation')
lidar_polar = plt.subplot(polar=True)
lidar_polar.set_theta_zero_location('N')  # Set 0° to top (North)
lidar_polar.set_theta_direction(-1)  # Counterclockwise

# Style the plot with dark theme
lidar_polar.set_facecolor('#0a1929')  # Dark navy background
lidar_polar.grid(True, color='white', alpha=0.3, linestyle='--', linewidth=0.5)
lidar_polar.tick_params(colors='white')
lidar_polar.spines['polar'].set_color('white')

ports = ydlidar.lidarPortList()
port = "/dev/ydlidar"
for key, value in ports.items():
    port = value
    print(f"Using port: {port}")

laser = ydlidar.CYdLidar()
laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 12.0)  # Maximum frequency
laser.setlidaropt(ydlidar.LidarPropSampleRate, 5)
laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
laser.setlidaropt(ydlidar.LidarPropMaxRange, RMAX_ABSOLUTE)  # Use configurable max range
laser.setlidaropt(ydlidar.LidarPropMinRange, 0.08)
laser.setlidaropt(ydlidar.LidarPropIntenstiy, False)

scan = ydlidar.LaserScan()
scan_count = 0
current_rmax = RMAX_ABSOLUTE  # Start with max range

def get_distance_to_wheelchair_boundary(x, y):
    """
    Calculate the minimum distance from a point (x, y) to the wheelchair boundary.
    The wheelchair is centered at origin with dimensions WHEELCHAIR_WIDTH x WHEELCHAIR_LENGTH.
    """
    half_width = WHEELCHAIR_WIDTH / 2.0
    half_length = WHEELCHAIR_LENGTH / 2.0
    
    # Calculate distance to each edge
    dx = max(abs(x) - half_width, 0)
    dy = max(abs(y) - half_length, 0)
    
    # Euclidean distance to nearest point on rectangle
    return np.sqrt(dx**2 + dy**2)

def get_point_color(distance_to_boundary):
    """
    Return RGB color based on distance to wheelchair boundary.
    RED (danger) -> YELLOW (caution) -> GREEN (safe)
    """
    if distance_to_boundary <= DANGER_ZONE:
        # RED zone - very close, danger!
        return np.array([1.0, 0.0, 0.0])  # Pure red
    elif distance_to_boundary <= CAUTION_ZONE:
        # Transition from RED to YELLOW to GREEN
        normalized = (distance_to_boundary - DANGER_ZONE) / (CAUTION_ZONE - DANGER_ZONE)
        
        if normalized < 0.5:
            # RED to YELLOW transition
            t = normalized * 2.0
            r = 1.0
            g = t
            b = 0.0
        else:
            # YELLOW to GREEN transition
            t = (normalized - 0.5) * 2.0
            r = 1.0 - t
            g = 1.0
            b = 0.0
        
        return np.array([r, g, b])
    else:
        # GREEN zone - safe distance
        return np.array([0.0, 1.0, 0.0])  # Pure green

def animate(num):
    global scan_count, current_rmax
    
    r = laser.doProcessSimple(scan)
    if r:
        scan_count += 1
        angle = []
        ran = []
        
        for point in scan.points:
            angle.append(point.angle)
            ran.append(point.range)
        
        # Calculate dynamic range based on furthest point
        if len(ran) > 0:
            max_distance = max(ran)
            target_rmax = min(max_distance * SCALE_MARGIN, RMAX_ABSOLUTE)
            target_rmax = max(target_rmax, RMIN_DISPLAY)  # Don't go below minimum
            
            # Smooth the transition
            current_rmax = current_rmax * (1 - SMOOTHING_FACTOR) + target_rmax * SMOOTHING_FACTOR
        else:
            current_rmax = RMAX_ABSOLUTE
        
        lidar_polar.clear()
        lidar_polar.set_ylim(0, current_rmax)  # Auto-scaling
        lidar_polar.set_rmax(current_rmax)
        lidar_polar.set_theta_zero_location('N')  # Front pointing up
        lidar_polar.set_theta_direction(-1)  # Counterclockwise
        
        # Style with dark theme
        lidar_polar.set_facecolor('#0a1929')
        lidar_polar.grid(True, color='white', alpha=0.3, linestyle='--', linewidth=0.5)
        lidar_polar.tick_params(colors='white', labelsize=9)
        lidar_polar.spines['polar'].set_color('white')
        
        # Draw area-based segmentation with interpolated boundary
        if len(angle) > 0:
            # Convert to numpy arrays
            angles = np.array(angle)
            ranges = np.array(ran)
            
            # Normalize angles to [-pi, pi)
            angles = ((angles + np.pi) % (2*np.pi)) - np.pi
            
            # Replace invalid ranges with current_rmax
            ranges_clean = np.copy(ranges)
            invalid_mask = (ranges_clean <= 0) | (ranges_clean > current_rmax) | np.isnan(ranges_clean)
            ranges_clean[invalid_mask] = current_rmax
            
            # Interpolate the boundary on a dense theta grid
            idx_sort = np.argsort(angles)
            a_sorted = angles[idx_sort]
            r_sorted = ranges_clean[idx_sort]
            
            # Extend for wrap-around
            a_ext = np.concatenate([a_sorted - 2*np.pi, a_sorted, a_sorted + 2*np.pi])
            r_ext = np.concatenate([r_sorted, r_sorted, r_sorted])
            
            # Dense theta grid (720 points -> 0.5 degree resolution)
            theta_grid = np.linspace(-np.pi, np.pi, 720)
            r_grid = np.interp(theta_grid, a_ext, r_ext)
            r_grid = np.clip(r_grid, 0.0, current_rmax)
            
            # Fill the area OUTSIDE the boundary (darker = obstacles/unknown)
            lidar_polar.fill_between(theta_grid, r_grid, current_rmax,
                                     where=(r_grid < current_rmax),
                                     interpolate=True,
                                     color='black', alpha=0.35, zorder=2, linewidth=0)
        
        # Draw the LiDAR points with distance-based color coding
        if len(angle) > 0:
            colors = []
            for ang, r in zip(angle, ran):
                # Convert to Cartesian coordinates
                x = r * np.cos(ang)
                y = r * np.sin(ang)
                
                # Calculate distance to wheelchair boundary
                dist_to_boundary = get_distance_to_wheelchair_boundary(x, y)
                
                # Get color based on distance
                color = get_point_color(dist_to_boundary)
                colors.append(color)
            
            colors = np.array(colors)
            lidar_polar.scatter(angle, ran, c=colors, s=10, alpha=0.9, edgecolors='white', linewidth=0.3, zorder=6)
        
        # Add wheelchair footprint (drawn BELOW all LiDAR data)
        half_width = WHEELCHAIR_WIDTH / 2.0
        half_length = WHEELCHAIR_LENGTH / 2.0
        rect_x = -half_width
        rect_y = -half_length
        
        wheelchair_rect = Rectangle((rect_x, rect_y), WHEELCHAIR_WIDTH, WHEELCHAIR_LENGTH,
                                   transform=lidar_polar.transData._b,
                                   facecolor='lightgray', 
                                   edgecolor='gray',
                                   alpha=0.3,
                                   linewidth=1.5,
                                   zorder=1)
        lidar_polar.add_patch(wheelchair_rect)
        
        # Add front direction arrow
        arrow_length = current_rmax * 0.12
        arrow_start = current_rmax * 0.02
        arrow_width = 0.20
        
        arrow_tip = [0, arrow_start + arrow_length]
        arrow_left = [arrow_width, arrow_start + arrow_length * 0.7]
        arrow_right = [-arrow_width, arrow_start + arrow_length * 0.7]
        
        lidar_polar.fill([arrow_left[0], 0, arrow_right[0], arrow_left[0]], 
                        [arrow_left[1], arrow_tip[1], arrow_right[1], arrow_left[1]],
                        color='#ff3366', alpha=0.9, zorder=10, edgecolor='white', linewidth=1.5)
        
        lidar_polar.plot([0, 0], [arrow_start, arrow_start + arrow_length * 0.6], 
                        color='#ff3366', linewidth=3, alpha=0.9, zorder=10)
        
        center_circle = plt.Circle((0, 0), current_rmax * 0.015, transform=lidar_polar.transData._b,
                                  facecolor='#ff3366', zorder=11, edgecolor='white', linewidth=2)
        lidar_polar.add_patch(center_circle)
        
        lidar_polar.text(0, arrow_start + arrow_length + current_rmax * 0.06, 'FRONT',
                        ha='center', va='bottom', fontsize=12, fontweight='bold',
                        color='#ff3366', zorder=12)
        
        # Add current range marker
        lidar_polar.text(np.pi/4, current_rmax * 0.95, f'{current_rmax:.1f}m', 
                        ha='center', fontsize=9, color='white', alpha=0.7)
        
        # Display frequency and stats with zoom level
        if scan.config.scan_time > 0:
            freq = 1.0 / scan.config.scan_time
            title = f'Moving Navigation (Auto-Zoom: {current_rmax:.1f}m) | Scan #{scan_count} | Points: {len(angle)} | {freq:.2f} Hz'
        else:
            title = f'Moving Navigation (Auto-Zoom: {current_rmax:.1f}m) | Scan #{scan_count} | Points: {len(angle)} | Initializing...'
        
        lidar_polar.set_title(title, pad=25, fontsize=13, fontweight='bold', color='white')

print("\n=== Moving Suggestive LiDAR Navigation ===")
print(f"Port: {port}")
print(f"Baudrate: 115200")
print(f"Scan Frequency: 12.0 Hz (Maximum)")
print(f"Sample Rate: 5 kHz")
print(f"Auto-scaling Range: {RMIN_DISPLAY}m - {RMAX_ABSOLUTE}m")
print(f"Scale Margin: {SCALE_MARGIN}x (adds {int((SCALE_MARGIN-1)*100)}% buffer)")
print("==========================================\n")

ret = laser.initialize()
if ret:
    print("✓ LiDAR initialized successfully!")
    ret = laser.turnOn()
    if ret:
        print("✓ LiDAR scanning started!")
        print("\n🔍 Auto-scaling enabled - View adjusts to detected objects")
        print("Close the matplotlib window to stop...\n")
        ani = animation.FuncAnimation(fig, animate, interval=10, cache_frame_data=False)
        plt.show()
    else:
        print("✗ Failed to turn on LiDAR!")
    laser.turnOff()
else:
    print("✗ Failed to initialize LiDAR!")

laser.disconnecting()
plt.close()
print("\n✓ LiDAR disconnected.")

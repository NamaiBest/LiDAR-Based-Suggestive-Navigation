#!/usr/bin/env python3
"""
TOF LiDAR Test - Maximum Frequency Version
Optimized for highest scan rate
"""
import os
import ydlidar
import time
import sys

if __name__ == "__main__":
    ydlidar.os_init()
    ports = ydlidar.lidarPortList()
    port = "/dev/ydlidar"
    for key, value in ports.items():
        port = value
        print(f"Found LiDAR port: {port}")
    
    laser = ydlidar.CYdLidar()
    
    # Configure for maximum performance
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 512000)  # Maximum baudrate
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TOF)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 12.0)  # Maximum scan frequency (12 Hz)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 20)  # Maximum sample rate
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
    
    print("\n=== YDLidar TOF Configuration ===")
    print(f"Port: {port}")
    print(f"Baudrate: 512000")
    print(f"Scan Frequency: 12.0 Hz (Maximum)")
    print(f"Sample Rate: 20 kHz")
    print(f"Dual Channel: Enabled")
    print("=================================\n")

    ret = laser.initialize()
    if ret:
        print("LiDAR initialized successfully!")
        ret = laser.turnOn()
        if ret:
            print("LiDAR scanning started!\n")
            scan = ydlidar.LaserScan()
            count = 0
            start_time = time.time()
            
            while ret and ydlidar.os_isOk():
                r = laser.doProcessSimple(scan)
                if r:
                    count += 1
                    actual_freq = 1.0 / scan.config.scan_time
                    print(f"Scan #{count} [Stamp: {scan.stamp:.3f}] Points: {scan.points.size():4d} | Frequency: {actual_freq:.2f} Hz")
                else:
                    print("Failed to get LiDAR Data.")
                
                # Minimal sleep to maximize throughput
                time.sleep(0.001)  # 1ms sleep for minimal CPU usage
                
        else:
            print("Failed to turn on LiDAR!")
        
        laser.turnOff()
        print("\nLiDAR stopped.")
    else:
        print("Failed to initialize LiDAR!")
        print(f"Error: {laser.DescribeError()}")
    
    laser.disconnecting()
    print("LiDAR disconnected.")

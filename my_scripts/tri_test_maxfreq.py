import os
import ydlidar
import time

if __name__ == "__main__":
    ydlidar.os_init()
    ports = ydlidar.lidarPortList()
    port = "/dev/ydlidar"
    for key, value in ports.items():
        port = value
        print(port)
    
    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)  # Standard baudrate
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 12.0)  # Maximum frequency
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 5)  # Adjusted sample rate
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, True)
    laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
    laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
    laser.setlidaropt(ydlidar.LidarPropMaxRange, 8.0)  # Maximum working range
    laser.setlidaropt(ydlidar.LidarPropMinRange, 0.08)  # Minimum working range
    laser.setlidaropt(ydlidar.LidarPropIntenstiy, False)

    ret = laser.initialize()
    if ret:
        ret = laser.turnOn()
        scan = ydlidar.LaserScan()
        scan_count = 0
        while ret and ydlidar.os_isOk():
            r = laser.doProcessSimple(scan)
            if r:
                scan_count += 1
                # Check if scan_time is valid before calculating frequency
                if scan.config.scan_time > 0:
                    freq = 1.0 / scan.config.scan_time
                    print(f"Scan #{scan_count} [Stamp: {scan.stamp:.3f}] Points: {scan.points.size():4d} | Frequency: {freq:.2f} Hz")
                else:
                    print(f"Scan #{scan_count} [Stamp: {scan.stamp:.3f}] Points: {scan.points.size():4d} | Frequency: waiting...")
            else:
                print("Failed to get Lidar Data")
            time.sleep(0.001)  # Minimal sleep for maximum throughput
        laser.turnOff()
    laser.disconnecting()

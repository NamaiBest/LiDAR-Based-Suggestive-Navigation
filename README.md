# LiDAR-Based Suggestive Navigation

Real-time wheelchair navigation system using YDLidar with distance-based safety visualization. Built with bare Python (no ROS), making it simple and easy to deploy.

## Hardware

**Tested Configuration:**
- YDLidar X2 (Triangle Series)
- Raspberry Pi 5
- Raspbian GNU/Linux 12 (Bookworm)

**Compatible with:**
- Other YDLidar Triangle Series (X2L, X4, etc.)
- Any Linux system with USB serial support
- Raspberry Pi 3/4/5 and similar boards

## Installation

### 1. Clone this repository
```bash
git clone <your-repo-url>
cd Lidar
```

### 2. Run the installation script
```bash
./install_dependencies.sh
```

The script will:
- Install required system packages (cmake, pkg-config, swig, git)
- Install Python dependencies (matplotlib, numpy)
- Download and build YDLidar SDK
- Install SDK system-wide to `/usr/local/`
- Configure serial port permissions

**Important:** If added to the `dialout` group, log out and back in before using the LiDAR.

### 3. Connect your LiDAR
Plug in your YDLidar X2 via USB. It should appear as `/dev/ttyUSB0`.

## Usage

### Interactive Menu (Recommended)
```bash
./run_navigation.sh
```

This launches an interactive menu with options:
1. **Fixed-scale view** (5m range) - Classic visualization
2. **Fixed-scale with adaptive shading** (6m range) - Shows unknown/obstacle regions
3. **Auto-scaling view** (2-8m dynamic) - Best for exploration
4. **Auto-scaling with adaptive shading** (2-8m) - Dynamic zoom + region awareness
5. **Console test** - No GUI, prints scan data
6. **Exit**

### Direct Execution
```bash
cd my_scripts
./run.sh plot_tri_maxfreq.py
```

## Features

### Fixed-Scale Visualization
- Constant 5-meter display range
- Wheelchair footprint overlay (0.5m × 0.6m)
- LiDAR positioned at (0.25m, 0.3m) from center
- Color-coded safety zones:
  - Red: < 0.20m (danger)
  - Yellow: 0.20m - 0.70m (caution)
  - Green: > 0.70m (safe)

### Auto-Scaling Visualization
- Dynamic range from 2m to 8m
- Smooth zoom transitions
- Adapts to environment size
- Same safety color coding

### Adaptive Region Shading (NEW)
- **Boundary interpolation**: Creates smooth, continuous boundaries from sparse LiDAR points
- **Visual segmentation**: Dark shading highlights areas outside detected boundaries
- **Real-time obstacle awareness**: Instantly see navigable vs. unknown/blocked regions
- **720-point interpolation**: Sub-degree angular resolution for precise boundaries
- Available in both fixed and auto-scaling modes

### Configuration
Edit parameters at the top of any script:
```python
RMAX = 5.0              # Display range (meters)
WHEELCHAIR_WIDTH = 0.50  # Width (meters)
WHEELCHAIR_LENGTH = 0.60 # Length (meters)
DANGER_ZONE = 0.20      # Red threshold (meters)
CAUTION_ZONE = 0.70     # Yellow/green transition (meters)
```

## What Makes This Different

**No ROS Required**
- Direct Python communication with YDLidar SDK
- No middleware, no complex dependencies
- Runs on minimal systems

**Simple to Extend**
- All code in readable Python
- Easy to add path planning algorithms
- Simple integration with other sensors

**Wheelchair-Focused**
- Designed for mobility applications
- Real-time obstacle awareness
- Intuitive color-coded feedback

## Technical Details

**YDLidar X2 Specifications:**
- Range: 0.08m - 8.0m
- Scan Frequency: 12 Hz
- Sample Rate: 3 kHz
- Points per Scan: ~280
- Interface: USB Serial (115200 baud)

**Distance Calculation:**
```
distance = sqrt(max(|x| - half_width, 0)² + max(|y| - half_length, 0)²)
```

## Project Structure

```
Lidar/
├── my_scripts/
│   ├── plot_tri_maxfreq.py                         # Fixed 5m visualization
│   ├── Adaptive Lidar system.py                    # Fixed 6m with region shading
│   ├── plot_moving_suggestive_lidar_navigation.py # Auto-scaling 2-8m
│   ├── PlotMoving Adaptive Lidar system.py        # Auto-scaling with region shading
│   ├── tri_test_maxfreq.py                         # Console test
│   ├── tof_test_maxfreq.py                         # TOF LiDAR test
│   └── run.sh                                       # Launch helper
├── run_navigation.sh       # Interactive menu
├── install_dependencies.sh # Setup script
├── requirements.txt        # Python packages
└── README.md              # This file
```

## Troubleshooting

**"ModuleNotFoundError: No module named 'ydlidar'"**
- Use `./run_navigation.sh` or `cd my_scripts && ./run.sh script_name.py`
- Or set: `export PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTHONPATH`

**"Permission denied" on /dev/ttyUSB0**
- Add yourself to dialout group: `sudo usermod -a -G dialout $USER`
- Log out and log back in

**LiDAR not detected**
- Check connection: `lsusb | grep CP210`
- Check port: `ls /dev/ttyUSB*`
- Verify baudrate is 115200 in script

**"Fail to get baseplate device information"**
- This warning is normal and doesn't affect operation

## Future Plans

- Path prediction algorithms
- Obstacle detection and classification
- Data logging for analysis
- Machine learning integration
- Multi-sensor fusion

## License

This project is independent of the YDLidar SDK. See the [YDLidar SDK repository](https://github.com/YDLIDAR/YDLidar-SDK) for SDK licensing.

## Credits

Built using [YDLidar SDK](https://github.com/YDLIDAR/YDLidar-SDK) for wheelchair navigation applications.

#!/bin/bash
# Simple launcher for LiDAR Navigation scripts

cd "$(dirname "$0")/my_scripts"
export PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTHONPATH

echo "=========================================="
echo "    LiDAR Navigation Launcher"
echo "=========================================="
echo ""
echo "Choose a visualization mode:"
echo ""
echo "  1) Fixed-scale view (5m range)"
echo "  2) Fixed-scale with area segmentation (6m range)"
echo "  3) Auto-scaling view (2-8m dynamic)"
echo "  4) Auto-scaling with area segmentation (2-8m)"
echo "  5) Console test (no GUI)"
echo "  6) Exit"
echo ""
read -p "Enter your choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo "Starting fixed-scale visualization..."
        python3 plot_tri_maxfreq.py
        ;;
    2)
        echo ""
        echo "Starting fixed-scale with area segmentation..."
        python3 "Adaptive_Lidar_system.py"
        ;;
    3)
        echo ""
        echo "Starting auto-scaling visualization..."
        python3 plot_moving_suggestive_lidar_navigation.py
        ;;
    4)
        echo ""
        echo "Starting auto-scaling with area segmentation..."
        python3 "PlotMoving_Adaptive_Lidar_system.py"
        ;;
    5)
        echo ""
        echo "Starting console test..."
        python3 tri_test_maxfreq.py
        ;;
    6)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

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
echo "  1) Fixed-scale view (5m range) - Recommended"
echo "  2) Auto-scaling view (2-8m dynamic)"
echo "  3) Console test (no GUI)"
echo "  4) Exit"
echo ""
read -p "Enter your choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Starting fixed-scale visualization..."
        python3 plot_tri_maxfreq.py
        ;;
    2)
        echo ""
        echo "Starting auto-scaling visualization..."
        python3 plot_moving_suggestive_lidar_navigation.py
        ;;
    3)
        echo ""
        echo "Starting console test..."
        python3 tri_test_maxfreq.py
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

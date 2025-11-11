#!/bin/bash
# Helper script to run LiDAR scripts with proper Python path

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTHONPATH

# Check if a script name was provided
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <script_name.py>"
    echo ""
    echo "Available scripts:"
    echo "  tri_test_maxfreq.py      - Console test at max frequency"
    echo "  plot_tri_maxfreq.py      - Real-time visualization"
    echo "  tof_test_maxfreq.py      - TOF LiDAR console test"
    echo ""
    exit 1
fi

SCRIPT_NAME=$1

# Check if file exists
if [ ! -f "$SCRIPT_DIR/$SCRIPT_NAME" ]; then
    echo "Error: Script '$SCRIPT_NAME' not found in $SCRIPT_DIR"
    exit 1
fi

# Run the script
cd "$SCRIPT_DIR"
python3 "$SCRIPT_NAME"

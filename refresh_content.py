#!/usr/bin/env python3
"""
Run the Clean ABAP to Hugo conversion.
This is a convenience script to run the conversion from the repository root.
"""

import os
import sys

# Add the scripts directory to the path
scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
sys.path.insert(0, scripts_dir)

# Import and run the main script
from scripts.main import main

if __name__ == '__main__':
    main()

"""Convenience launcher for the ADB device selector."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from umauto.tools.check_device import main

if __name__ == "__main__":
    main()

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from umauto.app import run

if __name__ == "__main__":
    run()

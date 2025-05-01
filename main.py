import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app import App

if __name__ == "__main__":
    app = App()
    app.run()

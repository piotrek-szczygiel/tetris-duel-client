import os
import sys


def path(filename: str) -> str:
    if getattr(sys, "frozen", False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    directory = os.path.join(application_path, "resources")
    return os.path.join(directory, filename)

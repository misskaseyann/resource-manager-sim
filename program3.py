import sys

import tkinter as tk
from tkinter import *
import os

from program3.core import Core
from program3.simwindow import SimWindow

if __name__ == "__main__":

    c = Core()
    sw = SimWindow(c)
    sw.loop()




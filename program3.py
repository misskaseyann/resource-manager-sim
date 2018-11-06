from program3.core import Core
from program3.simwindow import SimWindow


if __name__ == "__main__":
    c = Core()
    w = SimWindow(c)
    w.loop()
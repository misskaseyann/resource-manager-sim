from program3.core import Core

if __name__ == "__main__":
    fp = input("Give the file path: ")
    c = Core()
    c.read_file(fp)
    c.init_state()

    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
    c.step_forward()
    c.deadlock_detection()
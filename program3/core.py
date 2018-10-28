# Start file...


class Core(object):
    def __init__(self):
        print("sup")

    def read_file(self, fp):
        try:
            f = open(fp,'r')
        except IOError:
            print("Cannot find the file at ", fp)
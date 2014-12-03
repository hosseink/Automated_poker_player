import sys
import re
from StringIO import StringIO

def test():
    overwrite = raw_input("The file exists, overwrite? ")
    notify = raw_input("This file is marked for notifies.  Notify?")
    sys.__stdout__.write("Overwrite: %s, Notify: %s" % (overwrite,notify))

class Catcher(object):
    def __init__(self, stdin):
        self.stdin = stdin

    def write(self, msg):
        if re.search("The file exists, overwrite?", msg):
            self.stdin.truncate(0)
            self.stdin.write('yes\n')
            self.stdin.seek(0)
        if re.search("This file is marked for notifies.  Notify?", msg):
            self.stdin.truncate(0)
            self.stdin.write('no\n')
            self.stdin.seek(0)

sys.stdin = StringIO()
sys.stdout = Catcher(sys.stdin)
test()

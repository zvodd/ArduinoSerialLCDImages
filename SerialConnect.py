import serial
import time
import os

IMAGE_DIR = os.path.abspath('./images/')

# SER_BAUD =  9600
SER_BAUD =  115200

# windows
SER_DEVICE = 'COM5'
# linux
# SER_DEVICE = '/dev/tty.usbserial' 

SCON = serial.Serial(SER_DEVICE, SER_BAUD)

waittime = 0.2

class MyImages(object):
    """
    Takes a list of filenames,
     opens and reads each files binary data into list.

    get() method: to get next "frame" in a circular loop.

    TODO: Should be using the standard generator interface.
          Was too lazy / don't remember how.
    """
    def __init__(self, frames):
        self.bytesbuf = list()
        for fname in frames:
            # fname = "output{}.bin".format(i)
            with open(fname,'rb') as fh:
                self.bytesbuf.append(fh.read())
        self.indx = 0

    def get(self):
        """Returns the next "frame" (raw bytes from file)
        """
        rv = self.bytesbuf[self.indx]
        self.indx += 1
        if self.indx >= len(self.bytesbuf):
            self.indx = 0
        return rv

def wait_state(frames):
    """ 
    Reads from serial, waits and repeats.
    If received the message "Ready",
        send a frame and continues.
    """
    while True:
        check = SCON.readline()
        print check
        time.sleep(waittime)
        if check.find("Ready") == 0:
            SCON.write(frames.get())


def main():
    frame_names = (os.path.join(IMAGE_DIR, fn)
                    for fn in os.listdir(IMAGE_DIR)
                        if fn.endswith(".bin")
                  )
    frames = MyImages(frame_names)
    wait_state(frames)

if __name__ == '__main__':
    main()
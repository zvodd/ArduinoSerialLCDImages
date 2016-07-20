from PIL import Image
import os

"""
Opens all bmp files in a directory.
Converts to raw binary format to drive nokia LCD screen.
Assumes 84x48 image size.
Color is coverted automaticly to black and white (if not poorly).
"""

TARGET_DIRECTORY = "."

def bmp_2_bytestring(filename):
    '''
    Takes a image by file name.
    Opens image and iterates pixels in the order
     created by pixels_generator.
    Converts each pixel value to a bit.
    Returns string of bytes from bits.
    The bit is selected based on the value of the byte:
        less then 128 = 1
        else 0
    '''
    img = Image.open(filename)
    w, h = img.size
    pixel_acc = img.load()

    generated_pixels = pixels_generator(pixel_acc, w,h)
    obytes = str()
    cbyte = 0
    for i,v in enumerate(generated_pixels):
        rot_indx = i % 8
        if v < 128:
            cbyte |= 1 << rot_indx
        # every 8 bytes send a byte.
        if rot_indx == 0:
            obytes += chr(cbyte)
            cbyte = 0
    return obytes

def pixels_generator(pixel_acc, w,h):
    ''' Access pixels of images
    Yeild a int for every pixel
     Grabs pixels from x[0] to x[w] going down y+8 pixels at a time,
     then back to y+0.
    '''
    for y in range(0,h / 8):
        for x in range(0,w):
            for y2 in range(0,8):
                yield pixel_acc[x,(y*8)+y2]



def main():
    cdir = os.path.abspath(TARGET_DIRECTORY)

    fn_gen = ( x for x in os.listdir(cdir)
                 if x.endswith('.bmp')
             )

    for count, filename in enumerate(fn_gen):
        databytes = bmp_2_bytestring(filename)
        print "Read file'{}'".format(filename)

        new_fn = "output{}.bin".format(count+1)
        new_fullfn =  os.path.join(cdir, new_fn)

        #open and write nokia lcd format binary file
        with open(new_fullfn, 'wb') as outfile:
            outfile.write(databytes)
            print "Wrote file '{}'".format(new_fn)

if __name__ == '__main__':
    main()
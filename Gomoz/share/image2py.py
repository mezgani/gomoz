"""
image2py
Pete Shinners - Dec 30, 2001

image2py will take an image file, and embed it into a regular .PY file.
the image is converted to a string and then compressed and converted to
a base64 string. the image will also preserve its colorkey and palette.

note that the script created comes with a small amount of bootstrap code
to display the image embedded in the file. (just in case you later need
to determine what all those long strings really look like) :]

this is mainly a handy utility. it doesn't really useful in all situations.
but in cases where you create your own small utility module for pygame, you
might want to use small bitmapped images. instead of requiring external
resources, you can cut and paste the python code to create the image into
your script.

obviously you'll want to keep the image size within reason. anything bigger
than 100x100 is going to create a sizeable PY file.
"""


import sys, os
import pygame, pygame.image, zlib, base64


packed_image_file = r"""#!/usr/bin/env python
import base64, zlib, pygame, pygame.image
pygame.display.init()
size = %r
type = %r
imagedata = ''.join((
%s
))
image = pygame.image.fromstring(zlib.decompress(base64.decodestring(imagedata)),size, type)
%s
if __name__ == '__main__':
    pygame.init()
    s = pygame.display.set_mode(image.get_size())
    image.set_colorkey()
    s.blit(image, (0,0))
    pygame.display.flip()
    while 1:
        if pygame.event.wait().type in \
           (pygame.QUIT,pygame.KEYDOWN): break
"""


def embedimage(imagename, outfilename):
    img = pygame.image.load(imagename)

    type = 'RGB'
    if img.get_bytesize() == 1:
        type = 'P'
    elif img.get_masks()[3]:
        type = 'RGBA'

    imgstring = pygame.image.tostring(img, type)
    imgcompressed = zlib.compress(imgstring, 9)
    encoded = base64.encodestring(imgcompressed)

    instructions = ''
    if img.get_bitsize() == 8:
        pal = img.get_palette()
        palstr = ''
        for x in range(0, len(pal), 6):
            palstr += '  ' + repr(pal[x:x+6])[1:-1] + ',\n'
        instructions += 'palette = (%s)\n' % palstr
        instructions += 'image.set_palette(palette)\n'
    if img.get_colorkey():
        instructions += 'image.set_colorkey(%r)\n' % (img.get_colorkey()[:3],)
    if img.get_masks()[3]:
        instructions += 'image.set_alpha(255)\n'
    elif img.get_alpha():
        instructions += 'image.set_alpha(%i)\n' % img.get_alpha()

    file = open(outfilename, 'w')
    prettydata = ',\n'.join(map(repr, (encoded.split())))
    file.write(packed_image_file%(img.get_size(), type, prettydata, instructions))




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE:', sys.argv[0], '\n<imagename> <outfile.py>\n'
        sys.exit()
    embedimage(sys.argv[1], sys.argv[2])




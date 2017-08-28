from PIL import Image
from django.conf import settings


filepath = './media/articles/vasu/6b9cbe70c9-cat-1285634_960_720.png'


im = Image.open(filepath)

width, height = (im.size)
print ('Height:', height)
print ('Width:', width)

if height < width:
    print ('INSODE FOR')
    difference = (width - height)/2
    x = difference
    y = 0
    w = width - difference
    h = height
    im.crop((x, y, w, h))
    im.save('thubmail.jpg')
# elif height > width:
#     print ('ISISCNIJN')

#     difference = (height-width)/2



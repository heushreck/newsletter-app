# open all logo png files and resize them to 200x100
import os
from PIL import Image

for filename in os.listdir('logos'):
    if filename.endswith('.png'):
        img = Image.open('logos/'+filename)
        # create a new transparent image with the size 400x200
        new_img = Image.new('RGBA', (400, 200), (0, 0, 0, 0))
        # resize the image to have a height of 185px
        img = img.resize((int(185*img.width/img.height), 185))
        # if the image is still too wide, resize it to have a width of 380px
        if img.width > 400:
            img = img.resize((380, int(380*img.height/img.width)))
        # paste the resized image into the new image in the center
        new_img.paste(img, (int((400-img.width)/2), int((200-img.height)/2)))
        # save the new image
        new_img.save('logos2/'+filename)

        
        



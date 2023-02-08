from PIL import Image as img
import matplotlib.pyplot as plt

#left, bottom, right, top
#left = 80
#bottom = 480
#right = 540
#top = 22

# crop background.png image
im = img.open("background_benidorm.png")
im1 = im.crop((80, 22, 540, 480))
im1.save("background.png")



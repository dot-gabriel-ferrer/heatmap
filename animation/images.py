
from PIL import Image
 

# create a function to overlap images
def overlap_images(background, overlay, output):
    img1 = Image.open(background)
    img2 = Image.open(overlay)
    img1.paste(img2, mask = img2)
    img2 = img1.crop((80, 22, 540, 480))
    img2.save(output)
    img1.close()
    img2.close()

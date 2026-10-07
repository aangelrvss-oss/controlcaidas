import sys, glob, os
from PIL import Image, ImageDraw
files = sys.argv[2:]; out = sys.argv[1]
cols = 2; tw = 960
ims = [Image.open(f) for f in files]
th = int(tw * ims[0].height / ims[0].width)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * (th + 24)), (20, 20, 20))
d = ImageDraw.Draw(sheet)
for i, (f, im) in enumerate(zip(files, ims)):
    x, y = (i % cols) * tw, (i // cols) * (th + 24)
    sheet.paste(im.resize((tw, th)), (x, y + 24)); d.text((x + 6, y + 4), os.path.basename(f), fill=(200, 200, 200))
sheet.save(out)

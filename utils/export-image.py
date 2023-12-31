from PIL import Image as PImage
from PIL import ImageTk

from tkinter import *
from tkinter import ttk

from pathlib import Path

root = Tk()
content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=5, relief="ridge")

content.grid(column=0, row=0, columnspan=4)
frame.grid(column=0, row=0, columnspan=4, rowspan=2)

l = ttk.Label(frame)
l.grid(column=0, row=0, columnspan=4)

l2 = ttk.Label(frame)
l2.grid(column=0, row=1, columnspan=4)


# design_rpath = Path("Design/820x205_small.png")
# design_rpath = Path("Design/bg_8color.png")
design_rpath = Path("Design/bg_8color_2.png")
src_rpath = Path("fw/src/generated_image.c")
header_rpath = Path("fw/include/generated_image.h")
bin_rpath = Path("BG.BIN")

py_file = Path(__file__).resolve()
p = py_file.parent.parent.joinpath(design_rpath)

header_file = py_file.parent.parent.joinpath(header_rpath)
src_file = py_file.parent.parent.joinpath(src_rpath)
bin_file = py_file.parent.parent.joinpath(bin_rpath)

im = PImage.open(p)
stdimg = ImageTk.PhotoImage(im)
l.configure(image=stdimg)
l.image=stdimg

# Scale Variables
r_val = IntVar()
r_val.set(128)
g_val = IntVar()
g_val.set(128)
b_val = IntVar()
b_val.set(128)

im2 = None

def update_image():
    if im.mode is "RGBA":
        r, g, b, _ = im.split()
    elif im.mode is "RGB":
        r, g, b = im.split()

    # the resulting 1 bit color 
    R=250
    G=250
    B=250

    BLANK=128

    r = r.point(lambda p: p > r_val.get() and R or 0)
    g = g.point(lambda p: p > g_val.get() and G or 0)
    b = b.point(lambda p: p > b_val.get() and B or 0)

    global im2
    im2 = PImage.merge("RGB", (r, g, b))
    stdimg2 = ImageTk.PhotoImage(im2)
    l2.configure(image=stdimg2)
    l2.image=stdimg2


def red_slider_cb(value):
    update_image()
def green_slider_cb(value):
    update_image()
def blue_slider_cb(value):
    update_image()

r_l = ttk.Label(content, text="R")
r_l.grid(column=1, row=2, columnspan=1)
r_s = ttk.LabeledScale(content, from_=1, to=254, width=100, variable=r_val)
r_s.grid(column=2, row=2, columnspan=3)
r_s.value = 128
r_s.update()
r_s.scale.configure(command=red_slider_cb)

g_l = ttk.Label(content, text="G")
g_l.grid(column=1, row=3, columnspan=1)
g_s = ttk.LabeledScale(content, from_=1, to=254, variable=g_val)
g_s.grid(column=2, row=3, columnspan=3)
g_s.value = 128
g_s.update()
g_s.scale.configure(command=green_slider_cb)

b_l = ttk.Label(content, text="B")
b_l.grid(column=1, row=4, columnspan=1)
b_s = ttk.LabeledScale(content, from_=1, to=254, variable=b_val)
b_s.grid(column=2, row=4, columnspan=3)
b_s.value = 128
b_s.update()
b_s.scale.configure(command=blue_slider_cb)

update_image()

def save_callback():
    import io
    
    sz = im2.size
    # 4-bit mode data
    buffer = io.StringIO()
    binary_buffer = io.BytesIO()
    
    buffer.write("#ifndef GENERATED_IMAGE\n")
    buffer.write("#define GENERATED_IMAGE\n")
    buffer.write("#define IMAGE_WIDTH ({row:.0f})\n".format(row=sz[0]))
    buffer.write("#define IMAGE_ROW IMAGE_WIDTH\n")
    buffer.write("#define IMAGE_HEIGHT ({height:.0f})\n".format(height=sz[1]))
    buffer.write("#define IMAGE_ROW_LENGTH (IMAGE_HEIGHT / 4 + 1)\n")
    buffer.write("extern const uint16_t image[IMAGE_ROW][IMAGE_ROW_LENGTH];\n")

    buffer.write("#endif // GENERATED_IMAGE\n")

    with open(header_file, "w", encoding="utf-8") as f:
        f.write(buffer.getvalue())

    buffer = io.StringIO()
    buffer.write("// This file is generated by script utils/export-image.py\n")
    buffer.write("#include <stdint.h>\n")
    buffer.write("#include \"generated_image.h\"\n")
    buffer.write("const uint16_t image[IMAGE_ROW][IMAGE_ROW_LENGTH] = {\n")
        
    assert(0 == sz[0] % 4)
    width = int(sz[0])
    height = int(sz[1]/4)
    for x in range(0, width):
        buffer.write(" // row {}\n{{".format(x+1))
        buffer.write("0x{row:04x},".format(row=x+1))
        binary_buffer.write((x+1).to_bytes(2))

        for y in range(0, height):
            pixels = []
            pixels.append(im2.getpixel((width - 1 - x, y * 4 + 0)))
            pixels.append(im2.getpixel((width - 1 - x, y * 4 + 1)))
            pixels.append(im2.getpixel((width - 1 - x, y * 4 + 2)))
            pixels.append(im2.getpixel((width - 1 - x, y * 4 + 2)))
            d = 0
            for ip in range(0,4):
                for i in range(0,3): # RGB0RGB0
                    if pixels[ip][i] > 0:
                        p = 1
                    else:
                        p = 0
                    d = d | (p << ((3-i) + 4 * (3-ip)))
            buffer.write("0x{data:04x},".format(data=d))
            binary_buffer.write(d.to_bytes(2))
        buffer.write("},\n")

    buffer.write("}};\n".format(width=sz[0]/4, height=sz[1]))

    with open(src_file, "w", encoding="utf-8") as f:
        f.write(buffer.getvalue())

    with open(bin_file, "wb") as f:
        f.write(binary_buffer.getvalue())

save_btn = ttk.Button(content, text="Save", command=save_callback)
save_btn.grid(column=1, row=5)

# save_callback()
root.mainloop()

from pdfreader import SimplePDFViewer, PageDoesNotExist

fd = open('src/test6.pdf', "rb")
viewer = SimplePDFViewer(fd)

plain_text = ""
pdf_markdown = ""
images = []
try:
    while True:
        viewer.render()
        pdf_markdown += viewer.canvas.text_content
        plain_text += "".join(viewer.canvas.strings)
        images.extend(viewer.canvas.inline_images)
        images.extend(viewer.canvas.images.values())
        viewer.next()
except PageDoesNotExist:
    pass
for i in range(len(images)):
    fax_image = images[i]
    print(fax_image)
    print(type(fax_image))
    pil_image = fax_image.to_Pillow()
    pil_image.save("result/mResult.png")

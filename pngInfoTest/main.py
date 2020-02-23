# from PIL.PngImagePlugin import PngImageFile, PngInfo
# import io
# import pybase64
# from PIL import Image

# buffered = io.BytesIO()
# targetImage = PngImageFile("embed-test.png")

# metadata = PngInfo()
# metadata.add_text("MyNewString", "A string")
# metadata.add_text("MyNewInt", str(1234))

# targetImage.save(, pnginfo=metadata)
# imgdata = pybase64.b64decode(buffered.getvalue())
# hostImage = PngImageFile(imgdata)

# # targetImage = PngImageFile("NewPath.png")

# print(hostImage.text)
from PIL.PngImagePlugin import PngImageFile, PngInfo
import json

targetImage = PngImageFile("embed-test.png")

metadata = PngInfo()
metadata.add_text("MyNewString", "A string")
metadata.add_text("MyNewInt", str(1234))

targetImage.save("NewPath.png", pnginfo=metadata)
targetImage = PngImageFile("NewPath.png")
targetImageSize = targetImage.size
print('targetImage', targetImage, 'targetImageSize', targetImageSize)
a = {'name': 'wang', 'age': 29}
print('nameExist', 'name' in a)
b = json.dumps(a)
print('b', b)
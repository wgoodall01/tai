from PIL import Image
from PIL import WmfImagePlugin

# Write a handler for PIL which returns 10x10 white images when you attempt to load a WMF.

class WmfHandler:
    def open(self, im):
        return Image.new("RGB", (10, 10), "white")

    def load(self, im):
        return self.open(im)

    def save(self, im, fp, filename):
        return None


# Create the stub handler.
wmf_handler = WmfHandler()

# Register the WMF handler.
WmfImagePlugin.register_handler(wmf_handler)
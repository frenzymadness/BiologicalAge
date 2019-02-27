import pydicom
from PIL import Image, ImageQt


class Dicom:
    def __init__(self, filename):
        self.filename = filename

        # Information related to image
        self.data = pydicom.read_file(filename)
        self.size = (self.data.Rows, self.data.Columns)
        self.image = self.get_8bit_image()

    def get_8bit_image(self):
        # Get pixel data as float numbers
        array = self.data.pixel_array.astype('float64')
        # Normalize pixel data to 0-255
        array = (array / array.max()) * 255
        # Create and return image in right mode
        image = Image.fromarray(array)
        converted = image.convert('L')
        return ImageQt.ImageQt(converted)

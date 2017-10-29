import dicom
from PIL import Image


class DicomImage:
    def __init__(self, filename):
        self.filename = filename
        self.dicom_data = dicom.read_file(filename)
        self.size_x = self.dicom_data.Rows
        self.size_y = self.dicom_data.Columns
        self.pixel_spacing_x = self.dicom_data.PixelSpacing[0]
        self.pixel_spacing_y = self.dicom_data.PixelSpacing[1]
        self.image = self.get_8bit_image()

    def get_8bit_image(self):
        # Get pixel data as float numbers
        array = self.dicom_data.pixel_array.astype('float64')
        # Normalize pixel data to 0-255
        array = (array / array.max()) * 255
        # Create and return image
        return Image.fromarray(array)

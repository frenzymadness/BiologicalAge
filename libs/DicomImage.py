import dicom
from PIL import Image, ImageEnhance


class Dicom:
    def __init__(self, filename):
        self.filename = filename
        self.dicom_data = dicom.read_file(filename)
        self.size_x = self.dicom_data.Rows
        self.size_y = self.dicom_data.Columns
        self.pixel_spacing_x = self.dicom_data.PixelSpacing[0]
        self.pixel_spacing_y = self.dicom_data.PixelSpacing[1]
        self.image = self.get_8bit_image()
        self.original_image = self.get_8bit_image()

    def get_8bit_image(self):
        # Get pixel data as float numbers
        array = self.dicom_data.pixel_array.astype('float64')
        # Normalize pixel data to 0-255
        array = (array / array.max()) * 255
        # Create and return image in right mode
        image = Image.fromarray(array)
        return image.convert('L')

    def get_enhanced_image(self, contrast_level, brightness_level):
        contrast = ImageEnhance.Contrast(self.original_image)
        with_contrast = contrast.enhance(contrast_level)
        brightness = ImageEnhance.Brightness(with_contrast)
        return brightness.enhance(brightness_level)

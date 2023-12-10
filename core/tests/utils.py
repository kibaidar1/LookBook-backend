import io

from PIL import Image


def generate_image_bytes(self, file_extension: str = 'png'):
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, file_extension)
    file.name = f'test.{file_extension}'
    file.seek(0)
    return file


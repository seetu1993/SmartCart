import zbar
import zbar.misc
import pathlib

def imread(image_filename):
    from skimage.io import imread as read_image
    image = read_image(image_filename)
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    return image

def detect_code(image_path):
    #barcode_dir = pathlib.Path(__file__).parent / 'barcodes'
    scanner = zbar.Scanner()
    #print('scanning image ' + image.name)
    image_as_numpy_array = imread(image_path)
    results = scanner.scan(image_as_numpy_array)
    if not results:
        return None
    for result in results:
        if "EAN" in result.type:
            return result.data.decode('ascii')

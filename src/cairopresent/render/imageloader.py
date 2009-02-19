"""ImageSurface loading routines."""

import array

import cairo

##
# image load/paint performance
#   png w/ cairo: 0.70/0.06
#   png w/ pil: 1.04/0.08
#   jpg w/ pil: 0.85/0.06
##

def image_surface_with_cairo(filename):
    """Create a Cairo ImageSurface using Cairo's built-in PNG support.
    C{filename} must point to a PNG file.
    
    @type  filename: string
    @param filename: path to PNG file 
    """
    
    return cairo.ImageSurface.create_from_png(filename)
    
def image_surface_with_pil(filename):
    """Create a Cairo ImageSurface using PIL.
    C{filename} must be loadable by PIL.
    
    @type  filename: string
    @param filename: path to image file 
    """
    
    import Image
    
    image = Image.open(filename)
    width, height = image.size
    
    # swap B and R channel
    # TODO: why do we need this?!
    if image.mode == 'RGB':
        r, g, b = image.split()
        image = Image.merge('RGB', (b, g, r))
    image = image.convert('RGBA')
    
    data = array.array('c', image.tostring())
    return cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32,
                                              width, height, width * 4)

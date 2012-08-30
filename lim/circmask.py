"""
PyLunch code review: Circular mask

:Author: Pey Lian Lim

:Organization: Space Telescope Science Institute

"""

# THIRD PARTY
import numpy

def circular_mask(arr_shape, r, x_offset=0, y_offset=0):
    """
    Generate circular mask for 2D image.

    Parameters
    ----------
    arr_shape : tuple of int
        Shape of the array to use the mask.

    r : int
        Radius of the mask in pixels.

    x_offset, y_offset : int or float, optional
        Mask offset relative to image center.

    Returns
    -------
    Numpy indices of the mask, rounded to nearest
    integer.

    References
    ----------
    http://mail.scipy.org/pipermail/numpy-discussion/2011-January/054470.html

    """
    assert len(arr_shape) == 2, 'Image is not 2-D'

    ny, nx = arr_shape
    assert nx > 1 and ny > 1, 'Image is too small'

    assert isinstance(r, (int, long)) and r > 0, 'Radius must be int > 0'

    xcen = numpy.round(0.5 * nx - 0.5 + x_offset).astype('int')
    ycen = numpy.round(0.5 * ny - 0.5 + y_offset).astype('int')

    x1, x2 = xcen - r, xcen + r
    y1, y2 = ycen - r, ycen + r

    assert y1 >= 0 and y2 < ny and x1 >= 0 and x2 < nx, 'Mask falls outside image bounds'

    y, x = numpy.ogrid[-r:r, -r:r]
    i = numpy.where(x**2 + y**2 <= r**2)
    
    a = numpy.zeros(arr_shape).astype('bool')
    a[y1:y2, x1:x2][i] = True

    return numpy.where(a)

if __name__ == '__main__':
    import pylab

    # Make a funny face
    im = numpy.zeros((1000,1000))
    im[ circular_mask(im.shape, 400) ] = 1.0
    im[ circular_mask(im.shape, 10, x_offset=100, y_offset=50) ] = 10.0
    im[ circular_mask(im.shape, 10, x_offset=-100, y_offset=50) ] = 10.0
    im[ circular_mask(im.shape, 50, y_offset=-150) ] = 10.0

    pylab.imshow(im)
    pylab.show()

#!/usr/bin/env python

"""Provides PNG and SVG export routines."""

import os

import cairo

import render


class GraphicsExport(object):
    """Exports slides to graphics files.
    
    B{Abstract. Implementations must override C{render(self)}.}
    """
    
    def __init__(self, slides, filename, geometry):
        """Creates a graphics export object.
        
        @param slides:    The slides to export.
        @type  filename:  string
        @param filename:  Basename (w/o extension). To get I{foo-{0,1,2,3,...}.ext}, supply C{filename="foo"}. Implementation will decide on I{ext}.
        @type  geometry:  tuple
        @param geometry:  (width, height)
        """
        self.slides = slides
        self.filename = filename
        self.width, self.height = geometry
        
    def render(self):
        """Starts rendering the slides."""
        raise NotImplementedError


class SVGExport(GraphicsExport):
    """Exports slides to SVG files."""
    
    def __init__(self, slides, filename="svgfile", geometry=(640, 480)):
        """Creates a SVG export object."""
        GraphicsExport.__init__(self, slides, filename, geometry)
    
    def render(self):
        for index, slide in enumerate(self.slides):
            surface = cairo.SVGSurface("%s-%d.svg" % (self.filename, index),
                                       self.width, self.height)
            cr = cairo.Context(surface)
            render.render_slide(cr, self.width, self.height, slide)


class PNGExport(GraphicsExport):
    """Exports slides to PNG files."""
    
    def __init__(self, slides, filename="pngfile", geometry=(1024, 768)):
        """Creates a PNG export object."""
        GraphicsExport.__init__(self, slides, filename, geometry)
    
    def render(self):
        for index, slide in enumerate(self.slides):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                         self.width, self.height)
            cr = cairo.Context(surface)
            render.render_slide(cr, self.width, self.height, slide)
            surface.write_to_png("%s-%d.png" % (self.filename, index))
            
class PILExport(GraphicsExport):
    """Exports slides through PIL."""
        
    def __init__(self, slides, extension, filename="pilfile", geometry=(1024, 768)):
        """Creates a PIL export object.
        
        @param slides:    The slides to export.
        @type  filename:  string
        @param filename:  Basename (w/o extension). To get I{foo-{0,1,2,3,...}.ext}, supply C{filename="foo"}.
        @type  extension: string
        @param extension: Filename extension. Will decide on image format.
        @type  geometry:  tuple
        @param geometry:  (width, height)
        """
        GraphicsExport.__init__(self, slides, filename, geometry)
        self.extension = extension
    
    def render(self):
        import Image
        
        for index, slide in enumerate(self.slides):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                         self.width, self.height)
            cr = cairo.Context(surface)
            render.render_slide(cr, self.width, self.height, slide)
            
            image = Image.fromstring("RGBA", (self.width, self.height), surface.get_data())
            image.save("%s-%d.%s" % (self.filename, index, self.extension))
    
def main():
    file0 = os.path.expanduser('~/test.png')
    file1 = os.path.expanduser('~/images/stock/computer/161547780_81e990d7f7_o.jpg')
    file2 = os.path.expanduser('~/images/stock/noch_fragen/277386361_13b04e9d98_o.jpg')
    
    png = PNGExport([(file0, "Noch Fragen?"),
                     (file1, "A History of\nComputing Machinery"),
                     (file2, "Noch immer\nFragen?!")]
    )
    png.render()
    
    
    svg = SVGExport([(file0, "Noch Fragen?"),
                     (file1, "A History of\nComputing Machinery"),
                     (file2, "Noch immer\nFragen?!")]
    )
    svg.render()
    
    jpg = PILExport([(file0, "Noch Fragen?"),
                     (file1, "A History of\nComputing Machinery"),
                     (file2, "Noch immer\nFragen?!")],
                    "jpg"
    )
    jpg.render()

if __name__ == '__main__':
    main()
    
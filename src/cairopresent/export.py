#!/usr/bin/env python

"""Provides PDF, PNG, SVG and PIL export routines."""

import os

import cairo

import cairopresent


class Export(object):
    """Exports slides to graphics files.
    
    @attention: Abstract! Implementations must override C{render(self)}.
    """
    
    def __init__(self, presentation, filename, geometry):
        """Creates a graphics export object.
        
        @param presentation: The presentation to export.
        @type  filename:  string
        @param filename:  Basename (w/o extension). To get I{foo-{0,1,2,3,...}.ext}, supply C{filename="foo"}. Implementation will decide on I{ext}.
        @type  geometry:  tuple
        @param geometry:  (width, height)
        """
        self.slides = presentation.slides
        self.renderer = presentation.renderer
        self.filename = filename
        self.width, self.height = geometry
        
    def render(self):
        """Starts rendering the slides."""
        raise NotImplementedError


class PDFExport(Export):
    """Exports slides to a PNG file."""
    
    def __init__(self, presentation, filename="pdffile.pdf", geometry=(1024, 768)):
        """Creates a PDF export object."""
        Export.__init__(self, presentation, filename, geometry)
    
    def render(self):
        surface = cairo.PDFSurface(self.filename, self.width, self.height)
        cr = cairo.Context(surface)
        for slide in self.slides:
            self.renderer.render_slide(cr, self.width, self.height, slide)
            cr.show_page()
    
    
class SVGExport(Export):
    """Exports slides to SVG files."""
    
    def __init__(self, presentation, filename="svgfile", geometry=(640, 480)):
        """Creates a SVG export object."""
        Export.__init__(self, presentation, filename, geometry)
    
    def render(self):
        for index, slide in enumerate(self.slides):
            surface = cairo.SVGSurface("%s-%d.svg" % (self.filename, index),
                                       self.width, self.height)
            cr = cairo.Context(surface)
            self.renderer.render_slide(cr, self.width, self.height, slide)


class PNGExport(Export):
    """Exports slides to PNG files."""
    
    def __init__(self, presentation, filename="pngfile", geometry=(1024, 768)):
        """Creates a PNG export object."""
        Export.__init__(self, presentation, filename, geometry)
    
    def render(self):
        for index, slide in enumerate(self.slides):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                         self.width, self.height)
            cr = cairo.Context(surface)
            self.renderer.render_slide(cr, self.width, self.height, slide)
            surface.write_to_png("%s-%d.png" % (self.filename, index))
            
            
class PILExport(Export):
    """Exports slides through PIL."""
        
    def __init__(self, presentation, extension, filename="pilfile", geometry=(1024, 768)):
        """Creates a PIL export object.
        
        @param slides:    The slides to export.
        @type  filename:  string
        @param filename:  Basename (w/o extension). To get I{foo-{0,1,2,3,...}.ext}, supply C{filename="foo"}.
        @type  extension: string
        @param extension: Filename extension. Will decide on image format.
        @type  geometry:  tuple
        @param geometry:  (width, height)
        """
        Export.__init__(self, presentation, filename, geometry)
        self.extension = extension
    
    def render(self):
        import Image
        
        for index, slide in enumerate(self.slides):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                         self.width, self.height)
            cr = cairo.Context(surface)
            self.renderer.render_slide(cr, self.width, self.height, slide)
            
            image = Image.fromstring("RGBA", (self.width, self.height), surface.get_data())
           
            # swap B and R channel
            # TODO: why do we need this?!
            r, g, b, a = image.split()
            image = Image.merge('RGBA', (b, g, r, a))
    
            image.save("%s-%d.%s" % (self.filename, index, self.extension))
    
    
def main():
    file0 = os.path.expanduser('~/test.png')
    file1 = os.path.expanduser('~/images/stock/computer/161547780_81e990d7f7_o.jpg')
    file2 = os.path.expanduser('~/images/stock/noch_fragen/277386361_13b04e9d98_o.jpg')
    
    slides = [(file0, "Noch Fragen?"),
              (file1, "A History of\nComputing Machinery"),
              (file2, "Noch immer\nFragen?!")]
            
    presentation = cairopresent.render.pz.Presentation(slides)
    
    png = PNGExport(presentation)
    png.render()
    
    # these get really huge :-\
#    svg = SVGExport(presentation)
#    svg.render()
    
    jpg = PILExport(presentation, "jpg")
    jpg.render()
    
    pdf = PDFExport(presentation)
    pdf.render()


if __name__ == '__main__':
    main()
    
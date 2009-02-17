#!/usr/bin/env python

import os

import cairo

import render

class PDFExport(object):
    def __init__(self, slides, filename="pdffile.pdf", geometry=(1024, 768)):
        
        self.slides = slides
        self.filename = filename
        self.width, self.height = geometry
    
    def render(self):
        surface = cairo.PDFSurface(self.filename, self.width, self.height)
        cr = cairo.Context(surface)
        for slide in self.slides:
            render.render_slide(cr, self.width, self.height, slide)
            cr.show_page()
    
def main():
    f0 = os.path.expanduser('~/test.png')
    f1 = os.path.expanduser('~/images/stock/computer/161547780_81e990d7f7_o.jpg')
    f2 = os.path.expanduser('~/images/stock/noch_fragen/277386361_13b04e9d98_o.jpg')
    
    pdf = PDFExport([(f0, "Noch Fragen?"),
                     (f1, "A History of\nComputing Machinery"),
                     (f2, "Noch immer\nFragen?!")]
    )
    pdf.render()

if __name__ == '__main__':
    main()

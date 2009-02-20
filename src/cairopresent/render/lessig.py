"""Lawrance Lessig style Presentation and Renderer."""

import os

import pango
import pangocairo

from cairopresent.helpers import imageloader


class Presentation(object):
    """A presentation for Lessig style rendering.
    
    Slides will have black background, and centered white (or alternatively red) text. 
    """
     
    def __init__(self, filename):
        """Creates a PZ style presentation object.
        
        @type  filename: string
        @param filename: Path to the Presentation.
        """
        
        self.slides = self.parse_file(filename)
        self.renderer = Renderer(os.path.dirname(filename))
        
    def parse_file(self, filename):
        slides = []
        current_slide = ''
        
        f = open(filename)
        open_emph = False
        for line in f:
            if line.startswith('#'):
                continue
            elif line in ('\r\n', '\n') and current_slide:
                slides.append(current_slide)
                current_slide = ''
            else:
                line = line.replace('<', '&lt;')
                line = line.replace('>', '&gt;')
                while '*' in line:
                    if not open_emph:
                        line = line.replace('*', '<span color="#BB0000">', 1)
                    else:
                        line = line.replace('*', '</span>', 1)
                    open_emph = not open_emph
                current_slide += line
        
        if current_slide:
            slides.append(current_slide)
                        
        return slides
        
class Renderer(object):
    """A renderer for Lessig style rendering.
    
    @attention: Don't use directly. This will be used automatically when rendering a C{cairopresent.render.lessig.Presentation}!
    """
    
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def render_slide(self, cr, cr_width, cr_height, slide):
        """Renders the slide C{current_slide} onto the given Cairo context C{cr}."""
        
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.paint()
        
        if slide.startswith('img::'):
            img_filename = slide.split('img::')[-1].strip()
            if not os.path.isabs(img_filename):
                img_filename = os.path.join(self.base_dir, img_filename)
            
            # load image surface
            image_surface = None
            if img_filename == '.png':
                try:
                    # causes MemoryError if filename doesn't point to a PNG
                    image_surface = imageloader.image_surface_with_cairo(img_filename)
                except MemoryError:
                    image_surface = imageloader.image_surface_with_pil(img_filename)
            else:
                image_surface = imageloader.image_surface_with_pil(img_filename)
                
            # get geometry info
            iw, ih = image_surface.get_width(), image_surface.get_height()
            # scale factor and translation to zoom to center of image
            sf = min(float(cr_width) / iw, float(cr_height) / ih)    # scale factor
            tx = (cr_width - sf * iw) / 2    # translate x
            ty = (cr_height - sf * ih) / 2   # translate y
            
            # paint image
            cr.push_group()
            cr.translate(tx, ty)
            cr.scale(sf, sf)
            cr.set_source_surface(image_surface, 0, 0)
            cr.paint()
            cr.pop_group_to_source()
            cr.paint()
            
        else:
            # render some text (w/ pango)
            pc = pangocairo.CairoContext(cr)
            layout = pc.create_layout()
            layout.set_font_description(pango.FontDescription("1942 report %d" % int(cr_height/20.)))
            layout.set_markup(slide)
            layout.set_alignment(pango.ALIGN_CENTER)
            layout.set_spacing(int(1./50 * cr_height * pango.SCALE))
            ink_rect, logical_rect = layout.get_pixel_extents()
            tx, ty, tw, th = logical_rect
            cr.move_to((cr_width - tw)/2, (cr_height - th)/2)
            cr.set_source_rgb(1.0, 1.0, 1.0)
            pc.show_layout(layout)
        
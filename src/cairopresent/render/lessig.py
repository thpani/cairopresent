"""Lawrance Lessig style Presentation and Renderer."""

import pango
import pangocairo


class Presentation(object):
    """A presentation for Lessig style rendering.
    
    Slides will have black background, and centered white (or alternatively red) text. 
    """
     
    def __init__(self, slides):
        """Creates a PZ style presentation object.
        
        @type  slides: list of tuples
        @param slides: A list of tuples given as C{(text, flag)}. If C{flag} is C{True}, render w/ alt color.
        """
        self.slides = slides
        self.renderer = Renderer
        
        
class Renderer(object):
    """A renderer for Lessig style rendering.
    
    @attention: Don't use directly. This will be used automatically when rendering a C{cairopresent.render.lessig.Presentation}!
    """
    
    @classmethod
    def render_slide(cls, cr, cr_width, cr_height, slide):
        """Renders the slide C{current_slide} onto the given Cairo context C{cr}."""
        
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.paint()
        
        # render some text (w/ pango)
        pc = pangocairo.CairoContext(cr)
        layout = pc.create_layout()
        layout.set_font_description(pango.FontDescription("Yanone Kaffeesatz %d" % int(cr_height/10.)))
        layout.set_text(slide[0])
        layout.set_alignment(pango.ALIGN_CENTER)
        layout.set_spacing(int(1./50 * cr_height * pango.SCALE))
        ink_rect, logical_rect = layout.get_pixel_extents()
        tx, ty, tw, th = logical_rect
        cr.move_to((cr_width - tw)/2, (cr_height - th)/2)
        if not slide[1]:
            cr.set_source_rgb(1.0, 1.0, 1.0)
        else:
            cr.set_source_rgb(1.0, 0.0, 0.0)
        pc.show_layout(layout)
        
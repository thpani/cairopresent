import pango
import pangocairo

import imageloader

def render_slide(cr, cr_width, cr_height, current_slide):
    # load image surface
    image_surface = None
    if current_slide[0][-4:].lower() == '.png':
        try:
            # causes MemoryError if filename doesn't point to a PNG
            image_surface = imageloader.image_surface_with_cairo(current_slide[0])
        except:
            image_surface = imageloader.image_surface_with_pil(current_slide[0])
    else:
        image_surface = imageloader.image_surface_with_pil(current_slide[0])
        
    # get geometry info
    iw, ih = image_surface.get_width(), image_surface.get_height()
    # scale factor and translation to zoom to center of image
    sf = max(float(cr_width) / iw, float(cr_height) / ih)    # scale factor
    tx = (cr_width - sf * iw) / 2    # translate x
    ty = (cr_height - sf * ih) / 2    # translate y
    
    # paint image
    cr.push_group()
    cr.translate(tx, ty)
    cr.scale(sf, sf)
    cr.set_source_surface(image_surface, 0, 0)
    cr.paint()
    cr.pop_group_to_source()
    cr.paint()
    
    # render some text (w/ pango)
    pc = pangocairo.CairoContext(cr)
    layout = pc.create_layout()
    layout.set_font_description(pango.FontDescription("Yanone Kaffeesatz Bold %d" % int(cr_height/12.)))
    layout.set_text(current_slide[1])
    layout.set_indent(int(.03 * cr_width * pango.SCALE))
    layout.set_spacing(int(1./60 * cr_height * pango.SCALE))
    ink_rect, logical_rect = layout.get_pixel_extents()
    cr.rectangle(0, int(.06 * cr_height), int(logical_rect[2] + .06 * cr_width), int(logical_rect[3] + .05 * cr_height))
    cr.set_source_rgba(.90, .90, .90, .5)
    cr.fill()
    cr.move_to(0, int(.085 * cr_height)) # rect y_offset + rect_margin/2
    cr.set_source_rgb(0.0, 0.0, 0.0)
    pc.show_layout(layout) 
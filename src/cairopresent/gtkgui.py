#!/usr/bin/env python

"""GTK GUI for CairoPresent."""

import os

import pygtk
pygtk.require('2.0')
import gtk

import cairopresent

class MainWindow(gtk.Window):
    """Main presentation window."""
    
    def __init__(self, presentation):
        gtk.Window.__init__(self)
        
        self.set_title("CairoPresent")
        self.set_icon_from_file('/usr/share/icons/gnome/scalable/mimetypes/x-office-presentation.svg')
        
        self.slides = presentation.slides
        self.current_slide_index = 0
        self.goto_buffer = None
        
        self.renderer = presentation.renderer
        
        self.set_default_size(800, 600)
        self._is_fullscreen = False
        
        self.drawing_area = gtk.DrawingArea()
        self.add(self.drawing_area)
        
        self.connect('destroy', gtk.main_quit)
        self.connect('key_press_event', self.on_key_press)
        self.connect('window_state_event', self.on_window_state)
        self.drawing_area.connect('expose_event', self.expose)
        
        self.show_all()

    def on_key_press(self, win, event):
        """Callback for key-press-event."""
        key = gtk.gdk.keyval_name(event.keyval)
        if key in ('f', 'F', 'F5'):
            if self._is_fullscreen:
                self.unfullscreen()
            else:
                self.fullscreen()
        elif key in ('Right', 'space', 'Page_Down'):
            if self.current_slide_index + 1 < len(self.slides):
                self.current_slide_index += 1
                self.drawing_area.queue_draw()
        elif key in ('Left', 'BackSpace', 'Page_Up'):
            if self.current_slide_index > 0:
                self.current_slide_index -= 1
                self.drawing_area.queue_draw()
        elif key in ('Home'):
            self.current_slide_index = 0
            self.drawing_area.queue_draw()
        elif key in ('End'):
            self.current_slide_index = len(self.slides) - 1
            self.drawing_area.queue_draw()
        elif key in ('Escape'):
            if self._is_fullscreen:
                self.unfullscreen()
            else:
                self.destroy()
        elif key in map(str, range(10)):
            if self.goto_buffer is None:
                self.goto_buffer = key
            else:
                self.goto_buffer += key
        elif key in ('Return', 'g', 'G'):
            if self.goto_buffer is not None:
                target = int(self.goto_buffer)-1
                if 0 <= target < len(self.slides):
                    self.current_slide_index = target
                    self.drawing_area.queue_draw()
                self.goto_buffer = None
        else:
            print key   # TODO
        
        return True
    
    def on_window_state(self, win, event):
        """Callback for window-state-event."""
        self._is_fullscreen = bool(event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN)
    
        return False
    
    def expose(self, drawing_area, event):
        """Callback for expose-event."""
        cr = drawing_area.window.cairo_create()
        cr_width, cr_height = drawing_area.window.get_size()
        current_slide = self.slides[self.current_slide_index]
        self.renderer.render_slide(cr, cr_width, cr_height, current_slide)
        
        return False
    
def main():
    file0 = os.path.expanduser('~/test.png')
    file1 = os.path.expanduser('~/images/stock/computer/161547780_81e990d7f7_o.jpg')
    file2 = os.path.expanduser('~/images/stock/noch_fragen/277386361_13b04e9d98_o.jpg')
    
    slides = [(file0, "Noch Fragen?"),
              (file1, "A History of\nComputing Machinery"),
              (file2, "Noch immer\nFragen?!")]
    
    presentation = cairopresent.render.thp.Presentation(slides)
    
    MainWindow(presentation)
    gtk.main()
    
    presentation = cairopresent.render.lessig.Presentation('../../examples/lessig/lessig.txt')
    
    MainWindow(presentation)
    gtk.main()

if __name__ == '__main__':
    main()

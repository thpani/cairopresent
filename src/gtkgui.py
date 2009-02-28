#!/usr/bin/env python

"""GTK GUI for CairoPresent."""

import os
from threading import Thread

import cairo
import pygtk
pygtk.require('2.0')
import gobject
import gtk

import cairopresent
from cairopresent.helpers.resources import *


TRANSITION_TIMEOUT = 50 # ms steps between fade gradients
TRANSITION_STEP = 0.2  # alpha delta between fade gradients

gtk.gdk.threads_init()

class MainWindow(gtk.Window):
    """Main presentation window."""
    
    def __init__(self, presentation):
        gtk.Window.__init__(self)
        
        self.set_title("CairoPresent")
        self.set_icon_from_file(get_res('icon.png'))
        
        self.presentation = presentation
        self.slides = presentation.slides
        self.current_slide_index = 0
        self.goto_buffer = None

        self.in_transition = 0  # 1 to fade in; -1 to fade out
        self.transition_alpha = 0
        self.transition_next_index = None

        self.cache = {}
        
        self.renderer = presentation.renderer
        
        self.set_default_size(800, 600)
        self._is_fullscreen = False
        
        self.drawing_area = gtk.DrawingArea()
        self.add(self.drawing_area)
        
        self.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK)

        self.connect('destroy', gtk.main_quit)
        self.connect('button_press_event', self.on_button_press)
        self.connect('key_press_event', self.on_key_press)
        self.connect('window_state_event', self.on_window_state)
        self.drawing_area.connect('expose_event', self.expose)
        
        self.show_all()

    def on_button_press(self, win, event):
        x, y, state = event.window.get_pointer()
        if state & gtk.gdk.BUTTON1_MASK:
            self.transition()

    def on_key_press(self, win, event):
        """Callback for key-press-event."""
        key = gtk.gdk.keyval_name(event.keyval)
        if key in ('f', 'F', 'F5'):
            if self._is_fullscreen:
                self.unfullscreen()
            else:
                self.fullscreen()
        elif key in ('Right', 'space', 'Page_Down'):
            self.transition()
        elif key in ('Left', 'BackSpace', 'Page_Up'):
            self.transition(-1)
        elif key in ('Home'):
            self.transition(-self.current_slide_index)
        elif key in ('End'):
            self.transition(len(self.slides) - self.current_slide_index - 1)
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
                self.transition(target - self.current_slide_index)
                self.goto_buffer = None
        else:
            print key   # TODO
        
        return True
    
    def on_window_state(self, win, event):
        """Callback for window-state-event."""
        if self._is_fullscreen != bool(event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN):
            self._is_fullscreen = bool(event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN)
            self.invalidate_cache()
    
        return False
    
    def expose(self, drawing_area, event):
        """Callback for expose-event."""

        cr = drawing_area.window.cairo_create()
        cr_width, cr_height = drawing_area.window.get_size()

        self.render_into_cache(self.current_slide_index)
        current_slide = self.cache[self.current_slide_index]

        cr = drawing_area.window.cairo_create()
        cr.set_source_surface(current_slide)
        cr.paint()

        if self.in_transition:
            cr.set_source_rgba(0, 0, 0, self.transition_alpha)
            cr.paint()
       
        return False

    def invalidate_cache(self):
        self.cache = {}

    def render_into_cache(self, slide_index):
        if slide_index in self.cache:
            return

        cr_width, cr_height = self.drawing_area.window.get_size()
        buffer = cairo.ImageSurface(cairo.FORMAT_ARGB32, cr_width, cr_height)
        cr = cairo.Context(buffer)
        cr_width, cr_height = buffer.get_width(), buffer.get_height()
        current_slide_desc = self.slides[slide_index]
        self.renderer.render_slide(cr, cr_width, cr_height,
                                   current_slide_desc)
        self.cache[slide_index] = buffer

    def transition(self, direction=1):
        if direction == 0:
            return True

        if len(self.slides) <= self.current_slide_index + direction or \
           self.current_slide_index + direction < 0:
            return False

        if not self.presentation.show_transition(self.current_slide_index,
                self.current_slide_index + direction):
            self.current_slide_index += direction
            self.drawing_area.queue_draw()
            return True

        self.in_transition = 1
        self.transition_alpha = 0
        self.transition_next_index = self.current_slide_index + direction
        gobject.timeout_add(TRANSITION_TIMEOUT, self.transition_callback)
        return True

    def transition_callback(self):
        if self.in_transition == -1 and self.transition_alpha < 0:
            # fade finished
            self.in_transition = 0  # 1 to fade in; -1 to fade out
            self.transition_alpha = 0
            self.transition_next_index = None
            return False

        if self.transition_alpha > 1.1:
            # u-turn fade-out -> fade-in
            self.in_transition = -self.in_transition
            self.current_slide_index = self.transition_next_index
        self.transition_alpha += TRANSITION_STEP * self.in_transition

        self.drawing_area.queue_draw()
        return True # return True to continue calling timeout

def main():
    file0 = os.path.join(cairopresent.helpers.resources.EXAMPLE_PATH, 'thp', 'test.png')
    file1 = os.path.join(cairopresent.helpers.resources.EXAMPLE_PATH, 'thp', '161547780_81e990d7f7_o.jpg')
    file2 = os.path.join(cairopresent.helpers.resources.EXAMPLE_PATH, 'thp', '277386361_13b04e9d98_o.jpg')
    
    slides = [(file0, "Noch Fragen?"),
              (file1, "A History of\nComputing Machinery"),
              (file2, "Noch immer\nFragen?!")]
    
    presentation = cairopresent.render.thp.Presentation(slides)
    
    w = MainWindow(presentation)
    gtk.main()
    
    presentation = cairopresent.render.lessig.Presentation(get_example('lessig.txt'))
    
    w = MainWindow(presentation)
    gtk.main()

if __name__ == '__main__':
    main()

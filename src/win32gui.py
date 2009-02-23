"""Win32 GUI for CairoPresent."""

import os
import sys

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui
import win32con

import cairo

import cairopresent
from cairopresent.helpers.resources import *

LPSZ_CLASS_NAME = "CairoPresentMainWindow"

class MainWindow(object):
    def __init__(self, presentation):

        self.slides = presentation.slides
        self.current_slide_index = 0
        self.goto_buffer = None
        
        self.renderer = presentation.renderer
        
        message_map = {
                win32con.WM_CLOSE: self.OnClose,
                win32con.WM_DESTROY: self.OnDestroy,
                win32con.WM_PAINT: self.OnPaint,
                win32con.WM_SETCURSOR: self.OnCursor,
                win32con.WM_ERASEBKGND: self.OnBackgroundErase,
                win32con.WM_LBUTTONDOWN: self.OnClick,
                win32con.WM_KEYUP: self.OnKey,
                win32con.WM_CHAR: self.OnChar,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = LPSZ_CLASS_NAME
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        class_atom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_THICKFRAME | win32con.WS_MAXIMIZEBOX | win32con.WS_MINIMIZEBOX | win32con.WS_SYSMENU | win32con.WS_VISIBLE
        hwnd = win32gui.CreateWindowEx(0, class_atom, "CairoPresent", style, 0, 0, 1024, 768, 0, 0, 0, None)

    def OnKey(self, hWnd, msg, wParam, lparam):
        if wParam == win32con.VK_RIGHT:
            if self.current_slide_index + 1 < len(self.slides):
                self.current_slide_index += 1
                win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE)
        elif wParam == win32con.VK_LEFT:
            if self.current_slide_index > 0:
                self.current_slide_index -= 1
                win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE)
                
    def OnClick(self, hWnd, msg, wparam, lparam):
        if self.current_slide_index + 1 < len(self.slides):
            self.current_slide_index += 1
            win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE)

    def OnChar(self, hWnd, msg, wparam, lparam):
        key = chr(wparam)
        if key == ' ':
            if self.current_slide_index + 1 < len(self.slides):
                self.current_slide_index += 1
                win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE)
        elif key in map(str, range(10)):
            if self.goto_buffer is None:
                self.goto_buffer = key
            else:
                self.goto_buffer += key
        elif key in ('\r', 'g', 'G'):
            if self.goto_buffer is not None:
                target = int(self.goto_buffer)-1
                if 0 <= target < len(self.slides):
                    self.current_slide_index = target
                win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE)
                self.goto_buffer = None
        else:
            print key   # TODO

    def Render(self):
        try:
            InvalidateRect(self.hwnd, None, True)
            return True
        except:
            return False

    def OnPaint(self, hWnd, msg, wparam, lparam):
        hdc, ps = win32gui.BeginPaint(hWnd)
        left, top, right, bottom = win32gui.GetClientRect(hWnd)

        cr_width = right - left
        cr_height = bottom - top
        x = left
        y = top

        _buffer = win32gui.CreateCompatibleDC(hdc)
        #Double Buffer Stage 1
        hBitmap = win32gui.CreateCompatibleBitmap(hdc, cr_width, cr_height)
        hOldBitmap = win32gui.SelectObject(_buffer, hBitmap )

        surf = cairo.Win32Surface(_buffer)
        cr = cairo.Context(surf)

        # call renderer here
        current_slide = self.slides[self.current_slide_index]
        self.renderer.render_slide(cr, cr_width, cr_height, current_slide)

        surf.finish()

        win32gui.BitBlt(hdc,0, 0, cr_width,  cr_height,
          _buffer, x, y, win32con.SRCCOPY)

        win32gui.SelectObject( _buffer, hOldBitmap ) 
        win32gui.DeleteObject( hBitmap ) 
        win32gui.DeleteDC( _buffer )               

        win32gui.EndPaint(hWnd,ps)

    def OnCursor(self, hwnd, msg, wparam, lparam):
        cur_normal = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        win32gui.SetCursor(cur_normal)

    def OnBackgroundErase(self, hwnd, msg, wparam, lparam):
        return False

    def OnClose(self, hwnd, msg, wparam, lparam):
        win32gui.DestroyWindow(hwnd)
        win32gui.UnregisterClass(LPSZ_CLASS_NAME, None)
        
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        win32gui.PostQuitMessage(0) # Terminate the app.
            
def main():
    file0 = os.path.join(cairopresent.helpers.resources.EXAMPLE_PATH, 'thp', 'test.png')
    file1 = os.path.join(cairopresent.helpers.resources.EXAMPLE_PATH, 'thp', '161547780_81e990d7f7_o.jpg')
    file2 = os.path.join(cairopresent.helpers.resources.EXAMPLE_PATH, 'thp', '277386361_13b04e9d98_o.jpg')
    
    slides = [(file0, "Noch Fragen?"),
              (file1, "A History of\nComputing Machinery"),
              (file2, "Noch immer\nFragen?!")]
    
    presentation = cairopresent.render.thp.Presentation(slides)
    
    MainWindow(presentation)
    win32gui.PumpMessages()
    
    presentation = cairopresent.render.lessig.Presentation(get_example('lessig.txt'))
    
    MainWindow(presentation)
    win32gui.PumpMessages()

if __name__ == '__main__':
    main()
    

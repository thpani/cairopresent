import os
import glob

from distutils.core import setup
import py2exe

setup(
    name = "CairoPresent",
    description = "A Cairo-based slide renderer.",
    version = "0.0.1",
    windows = ['gtkgui.py'],
    options = { 'py2exe' : { 'includes' : ['atk'] } },
    data_files=[
        ('.', ['../res/icon.png']),
        ('etc/gtk-2.0', [os.path.expanduser('~/gtk/etc/gtk-2.0/gdk-pixbuf.loaders')]),
        ('lib/gtk-2.0/2.10.0/loaders', [os.path.expanduser('~/gtk/lib/gtk-2.0/2.10.0/loaders/libpixbufloader-png.dll')]),
        ],
)

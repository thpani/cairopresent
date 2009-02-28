import glob
import platform
import os

from distutils.core import setup

NAME = 'CairoPresent'
DESC = 'A Cairo-based slide renderer.'
VERSION = '0.0.1'
URL = 'http://pani.webhop.org/cairopresent/preview.html'
AUTHOR = 'Thomas Pani'
AUTHOR_EMAIL = 'thomas.pani@gmail.com'

if platform.system() == 'Windows':
    import py2exe

    setup(
        name = NAME,
        description = DESC,
        version = VERSION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        url = URL,
        windows = ['gtkgui.py'],
        options = { 'py2exe' : { 'includes' : ['atk'] } },
        data_files=[
            ('.', ['../res/icon.png']),
            ('etc/gtk-2.0', [os.path.expanduser('~/gtk/etc/gtk-2.0/gdk-pixbuf.loaders')]),
            ('lib/gtk-2.0/2.10.0/loaders', [os.path.expanduser('~/gtk/lib/gtk-2.0/2.10.0/loaders/libpixbufloader-png.dll')]),
            ],
    )

else:
    setup(
        name = NAME,
        description = DESC,
        version = VERSION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        url = URL,
        packages = ['cairopresent', 'cairopresent.helpers',
        'cairopresent.render'],
        data_files = [('share/pixmaps/cairopresent', ['../res/icon.png'])],
        scripts = ['gtkgui.py', 'export.py']
        )

import os.path
import sys

import cairopresent

RES_PATH = os.path.normpath(os.path.join(cairopresent.__file__, '..', '..', '..', 'res'))
EXAMPLE_PATH = os.path.normpath(os.path.join(cairopresent.__file__, '..', '..', '..', 'examples'))

if hasattr(sys, "frozen") and sys.frozen == "windows_exe":
    RES_PATH = os.path.dirname(sys.executable)
    EXAMPLE_PATH = os.path.dirname(sys.executable)

def get_res(filename):
    return os.path.join(RES_PATH, filename)

def get_example(filename):
    return os.path.join(EXAMPLE_PATH, os.path.splitext(filename)[0], filename)

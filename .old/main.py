import mmap
import ctypes
import time
import sys
import os
from stinttracker.update_stint import update_stint
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize
from window import MainWindow, FONT, get_fonts, OverlayScrollStyle

from pyLMUSharedMemory import lmu_data
from helpers import resource_path

app = QApplication(sys.argv)

app.setStyle('Fusion')

app_icon = QIcon()
app_icon.addFile(resource_path('favicon/favicon-16x16.png'), QSize(16,16))
app_icon.addFile(resource_path('favicon/favicon-24x24.png'), QSize(24,24))
app_icon.addFile(resource_path('favicon/favicon-32x32.png'), QSize(32,32))
app_icon.addFile(resource_path('favicon/favicon-48x48.png'), QSize(48,48))
app_icon.addFile(resource_path('favicon/favicon-256x256.png'), QSize(256,256))
app.setWindowIcon(app_icon)

font = get_fonts(FONT.text_small)

# Set as default font for the app
app.setFont(font)

window = MainWindow()
window.show()



# Open the qss styles file and read in the CSS-like styling code
with open(resource_path('styles/main.qss'), 'r') as f:
    style = f.read()

    # Set the stylesheet of the application
    app.setStyleSheet(style)

# app.setStyle(OverlayScrollStyle())
app.exec()

# Open shared memory
shared_mem = mmap.mmap(
    fileno=0,
    length=ctypes.sizeof(lmu_data.LMUObjectOut),
    tagname=lmu_data.LMUConstants.LMU_SHARED_MEMORY_FILE
)

lmu = lmu_data.LMUObjectOut.from_buffer(shared_mem)

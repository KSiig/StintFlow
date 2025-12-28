import mmap
import ctypes
import time
import sys
from stinttracker.update_stint import update_stint
from PyQt6.QtWidgets import QApplication, QMainWindow
from window import MainWindow

from pyLMUSharedMemory import lmu_data

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

# Open shared memory
shared_mem = mmap.mmap(
    fileno=0,
    length=ctypes.sizeof(lmu_data.LMUObjectOut),
    tagname=lmu_data.LMUConstants.LMU_SHARED_MEMORY_FILE
)

lmu = lmu_data.LMUObjectOut.from_buffer(shared_mem)

import sys
from pyLMUSharedMemory import lmu_data
from stinttracker.update_stint import update_stint
import mmap
import ctypes
import time
import sys

# Open shared memory
shared_mem = mmap.mmap(
    fileno=0,
    length=ctypes.sizeof(lmu_data.LMUObjectOut),
    tagname=lmu_data.LMUConstants.LMU_SHARED_MEMORY_FILE
)

lmu = lmu_data.LMUObjectOut.from_buffer(shared_mem)

try:
    session_id = sys.argv[1]
    drivers = sys.argv[2].split(',')
    tracking_data = {
        "session_id": session_id,
        "drivers": drivers
    }
    print("Tracking session:", session_id)
    while True:
        update_stint(lmu.telemetry, lmu.scoring, tracking_data)
        hz_interval = 1
        time.sleep(1/hz_interval)


except KeyboardInterrupt:
    print("Exiting...")
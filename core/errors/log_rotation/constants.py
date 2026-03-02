"""Constants shared by log rotation helpers."""

import re

HEADER_PREFIX = "=== StintFlow session started:"
HEADER_FORMAT = f"{HEADER_PREFIX} %Y-%m-%d %H:%M:%S ==="
HEADER_PATTERN = re.compile(
    rf"^{re.escape(HEADER_PREFIX)} (?P<ts>\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}) ===$"
)

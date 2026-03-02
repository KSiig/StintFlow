"""Validate MongoDB host string format."""


def _validate_host(host: str) -> bool:
    """Return True if *host* is empty (URI) or hostname[:port] shaped."""
    if not host:
        return False

    if ":" not in host:
        return True

    parts = host.split(":")
    if len(parts) != 2:
        return False

    try:
        port = int(parts[1])
        return 1 <= port <= 65535
    except ValueError:
        return False

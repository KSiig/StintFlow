from typing import Any, Mapping

def _wheel_data_from_mgmt(mgmt: Mapping[str, Any], index: int) -> Mapping[str, Any]:
    wheel_info = mgmt.get("wheelInfo")
    if not isinstance(wheel_info, Mapping):
        raise KeyError("wheelInfo missing or invalid")

    wheel_locs = wheel_info.get("wheelLocs")
    if not isinstance(wheel_locs, (list, tuple)):
        raise KeyError("wheelLocs missing or invalid")

    try:
        data = wheel_locs[index]
    except Exception as exc:
        raise IndexError(f"wheel index access failed: {exc}") from exc

    if not isinstance(data, Mapping):
        raise KeyError("wheel data is not a mapping")

    return data
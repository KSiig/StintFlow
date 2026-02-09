"""
Get the path to the log file for error logging.

The log file is placed in a user-accessible location so non-technical users
can easily find and send it for debugging purposes.
"""

from pathlib import Path


def get_log_file_path():
    """
    Get the path to the application log file.
    
    Returns:
        Path: Path object pointing to the log file location.
        
    The log file is placed in the user's home directory under a 'StintFlow' folder
    to make it easily accessible for non-technical users.
    """
    home_dir = Path.home()
    log_dir = home_dir / "StintFlow"
    
    # Create directory if it doesn't exist
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "stintflow.log"
    return log_file

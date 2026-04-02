import os
import json
import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

def read_json(filepath: str) -> Dict[str, Any]:
    """Read JSON file and return its content as a dictionary."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {filepath}")
        raise

def write_json(data: Dict[str, Any], filepath: str, indent: int = 4) -> None:
    """Write dictionary to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)
    except PermissionError:
        logger.error(f"Permission denied when writing to: {filepath}")
        raise

def ensure_dir_exists(dirpath: str) -> None:
    """Ensure directory exists; create if it doesn't."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        logger.info(f"Created directory: {dirpath}")

def get_filepaths_in_dir(dirpath: str, extensions: Optional[List[str]] = None) -> List[str]:
    """Get list of filepaths in directory, optionally filtered by extensions."""
    if not os.path.isdir(dirpath):
        logger.error(f"Directory not found: {dirpath}")
        raise FileNotFoundError(f"Directory not found: {dirpath}")

    filepaths = []
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        if os.path.isfile(filepath):
            if extensions is None or any(filename.endswith(ext) for ext in extensions):
                filepaths.append(filepath)
    return filepaths

def setup_logging(log_file: Optional[str] = None, level: int = logging.INFO) -> None:
    """Configure logging to console and optionally to a file."""
    handlers = [logging.StreamHandler()]
    if log_file is not None:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
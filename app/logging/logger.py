import logging
import os
from datetime import datetime

_logging_configured = False

def setup_logging(level=logging.INFO):
    """
    Configure logging to write to a timestamped log file in the logs directory.
    This function is idempotent - calling it multiple times won't create duplicate handlers.
    
    Args:
        level: Logging level (default: logging.INFO)
    """
    global _logging_configured
    
    if _logging_configured:
        return
    
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    log_file_path = os.path.join(logs_dir, log_file)
    
    logging.basicConfig(
        filename=log_file_path,
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=level,
        force=True  
    )
    
    _logging_configured = True
    return log_file_path

def get_logger(name=None):
    """
    Get a logger instance. Automatically sets up logging if not already configured.
    
    Args:
        name: Logger name (default: None, uses root logger)
    
    Returns:
        logging.Logger instance
    """
    if not _logging_configured:
        setup_logging()
    return logging.getLogger(name)


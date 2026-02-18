import sys
import os
from typing import Optional, Tuple, Any

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

try:
    from app.logging.logger import get_logger
except ImportError:
    import logging
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger(__name__)

class NetworkSecurityException(Exception):
    def __init__(self, error_message: str, error_detail: Optional[Tuple[type, BaseException, Any]] = None):
        """
        Custom exception for network security application.
        
        Args:
            error_message: Error message string
            error_detail: Tuple from sys.exc_info() containing (type, value, traceback)
        """
        self.error_message = error_message
        
        if error_detail is None:
            error_detail = sys.exc_info()
        
        _, _, exc_tb = error_detail
        
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None
    
    def __str__(self):
        if self.file_name and self.lineno:
            return f"Error occurred in python script name [{self.file_name}] line number [{self.lineno}] error message: [{self.error_message}]"
        return f"Error message: [{self.error_message}]"

if __name__ == "__main__":
    try:
        logger.info("Dividing by zero")
        a = 1 / 0
    except Exception as e:
        logger.info("Error occurred in main function")
        raise NetworkSecurityException(str(e), sys.exc_info())

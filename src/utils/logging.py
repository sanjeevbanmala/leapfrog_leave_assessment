""" Logging utility module. """

import logging

logging.basicConfig(filename='streamlit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
                    
def get_logger(name=None):
    """Get logger instance."""
    return logging.getLogger(name)

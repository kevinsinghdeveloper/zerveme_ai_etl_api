import json
import logging
import os
import io
from datetime import datetime
from typing import Dict, Any

class Utility:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set default logging level to DEBUG

    if not logger.hasHandlers():
        # Create console handler and set level to INFO
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create file handler and set level to DEBUG
        os.makedirs('logs', exist_ok=True)
        log_filename = f"logs/app_{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add formatter to handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    @staticmethod
    def log(message: str) -> None:
        Utility.logger.info(message)

    @staticmethod
    def debug_log(message: str) -> None:
        Utility.logger.debug(message)

    @staticmethod
    def warning_log(message: str) -> None:
        Utility.logger.warning(message)

    @staticmethod
    def error_log(message: str) -> None:
        Utility.logger.error(message)

    @staticmethod
    def critical_log(message: str) -> None:
        Utility.logger.critical(message)

    @staticmethod
    def read_in_json_file(json_path: str) -> Dict[str, Any]:
        try:
            with open(json_path, 'r') as file:
                content = file.read()
                config = json.loads(content)
                return config
        except json.JSONDecodeError as e:
            Utility.error_log(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno}")
            Utility.error_log(f"Problematic JSON content: {content}")
        except FileNotFoundError:
            Utility.error_log(f"File not found: {json_path}")
            return None
        except Exception as e:
            Utility.error_log(f"An error occurred: {e}")
        raise

    @staticmethod
    def write_dict_to_json_file(data: dict, file_path: str):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            Utility.log(f"Dictionary successfully written to {file_path}")
        except Exception as e:
            Utility.error_log(f"An error occurred while writing to the JSON file: {e}")

    @staticmethod
    def read_image(image_path: str) -> bytes:
        try:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
                Utility.log(f"Image read successfully from {image_path}.")
                return content
        except FileNotFoundError:
            Utility.error_log(f"Image file not found: {image_path}")
            raise
        except Exception as e:
            Utility.error_log(f"Failed to read image file: {e}")
            raise

    @staticmethod
    def trim_spaces(input_string):
        # Split the string into words and join them with a single space
        trimmed_string = ' '.join(input_string.split())
        return trimmed_string

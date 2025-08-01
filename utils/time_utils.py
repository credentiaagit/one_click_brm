from datetime import datetime
import time

# Customer imports
from app import func_logger, app_logger

#Converts date strings to epoch time and fetches current time, with full logging support.
class DateToEpochConverter:                    
    def __init__(self):
        return

    # Convert date string (YYYY-MM-DD HH:MM:SS) to epoch timestamp.
    def convert_to_epoch(self, date_string):     
        try:
            dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            epoch_time = int(time.mktime(dt.timetuple()))
            func_logger.info("convert_to_epoch", extra={ 'input_data': date_string, 'output_data': str(epoch_time) })
            return epoch_time
        except ValueError:
            msg = "Invalid format! Use YYYY-MM-DD HH:MM:SS"
            app_logger.error(f"{msg} - {date_string}")
            return msg

    # Get the current system time in a formatted string.
    def get_current_time(self):                   
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_logger.info("get_current_time", extra={ 'input_data': None, 'output_data': current_time })
            return current_time
        except Exception as e:
            app_logger.error(f"Error while get_current_time()" + str(e))
            return str(e)



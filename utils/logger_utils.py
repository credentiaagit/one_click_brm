import logging
import os

def setup_loggers(log_dir, app_log_filename, log_level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)

    # Common formatters
    simple_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s | Input: %(input_data)s | Output: %(output_data)s'
    )

    # === Application Logger ===
    app_logger = logging.getLogger('appLogger')
    if not app_logger.handlers:
        app_log_path = os.path.join(log_dir, app_log_filename)
        app_handler = logging.FileHandler(app_log_path)
        app_handler.setFormatter(simple_formatter)
        app_logger.setLevel(log_level)
        app_logger.addHandler(app_handler)
        app_logger.propagate = False

    # === Functional Logger ===
    func_logger = logging.getLogger('funcLogger')
    if not func_logger.handlers:
        func_log_path = os.path.join(log_dir, app_log_filename)
        func_handler = logging.FileHandler(func_log_path)
        func_handler.setFormatter(detailed_formatter)
        func_logger.setLevel(log_level)
        func_logger.addHandler(func_handler)
        func_logger.propagate = False

    return app_logger, func_logger


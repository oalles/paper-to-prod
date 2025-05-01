import logging
import os

def setup_logger(session_path, name="paper_to_prod", external_hook=None):
    log_dir = os.path.join(session_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "run.log")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(fh)
    # Hook externo opcional
    if external_hook:
        class ExternalHandler(logging.Handler):
            def emit(self, record):
                log_entry = self.format(record)
                external_hook(log_entry, record.levelname)
        eh = ExternalHandler()
        eh.setLevel(logging.INFO)
        eh.setFormatter(formatter)
        logger.addHandler(eh)
    return logger

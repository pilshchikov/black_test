import logging
from logging.handlers import RotatingFileHandler
import signal
import threading
import time
from datetime import datetime

# Configure logger with rotating file handler
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = "application.log"
handler = RotatingFileHandler(
    log_file, mode="a", maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None, delay=0
)
handler.setFormatter(log_formatter)
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Global flag to control the running of the thread
run_thread = True


def handle_signal_received(signal, frame):
    global run_thread
    run_thread = False
    logger.info("Signal received, preparing to exit...")


def time_since_start(start_time):
    """Calculates time elapsed since start_time and formats the output."""
    now = datetime.now()
    elapsed_time = now - start_time
    return elapsed_time.total_seconds()


def continuously_write_time(start_time):
    """Function to run in a thread, continuously writing elapsed time."""
    while run_thread:
        elapsed_seconds = time_since_start(start_time)
        logger.info(f"Seconds since start: {elapsed_seconds:.2f}")
        time.sleep(1)
    total_time = time_since_start(start_time)
    logger.info(f"Total elapsed time: {total_time:.2f} seconds.")


def main():
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    start_time = datetime.now()
    logger.info("Script started.")

    # Thread to update time
    thread = threading.Thread(target=continuously_write_time, args=(start_time,))
    thread.start()

    # Wait for the thread to finish
    while thread.is_alive():
        try:
            thread.join(timeout=1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received.")
            global run_thread
            run_thread = False
            break


if __name__ == "__main__":
    main()

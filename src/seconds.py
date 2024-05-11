import time
import threading
import logging
import os
import signal
import sys
from datetime import datetime, timedelta

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global flag to control the running of the thread
run_thread = True

def handle_signal_received(signum, frame):
    global run_thread
    run_thread = False
    logging.info("Signal received, preparing to exit...")

def time_since_start(start_time, format_string="%Y-%m-%d %H:%M:%S"):
    """Calculates time elapsed since start_time and formats the output."""
    now = datetime.now()
    elapsed_time = now - start_time
    return elapsed_time.total_seconds()

def continuously_write_time(start_time):
    """Function to run in a thread, continuously writing elapsed time."""
    while run_thread:
        elapsed_seconds = time_since_start(start_time)
        logging.info(f"Seconds since start: {elapsed_seconds:.2f}")
        time.sleep(1)
    total_time = time_since_start(start_time)
    logging.info(f"Total elapsed time: {total_time:.2f} seconds.")

def main():
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal_received)
    signal.signal(signal.SIGTERM, handle_signal_received)

    start_time = datetime.now()
    logging.info("Script started.")

    # Thread to update time
    thread = threading.Thread(target=continuously_write_time, args=(start_time,))
    thread.start()

    # Wait for the thread to finish
    while thread.is_alive():
        try:
            thread.join(timeout=1)
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received.")
            global run_thread
            run_thread = False
            break

if __name__ == "__main__":
    main()

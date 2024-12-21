import psutil
import logging
import time


class Monitor:
    """
    Monitors system performance and application health.
    """

    def __init__(self, check_interval=10):
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def get_cpu_usage(self):
        """
        Get current CPU usage percentage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        self.logger.info(f"CPU usage: {cpu_usage}%")
        return cpu_usage

    def get_memory_usage(self):
        """
        Get current memory usage.
        """
        memory_info = psutil.virtual_memory()
        self.logger.info(f"Memory usage: {memory_info.percent}%")
        return memory_info.percent

    def log_process_stats(self, process_name):
        """
        Log resource usage of a specific process.
        """
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if process_name in proc.info['name']:
                self.logger.info(f"Process {proc.info['name']} (PID: {proc.info['pid']}):")
                self.logger.info(f"CPU: {proc.info['cpu_percent']}%, Memory: {proc.info['memory_percent']}%")
                return proc.info

    def monitor(self):
        """
        Continuously monitor system and process performance.
        """
        self.logger.info("Starting monitoring...")
        try:
            while True:
                self.get_cpu_usage()
                self.get_memory_usage()
                self.log_process_stats("python")  # Replace with your process name
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped.")


if __name__ == "__main__":
    monitor = Monitor()
    monitor.monitor()
import subprocess


def _execute_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing command: {e}"


class SystemMonitor:
    def __init__(self):
        pass

    def get_cpu_load(self):
        return _execute_command('top -bn1 | grep "Cpu(s)"')

    def get_memory_usage(self):
        return _execute_command('free -m')

    def get_disk_usage(self):
        return _execute_command('df -h')


def get_status():
    monitor = SystemMonitor()

    cpu_load = monitor.get_cpu_load()
    memory_usage = monitor.get_memory_usage()
    disk_usage = monitor.get_disk_usage()

    status = (
        f"CPU load: <code>{cpu_load}</code>\n\n"
        f"Memory usage: <code>{memory_usage}</code>\n\n"
        f"Disk usage: <code>{disk_usage}</code>\n"
    )

    return status
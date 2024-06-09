import subprocess
from datetime import datetime

from tgbot.config import load_config

devices = load_config(".env").misc.ip

device = {"39": devices[0], "68": devices[1]}

status = {ip: {'reachable': None, 'last_change': None} for ip in device}


def ping_ip(ip):
    try:
        output = subprocess.run(["ping", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output.returncode == 0
    except Exception as e:
        print(f"Error pinging {ip}: {e}")
        return False


def check_ips():
    changes = {}
    for name, ip in device.items():
        reachable = ping_ip(ip)
        last_status = status[name]['reachable']

        if reachable != last_status:
            current_time = datetime.now()
            if last_status is not None:
                duration = current_time - status[name]['last_change']
                if reachable:
                    changes[name] = {'status': 'в мережі ⚡\n\nЧас недоступності:', 'duration': duration}
                else:
                    changes[name] = {'status': 'більше недоступний 🚫\n\nЧас доступності:', 'duration': duration}
            else:
                if reachable:
                    changes[name] = {'status': 'в мережі ⚡', 'duration': None}
                else:
                    changes[name] = {'status': 'недоступний 🚫', 'duration': None}

            status[name]['reachable'] = reachable
            status[name]['last_change'] = current_time

    return changes
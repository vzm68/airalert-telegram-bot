import asyncio
import logging
import subprocess
from datetime import datetime

from tgbot.config import load_config

logger = logging.getLogger(__name__)

devices = load_config(".env").misc.ip

device = {"39": devices[0], "68": devices[1]}

status = {ip: {'reachable': None, 'last_change': None} for ip in device}


async def ping_ip(ip):
    try:
        output = await asyncio.create_subprocess_exec(
            'ping', '-c', '4', ip,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await output.communicate()
        return output.returncode == 0
    except Exception as e:
        logger.error(f"Error pinging {ip}: {e}")
        return False


async def check_ips():
    changes = {}
    for name, ip in device.items():
        reachable = await ping_ip(ip)
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
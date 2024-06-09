import tinytuya
from tgbot.config import load_config

tuya_access_id = load_config(".env").misc.tuya_id
tuya_access_key = load_config(".env").misc.tuya_key

# Make connection to Tuya API
c = tinytuya.Cloud(
        apiRegion="eu",
        apiKey=tuya_access_id,
        apiSecret=tuya_access_key)

# No secret, just ids
devices = {"68 Rest Room": "bfb1a7895a12867af0uusb",
           "68 Balcony": "bfe1856bd08d9af9d38mau",
           "39 Indoor": "bf70f3538cf3798dab1hdr",
           "39 kitchen": "bf3332e7a109148993aykc"}

# Track and identify devices by location, can be changed at will
device_locations = [
    ("68, Спальня", "68 Rest Room"),
    ("68, Балкон", "68 Balcony"),
    ("39, Коридор", "39 Indoor"),
    ("39, Кухня", "39 kitchen")
]


def tuya_sensors_info():
    """
    Prepares a beautiful view of information

    :param device_data:
    :return:
    """

    def data(device_name):
        """
        Parse needed data from every device.

        :param device_name:
        :return:
        """
        try:
            device = c.getstatus(devices[device_name])['result']
            temp = int(device[0]['value']) / 10
            humidity = int(device[1]['value'])
            battery = device[2]['value']

            battery_status = ""
            if isinstance(battery, int):
                if battery >= 90:
                    battery_status = str(battery) + "%⚡"
                elif 30 < battery < 90:
                    battery_status = str(battery) + "%🔋"
                else:
                    battery_status = str(battery) + "%🪫"

            elif isinstance(battery, str):
                if battery == "high":
                    battery_status = battery + " ⚡"
                elif battery == "middle":
                    battery_status = battery + "🔋"
                else:
                    battery_status = battery + "🪫"

            return {'temp': temp, 'humidity': humidity, 'battery': battery_status}

        except Exception as err:
            # For beauty output in result, in future must be fixed
            print(err)
            return {'temp': "Failed ", 'humidity': "Failed ", 'battery': "Failed "}

    device_data = {}  # Final sorting for display in the format {Device_name: "temp": data, ..etc}

    for location, device_name in device_locations:
        device_data[location] = {device_name: data(device_name)}

    output = ""
    try:
        for location, data in device_data.items():
            for device_name, info in data.items():
                output += f"{location}:\n"
                output += "=" * len(location) + "\n"
                output += f"{'Температура:':<15} {info['temp']}°C\n"
                output += f"{'Вологість:':<15} {info['humidity']}%\n"
                output += f"{'Акумулятор:':<15} {info['battery']}\n\n"
    except Exception as err:
        print(err)
    return output


# DEBUG
# print(tuya_sensors_info())
# print(device_data)
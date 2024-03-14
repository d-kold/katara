import os
import typing

from logger import LOGGER


class EnvConfig:
    CONFIG_KEYS = [('MQTT_HOST', 'localhost', str, False),
                   ('MQTT_PORT', '1883', int, False),
                   ('MQTT_QOS', '0', int, False),
                   ('MQTT_USERNAME', '', str, False),
                   ('MQTT_PASSWORD', '', str, True)]

    @staticmethod
    def load(keys: typing.List[typing.Tuple[str,
                                            typing.Optional[str],
                                            typing.Any,
                                            bool]]
             ) -> typing.Dict[str, typing.Any]:
        result = {}
        LOGGER.info('Config:')
        max_length_name = max(len(key[0]) for key in keys)
        for name, default, transform, hide in keys:
            if default is None and (name not in os.environ):
                raise Exception(f'Missing environment variable {name}')

            env_value = os.getenv(name, default)
            LOGGER.info(f'    {f"{name}:".ljust(max_length_name + 4)}{"<hidden>" if hide else env_value}')
            result[name] = transform(env_value)
        LOGGER.info('')

        return result

import json
import sys
from typing import Dict


def get_last_url() -> str:
    """
    Retrieve the last URL stored in the 'property.txt' file.

    :return: The last URL stored in the 'property.txt' file, or an empty string if the file
        does not exist.
    :rtype: str
    """
    try:
        with open("property.txt") as file:
            return file.readline().rstrip()
    except FileNotFoundError:
        return ""


def save(url: str) -> None:
    """
    Save a URL to the 'property.txt' file.

    :param url: The URL to be saved in the 'property.txt' file.
    :type url: str
    """
    with open("property.txt", "w") as file:
        file.write(url)


def load_config() -> Dict:
    """
    Load 'config.json' contents.
    """
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        sys.exit("File 'config.json' not found")


def load_api_key() -> str:
    """
    Extract the ScrapOps API key.

    :return: The ScrapOps API key as a string.
    :rtype: str

    :raises ValueError: If the API key is not specified in the configuration file.
    """
    config = load_config()
    api_key = config.get("api_key")
    if api_key is None:
        raise ValueError("API key is not specified in the configuration file")
    return api_key

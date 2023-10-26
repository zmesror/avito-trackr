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

"""
Exception raised
"""


class NoApiKey(Exception):
    """
    Exception raised when missing API key
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.args[0]} is missing API key"

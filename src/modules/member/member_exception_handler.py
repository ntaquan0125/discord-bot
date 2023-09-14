from typing import *


class memberNoPermission(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "You do not have the permission"


class idAlreadySignUp(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your discord ID already sign up to this server, please contact to admin for more information"


class idNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "Your discord ID you want to change info isn't exist in system, please contact to admin for more information"

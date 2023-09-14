import discord

from typing import *


class errorHandle:
    def __init__(self) -> None:
        pass

    async def noPermission(interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            "You do not have the permission", ephemeral=True
        )

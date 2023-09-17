import discord
from discord.ext.commands import Cog, Bot
from discord import app_commands

from utils import *
from typing import *

from datetime import date, datetime

from member_exception_handler import *
from database_bot_database import botDatabase

GUILD_ID = discord.Object(get_config_value("pif_guild_id"))


class botMemberManagement(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase) -> None:
        super().__init__()

        self.bot = bot
        self.database_handle = database_handle

    async def check_guild_id(interaction: discord.Interaction) -> bool:
        if interaction.guild_id == get_config_value("pif_guild_id"):
            return True
        else:
            await interaction.response.send_message(
                "You don't have permission", ephemeral=True
            )
            return False

    @app_commands.command(name="sign_up", description="Sign up your self to PIF bot")
    @app_commands.describe(
        name="Your name",
        birthday="Your birthday",
        mail="Your email address",
        phone="Your phone number",
        university_id="Your university ID",
    )
    @app_commands.check(check_guild_id)
    async def sign_up_new_member(
        self,
        interaction: discord.Interaction,
        name: str,
        birthday: str,
        mail: str,
        phone: str,
        university_id: str,
    ):
        try:
            data_verify = await self.database_handle.find_with_filter(
                "discord_ID", str(interaction.user.id)
            )

            if len(list(data_verify)) > 0:
                raise idAlreadySignUp

            await self.database_handle.add_new_people(
                name=name,
                birthday=birthday,
                mail=mail,
                phone=phone,
                university_ID=university_id,
                PIFer_Cxx="",
                PIFer_role=["PIFer"],
                discord_ID=str(interaction.user.id),
                discord_role=["PIFer"],
            )
            await interaction.response.send_message("Complete sign in", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @app_commands.command(
        name="change_data", description="Change data of member in PIF server"
    )
    @app_commands.describe(
        discord_id="Mention the user you want to change infomation",
        name="Name you want to change to",
        birthday="Birthday you want to change to",
        mail="Email address you want to change to",
        phone="Phone number you want to change to",
        university_id="University ID you want to change to",
        pifer_cxx="Course of C joining to PIF you want to change to",
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.check(check_guild_id)
    async def change_member_info(
        self,
        interaction: discord.Interaction,
        discord_id: str,
        name: str = "",
        birthday: str = "",
        mail: str = "",
        phone: str = "",
        university_id: str = "",
        pifer_cxx: str = "",
    ):
        if interaction.guild_id != get_config_value("pif_guild_id"):
            await interaction.response.send_message(
                "You not have permission", ephemeral=True
            )
        try:
            discord_ID_database = discord_id[2 : len(discord_id) - 1]

            data_verify = await self.database_handle.find_with_filter(
                "discord_ID", discord_ID_database
            )

            if len(list(data_verify)) == 0:
                raise idNotFound

            await self.database_handle.update_data_people(
                name=name,
                birthday=birthday,
                mail=mail,
                phone=phone,
                university_id=university_id,
                PIFer_Cxx=pifer_cxx,
                discord_ID=discord_ID_database,
            )

            await interaction.response.send_message("Change completed", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(e.__str__(), ephemeral=True)
            print(e)

    @change_member_info.error
    async def error_respone(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        try:
            if isinstance(error, app_commands.MissingPermissions):
                await interaction.response.send_message(
                    memberNoPermission.__str__(self=self), ephemeral=True
                )
                raise memberNoPermission
        except Exception as e:
            print(e)

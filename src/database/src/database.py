import pymongo

from typing import *


class BotDatabase:
    def __init__(self, url: str, database_name: str, collection_name: str) -> None:
        self.mongo_database = pymongo.MongoClient(url)
        self.member_PIF = self.mongo_database[database_name]
        self.discord_database = self.member_PIF[collection_name]
        self.last_id = self.discord_database.count_documents({})
        self.uint_template = {
            "_id": 0,
            "name": "1",
            "birthday": "2",
            "mail": "3",
            "phone": "4",
            "University_ID": "5",
            "PIFer_Cxx": "6",
            "PIFer_role": "7",
            "discord_ID": "8",
            "discord_role": "9",
        }

    def add_new_people(
        self,
        name: str,
        birthday: str,
        mail: str,
        phone: str,
        University_ID: str,
        PIFer_Cxx: str,
        PIFer_role: List[str],
        discord_ID: str,
        discord_role: List[str],
    ):
        uint = self.uint_template
        uint["_id"] = self.last_id
        uint["name"] = name
        uint["birthday"] = birthday
        uint["mail"] = mail
        uint["phone"] = phone
        uint["University_ID"] = University_ID
        uint["PIFer_Cxx"] = PIFer_Cxx
        uint["PIFer_role"] = PIFer_role
        uint["discord_ID"] = discord_ID
        uint["discord_role"] = discord_role

        self.discord_database.insert_one(uint)

        self.last_id += 1

    def change_data_people(self):
        self.discord_database.insert_one(self.uint_template)


test = BotDatabase("mongodb://root:password@mongo:27017/?authSource=admin")

import cv2
import discord
import numpy as np
import urllib.request

from discord.ext import commands

from utils import *


class AnimeFaceRegconition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def url_to_image(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image

    def detect(
        self, image, cascade_file="./src/modules/anime_face/lbpcascade_animeface.xml"
    ):
        cascade = cv2.CascadeClassifier(cascade_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24)
        )
        if len(faces) > 0:
            for x, y, w, h in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite("./src/modules/anime_face/face_detected.png", image)
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if not self.bot.is_ready:
            return

        try:
            if message.attachments[0].url.lower().endswith((".png", ".jpg", ".jpeg")):
                image = self.url_to_image(message.attachments[0].url)
                if self.detect(image):
                    print_debug(self, "Found face")
                    await message.channel.send(
                        file=discord.File("./src/modules/anime_face/face_detected.png")
                    )
        except IndexError:
            pass

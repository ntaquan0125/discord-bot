import cv2
import discord

from discord.ext import commands

from utils.media import get_image_from_url


class AnimeFaceRegconition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def detect(self, image, cascade_file = './cogs/anime_face/lbpcascade_animeface.xml'):
        cascade = cv2.CascadeClassifier(cascade_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imwrite('./cogs/anime_face/face_detected.png', image)
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if not self.bot.is_ready:
            return

        try:
            if message.attachments[0].url.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = get_image_from_url(message.attachments[0].url)
                if self.detect(image):
                    await message.channel.send(file=discord.File('./cogs/anime_face/face_detected.png'))
        except IndexError:
            pass


async def setup(bot):
    await bot.add_cog(AnimeFaceRegconition(bot))

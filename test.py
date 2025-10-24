import asyncio
from Bot.bot import Bot

bot = Bot(token="7787525076:AAFhpp1MyZvOd1njgtWvM9u9AW49Jd-4rXk")

print(asyncio.run(bot.request("GET","getMe")))
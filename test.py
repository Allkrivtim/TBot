import asyncio
from TBot import Dispatcher, Bot

bot = Bot(token="7787525076:AAFhpp1MyZvOd1njgtWvM9u9AW49Jd-4rXk")
dp = Dispatcher(bot)

#print(asyncio.run(bot.request("GET","getMe")))
print(asyncio.run(dp.start_polling()))
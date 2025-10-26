import asyncio
from TBot import Dispatcher, Bot

bot = Bot(token="7787525076:AAFhpp1MyZvOd1njgtWvM9u9AW49Jd-4rXk")
dp = Dispatcher(bot)

async def main():
    await dp.start_polling()



if __name__ == "__main__":
    asyncio.run(main())

@dp.command_handler()
def start_cmd():
    print(data)
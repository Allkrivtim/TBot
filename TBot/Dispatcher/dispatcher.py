from TBot.Bot import Bot

class Dispatcher(Bot):
    def __init__(self, bot=Bot):
        super().__init__(bot.token)
        self.handlers = []

    def command_handler(self, func, update):
        print(update)
        self.handlers.append(func)
        return func

    async def start_polling(self):
        params = {
            "offset": None,
            "limit": 100,
            "timeout": 30
        }

        while True:
            update = await self._make_request("GET", "getUpdates", params=params, timeout=params.get("timeout"))
            params["offset"] = update.get("result")[0].get("update_id") + 1

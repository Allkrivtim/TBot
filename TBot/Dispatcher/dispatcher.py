from TBot.Bot import Bot
from TBot.Types import PollingResponse

class Dispatcher(Bot):
    def __init__(self, bot=Bot):
        super().__init__(bot.token)
        self.command_handler = None

    async def start_polling(self):
        params = {
            "offset": None,
            "limit": 100,
            "timeout": 30
        }

        while True:
            response = await self._make_request("GET", "getUpdates", params=params, timeout=params.get("timeout"))
            params["offset"] = response.get("result")[0].get("update_id") + 1
            update = PollingResponse(response)

            for update in update.updates:
                if update.type == 'message':
                    msg = update.message

                    if msg.is_command:
                        self.command_handler(msg)
                    else:
                        print(f"Text: {msg.text}")

                    if msg.has_media:
                        print("Media.")

                elif update.type == 'callback_query':
                    cb = update.callback_query
                    print(f"Callback: {cb.data}")

    async def command_handler(self, func):
        async def wrapper(data):
            func.__globals__['data'] = data
            return await func()
        self.command_handler = wrapper
        return func
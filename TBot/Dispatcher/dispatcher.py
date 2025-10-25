from TBot.Bot import Bot
from TBot.Types import TelegramUpdate, PollingResponse, CallbackQuery, Message

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
            response = await self._make_request("GET", "getUpdates", params=params, timeout=params.get("timeout"))
            params["offset"] = response.get("result")[0].get("update_id") + 1
            update = PollingResponse(response)

            for update in update.updates:
                if update.type == 'message':
                    msg = update.message

                    if msg.is_command:
                        print(f"Command: {msg.command}")
                        print(f"Args: {msg.command_args}")
                    else:
                        print(f"Text: {msg.text}")

                    if msg.has_media:
                        print("Media.")

                elif update.type == 'callback_query':
                    cb = update.callback_query
                    print(f"Callback: {cb.data}")




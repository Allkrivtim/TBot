class TelegramUpdate:
    def __init__(self, update_data):
        self.raw = update_data
        self.update_id = self.raw.get('update_id')
        self.type = self._detect_type()

    #--TYPE OF UPDATE--
    def _detect_type(self):
        if 'message' in self.raw:
            return 'message'
        elif 'edited_message' in self.raw:
            return 'edited_message'
        elif 'callback_query' in self.raw:
            return 'callback_query'
        elif 'inline_query' in self.raw:
            return 'inline_query'
        elif 'channel_post' in self.raw:
            return 'channel_post'
        elif 'poll' in self.raw:
            return 'poll'
        elif 'poll_answer' in self.raw:
            return 'poll_answer'
        else:
            return 'unknown'
    #--MESSAGE--
    @property
    def message(self):
        msg = self.raw.get('message') or self.raw.get('edited_message')
        return Message(msg) if msg else None
    #--CALLBACK--
    @property
    def callback_query(self):
        cb = self.raw.get('callback_query')
        return CallbackQuery(cb) if cb else None

    def __repr__(self):
        return f"<TelegramUpdate id={self.update_id} type={self.type}>"


class Message:
    def __init__(self, message_data):
        if not message_data:
            raise ValueError("Message data is empty")

        self.raw = message_data
        self.message_id = message_data.get('message_id')
        self.date = message_data.get('date')
        self.text = message_data.get('text', '')

        # Sender
        sender = message_data.get('from', {})
        self.sender_id = sender.get('id')
        self.sender_is_bot = sender.get('is_bot', False)
        self.sender_first_name = sender.get('first_name', '')
        self.sender_username = sender.get('username')
        self.sender_language = sender.get('language_code', 'en')

        # Chat
        chat = message_data.get('chat', {})
        self.chat_id = chat.get('id')
        self.chat_type = chat.get('type', 'private')
        self.chat_title = chat.get('title')  # для групп
        self.chat_username = chat.get('username')
        self.chat_first_name = chat.get('first_name')

        # Дополнительные поля
        self.reply_to_message = message_data.get('reply_to_message')
        self.entities = message_data.get('entities', [])
        self.photo = message_data.get('photo')
        self.document = message_data.get('document')
        self.sticker = message_data.get('sticker')
        self.video = message_data.get('video')
        self.voice = message_data.get('voice')

    @property
    def is_command(self):
        return bool(self.text and self.text.startswith('/'))

    @property
    def command(self):
        if not self.is_command:
            return None
        # /start@botname arg1 arg2 -> start
        cmd = self.text.split()[0][1:]  # убираем /
        return cmd.split('@')[0]  # убираем @botname

    @property
    def command_args(self):
        if not self.is_command:
            return []
        parts = self.text.split()[1:]
        return parts

    @property
    def has_media(self):
        return any([self.photo, self.document, self.sticker,
                    self.video, self.voice])

    def __repr__(self):
        preview = self.text[:30] + '...' if len(self.text) > 30 else self.text
        return f"<Message id={self.message_id} from={self.sender_username} text='{preview}'>"


class CallbackQuery:
    def __init__(self, callback_data):
        if not callback_data:
            raise ValueError("Callback data is empty")

        self.raw = callback_data
        self.id = callback_data.get('id')
        self.data = callback_data.get('data', '')

        # From user
        sender = callback_data.get('from', {})
        self.user_id = sender.get('id')
        self.username = sender.get('username')
        self.first_name = sender.get('first_name', '')

        # Message (если есть)
        self.message = callback_data.get('message')
        self.chat_id = self.message.get('chat', {}).get('id') if self.message else None

    def __repr__(self):
        return f"<CallbackQuery id={self.id} from={self.username} data='{self.data}'>"


class PollingResponse:
    def __init__(self, response_data):
        self.raw = response_data
        self.ok = response_data.get('ok', False)

        if not self.ok:
            error_code = response_data.get('error_code')
            description = response_data.get('description', 'Unknown error')
            raise Exception(f"Telegram API Error {error_code}: {description}")

        results = response_data.get('result', [])
        self.updates = [TelegramUpdate(upd) for upd in results]

    def __len__(self):
        return len(self.updates)

    def __iter__(self):
        return iter(self.updates)

    def __repr__(self):
        return f"<PollingResponse ok={self.ok} updates={len(self.updates)}>"

# test = TelegramUpdate({
#     "update_id": 712835318,
#     "message": {
#         "message_id": 8,
#         "from": {
#             "id": 2025626360,
#             "is_bot": "false",
#             "first_name": "Timitorix",
#             "username": "suvorovalk",
#             "language_code": "en"
#         },
#         "chat": {
#             "id": 2025626360,
#             "first_name": "Timitorix",
#             "username": "suvorovalk",
#             "type": "private"
#         },
#         "date": 1761379631,
#         "text": "/start",
#         "entities": [
#             {
#                 "offset": 0,
#                 "length": 6,
#                 "type": "bot_command"
#             }
#         ]
#     }
# })
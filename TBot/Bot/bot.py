import httpx

class Bot:
    def __init__(self, token: str):
        #--INITIALIZATION--
        self.token = token
        self.tg_url = "https://api.telegram.org/bot"

    async def _make_request(self, http_method:str, method: str, params=None, timeout=31):
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(f"{http_method}",f"{self.tg_url}{self.token}/{method}", params=params)
            #response.data = json.dumps(response.json(), indent=4, ensure_ascii=False)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error:{response.status_code}")
                return None

    async def request(self, http_method:str, method: str, params=None):
        return await self._make_request(http_method, method, params)
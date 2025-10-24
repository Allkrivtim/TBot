import httpx,json

class Bot:
    def __init__(self, token: str, debug: bool=True):
        #--INITIALIZATION--
        self.token = token
    async def request(self, http_method:str, method: str):
        response = httpx.request(f"{http_method}",f"https://api.telegram.org/bot{self.token}/{method}")
        response.json = json.dumps(response.json(), indent=4, ensure_ascii=False)
        if response.status_code == 200:
            return response.json
        else:
            print(f"Error:{response.status_code}")
            return None

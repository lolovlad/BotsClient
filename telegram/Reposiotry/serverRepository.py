from httpx import AsyncClient
from ..settiongs import settings


class ServerRepository:
    def __init__(self):
        self.__url_base: str = f"http://{settings.host_server}:{settings.port_server}/v1/"

    async def get_region(self) -> list:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get("/filter/region")
            return r.json()

    async def get_one_region(self, id_region: int) -> dict:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/filter/region/{id_region}")
            return r.json()

    async def get_type(self) -> list:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get("/filter/type")
            return r.json()

    async def get_one_type(self, id_type: int) -> dict:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/filter/type/{id_type}")
            return r.json()

    async def get_num_page(self, type_reserve: int | str, region_reserve: int | str) -> int:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/reserver/count_page", params={"type_reserve": type_reserve, "region_reserve": region_reserve})
            return r.json()["count"]

    async def get_page_reserver(self, type_reserve: int | str, region_reserve: int | str, num_page: int) -> dict:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/reserver/page/{num_page}", params={"type_reserve": type_reserve, "region_reserve": region_reserve})
            return r.json()[0]

    async def get_one_reserver(self, id_reserver: int) -> dict:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/reserver/get_one/{id_reserver}")
            return r.json()

    async def get_answer(self, text: str) -> dict:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/chat/answer", params={"text_chat": text}, timeout=10000)
            return r.json()

    async def get_weather(self, id_reserve: int) -> dict:
        async with AsyncClient(base_url=self.__url_base) as client:
            r = await client.get(f"/chat/weather/{id_reserve}", timeout=10000)
            return r.json()
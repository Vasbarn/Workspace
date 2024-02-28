import requests
import json

class BitrixConnector:

    def __init__(self, keys: dict, url):
        self.__api_keys = keys
        self.__url = url
        self.__headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.__query_url = "{url}{key}/{method}".format(url=self.__url, key="{key}",method="{method}" )

    def get_elements_from_list(self, data: dict = None, ):
        list_elements = []
        result = {
            "fields": None,
            "data": list_elements
        }

        with (requests.Session() as session):
            # Получаем все поля списка
            response = session.post(
                url=self.__query_url.format(
                    key=self.__api_keys.get("lists"),
                    method="lists.field.get"
                ),
                data=json.dumps(data),
                headers=self.__headers
            ).json()
            result["fields"] = response.get("result")
            # получаем элементы
            response = session.post(
                url=self.__query_url.format(
                    key=self.__api_keys.get("lists"),
                    method="lists.element.get"
                    ),
                data=json.dumps(data),
                headers=self.__headers
                ).json()
            list_elements.extend(response.get("result"))
            while response.get("next"):
                data['start'] = response.get("next")
                response = session.post(
                    url=self.__query_url.format(
                        key=self.__api_keys.get("lists"),
                        method="lists.element.get"
                    ),
                    data=json.dumps(data),
                    headers=self.__headers
                ).json()
                list_elements.extend(response.get("result"))
        return result


method = "lists.element.get"
key = "fdrwucecw1uvpel1"
url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
if __name__ == "__main__":
    answer = {}
    cls = BitrixConnector(dict(lists="fdrwucecw1uvpel1"), "https://bitrix.tg-alterra.ru/rest/1166/")
    answer["BP"] = cls.get_elements_from_list(
        {'IBLOCK_TYPE_ID': 'bitrix_processes',
         'IBLOCK_ID': '182',}
    )
    answer["BP2"] = cls.get_elements_from_list(
        {'IBLOCK_TYPE_ID': 'lists_socnet',
         'IBLOCK_ID': '178', }
    )
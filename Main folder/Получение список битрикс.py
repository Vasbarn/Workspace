import requests
import json
import pandas as pd


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

    def get_workers(self, data: dict = None, ):
        """Получаем всех сотрудников из указанных подразделений из битрикса"""
        result = []
        with requests.Session() as session:
            response = session.post(
                url=self.__query_url.format(
                    key=self.__api_keys.get("user"),
                    method="user.get.json"
                ),
                data=json.dumps(data),
                headers=self.__headers
            ).json()
            result.extend(response.get("result"))
            while response.get("next"):
                data['start'] = response.get("next")
                response = session.post(
                    url=self.__query_url.format(
                        key=self.__api_keys.get("user"),
                        method="user.get.json"
                    ),
                    data=json.dumps(data),
                    headers=self.__headers
                ).json()
                result.extend(response.get("result"))
        return result


if __name__ == "__main__":
    cls = BitrixConnector(dict(lists="fdrwucecw1uvpel1", user="vqxmfrmo0ewoupy7"),
                          "https://bitrix.tg-alterra.ru/rest/1166/")
    # bizproc = cls.get_elements_from_list(
    #     {'IBLOCK_TYPE_ID': 'bitrix_processes',
    #      'IBLOCK_ID': '182',}
    # )
    records_list = cls.get_elements_from_list(
        {'IBLOCK_TYPE_ID': 'lists_socnet',
         'IBLOCK_ID': '178', }
    )
    # bizproc_fields = pd.DataFrame(bizproc["fields"])
    # bizproc_data = pd.DataFrame(bizproc["data"])
    records_list_fields = pd.DataFrame(records_list["fields"])
    records_list_data = pd.DataFrame(records_list["data"])
    users = pd.DataFrame(cls.get_workers({}))

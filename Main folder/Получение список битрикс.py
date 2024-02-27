import requests
import json

method = "lists.element.get"
key = "fdrwucecw1uvpel1"
url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
data = {
    'IBLOCK_TYPE_ID': 'bitrix_processes',
    'IBLOCK_ID': '182',
}
result = []
with requests.Session() as session:
    response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
    print(response)
    data = {
        'IBLOCK_TYPE_ID': 'bitrix_processes',
        'IBLOCK_ID': '182',
    }
    method = "lists.get"
    url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
    response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
    print(response)
    method = "lists.field.get"
    url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
    response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
    print(response)
#     result.extend(response.get("result"))
#     print(response)
#     while response.get("next"):
#         data['start'] = response.get("next")
#         response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
#         print(response.get("next"))
#         result.extend(response.get("result"))
#         break
# for elem in result:
#     print(elem)

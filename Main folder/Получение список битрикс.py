import requests
import json

method = "lists.element.get"
key = "fdrwucecw1uvpel1"
url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
data = {
    'IBLOCK_TYPE_ID': 'lists_socnet',
    'IBLOCK_CODE': 'list178',
    # 'filter': {
    #     "ACTIVE": True
    # },
}
result = []
with requests.Session() as session:
    response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
    result.extend(response.get("result"))
    print(response.get("next"))
    while response.get("next"):
        data['start'] = response.get("next")
        response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
        print(response.get("next"))
        result.extend(response.get("result"))
        break
for elem in result:
    print(elem)

import requests
import json
import logging
import pandas as pd


def get_task(dict_users: dict) -> dict:
	method = "tasks.task.list.json"
	key = "wm57zm41jef9byib"
	url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
	headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
	num = 0
	result = []
	for type_filter in ["CREATED_BY", "RESPONSIBLE_ID", "ACCOMPLICE"]:
		data = {
			'filter': {
				type_filter: list(dict_users.keys()),
				"REPLICATE": 'N',
				"REAL_STATUS": [1, 2, 3]
			},
			'select': [
				'ID', 'TITLE', 'DESCRIPTION', 'STATUS', 'CREATED_BY', 'CREATED_DATE', "DEADLINE",
				'RESPONSIBLE_ID', "ACCOMPLICES",  'COMMENTS_COUNT', 'TIME_ESTIMATE', 'TIME_SPENT_IN_LOGS',
			],
			'start': num
		}
		with requests.Session() as session:
			response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
			result.extend(response.get("result").get("tasks"))
			while response.get("next"):
				data['start'] = response.get("next")
				logger_for_BX.info(f"Задачи {data.get("start")} из {response.get("total")}")
				response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
				result.extend(response.get("result").get("tasks"))
		result_dict = dict()
	for elem in result:
		if not result_dict.get(elem.get("id")):
			elem["creator"] = elem["creator"]["name"]
			elem["responsible"] = elem["responsible"]["name"]
			accomplices_list = []
			if isinstance(elem["accomplicesData"], dict):
				for id_key in elem["accomplicesData"].keys():
					if id_key in list(dict_users.keys()):
						accomplices_list.append(id_key)
				elem["accomplicesData"] = accomplices_list

			result_dict[elem.get("id")] = elem
	return result_dict


def get_workers() -> dict:
	"""Получаем всех сотрудников из указанных подразделений из битрикса"""
	method = "user.get.json"
	key = "vqxmfrmo0ewoupy7"
	url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
	headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
	list_departament = [
		7,  # ИТ-отдел
		4995,  # Команда 1С разработчиков №3
		5005,  # Команда 1С разработчиков №2
		5000,  # Команда 1С разработчиков №1
		5006,  # Сектор Веб-разработки
		5007,  # Сектор системного администрирования
		5008,  # Сектор технической поддержки
	]
	num = 0
	data = {
		'filter': {
			"UF_DEPARTMENT": list_departament,
			"ACTIVE": True
		},
		'start': num
	}
	result = []
	with requests.Session() as session:
		response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
		result.extend(response.get("result"))
		while response.get("next"):
			data['start'] = response.get("next")
			logger_for_BX.info(f"Пользователи {data.get("start")} из {response.get("total")}")
			response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
			result.extend(response.get("result"))
	result_dict = dict()
	for elem in result:
		if not result_dict.get(elem.get("ID")) and int(elem.get("ID")) != 1:
			result_dict[elem.get("ID")] = elem
	return result_dict


if __name__ == "__main__":
	logging.basicConfig(level=logging.WARNING)
	logger_for_BX = logging.getLogger(__name__)
	logger_for_BX.setLevel(logging.WARNING)
	users_it: dict = get_workers()
	users_it_df = pd.DataFrame(users_it.values())
	tasks = get_task(users_it)
	tasks_df = pd.DataFrame(tasks.values())


import time

import requests



headers = {
    'authority': 'kkt-online.nalog.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_ym_uid=17013966147887428; _ym_d=1701396614; _ym_isad=2; kkt-nalog-ru-cookie=3d5f3e9fabb44576bccc8ce0257221f3; sputnik_session=1701400963380|1; _ym_visorc=b; session-cookie=179c96b248e2cca1099cc1d4beb261f5506614d140f3fbd987cbdccfcd7ba20621ac155d8eb08f7d02a60ecd7f7b903a',
    'origin': 'https://kkt-online.nalog.ru',
    'referer': 'https://kkt-online.nalog.ru/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'type': 'request',
    'date': '03.12.2023',
    'time': '11:44',
    'operationtype': '1',
    'summ': '240',
    'fn': '7281440500625269',
    'fd': '37480',
    'fp': '816932496',
}
with requests.Session() as ses:
    response = ses.post('https://kkt-online.nalog.ru/openapikkt.html', headers=headers, data=data).json()
    print(response)
    data = {
        'type': 'poll',
        'UserToken': response.get("UserToken"),
        'id': response.get("ID"),
    }
    response = ses.post('https://kkt-online.nalog.ru/openapikkt.html', data=data, headers=headers,
                        cookies=ses.cookies)
    print(response.text)
    time.sleep(5)
    response = ses.post('https://kkt-online.nalog.ru/openapikkt.html', data=data, headers=headers,
                        cookies=ses.cookies)
    print(response.text)




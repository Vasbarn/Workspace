import requests
import json
import tkinter as tk

from tkinter.messagebox import showinfo, askyesno, showerror


def click():
    result = askyesno(title="Подтверждение", message="Отправить оповещение?")
    if result:
        message = word_editor.get("1.0", "end").strip()
        if len(message):
            main(message)
            showinfo("Успех", "Все оповещения отправлены!")
            word_editor.delete("1.0", "end")
        else:
            showerror("Пустое сообщение", "Текст оповещения пустой")
    else:
        pass


def main(message: str):
    with requests.Session() as sess:
        send_notify(sess, message)


def send_notify(session: requests.Session(), message: str = "Тест") -> None:
    method = "im.notify.personal.add.json"
    key = "3dwud0dv6vlq3uk0"
    url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    for id_bx in get_workers(session):
        data = {
            'USER_ID': 1166,
            'MESSAGE': message
        }
        session.post(url=url, data=json.dumps(data), headers=headers).json()
        break


def get_workers(session: requests.Session()) -> list:
    """Получаем всех сотрудников из указанных подразделений из битрикса"""
    method = "user.get.json"
    key = "vqxmfrmo0ewoupy7"
    url = f"https://bitrix.tg-alterra.ru/rest/1166/{key}/{method}"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {
        'filter': {
            "ACTIVE": True
        },
    }
    result = []
    while True:
        response: dict = dict(session.post(url=url, data=json.dumps(data), headers=headers).json())
        result.extend(response.get("result"))
        if not response.get("next"):
            break
        data['start'] = response.get("next")
    result = list(map(lambda elem: elem.get("ID"), result))
    return result


window = tk.Tk()
window.title("Отправка оповещений в Bitrix24")
window.iconbitmap(default="favicon.ico")


label = tk.Label(text="Введите текст для оповещения", font="Verdana 15 normal roman")
label.pack(side=tk.TOP)

word_editor = tk.Text(bg="#E6E6FA", wrap="word", height=6)
word_editor.pack(side=tk.TOP)

send_m = tk.Button(text="Отправить",  command=click, font="Verdana 15 normal roman")
send_m.pack(expand=True, anchor=tk.S, fill=tk.X)


if __name__ == "__main__":
    window.mainloop()

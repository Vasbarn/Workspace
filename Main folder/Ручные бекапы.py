import os
import shutil
import time
from threading import Thread
import datetime

class HDDir:
    def __init__(self):
        self.__path_on_hd_main = "D:" + os.sep + "Резервные копии"
        self.__dir_hd_with_path = {
            "Бухгалтерия": os.path.join(self.__path_on_hd_main, "Бухгалтерия"),
            "ЗУП": os.path.join(self.__path_on_hd_main, "ЗУП"),
            "Охрана труда": os.path.join(self.__path_on_hd_main, "Охрана труда"),
            "Торговля": os.path.join(self.__path_on_hd_main, "Торговля"),
        }

        self.__path_on_70_main = 2 * os.sep + os.path.join("192.168.8.70", "Backup")
        self.__path_on_62_main = 2 * os.sep + os.path.join("192.168.8.62", "e$", "Data", "Backup")
        self.__dir_back__with_path = {
            "Бухгалтерия": os.path.join(self.__path_on_70_main, "accounting3"),
            "Бухгалтерия 2": os.path.join(self.__path_on_70_main, "accounting_black"),
            "ЗУП": os.path.join(self.__path_on_70_main, "salary3"),
            "Охрана труда": os.path.join(self.__path_on_70_main, "ot-soft"),
            "Торговля": self.__path_on_62_main
        }

        self.__prefix_accounting = "accounting3_backup_"
        self.__prefix_accounting_black = "accounting_black_backup_"
        self.__prefix_salary3 = "salary3_backup_"
        self.__prefix_ot_soft = "ot-soft_backup_"
        self.__prefix_trade = "trade_backup_"

    def get_all_wanted_files_on_usb(self) -> dict:
        """
        Собираем все файлы на флешке в папках которые есть. Для последующего удаления
        :return: result: dict dictionary need files
        """
        result = dict()
        for key, value in self.__dir_hd_with_path.items():
            if key == "Бухгалтерия":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_accounting), files)
                result["Бухгалтерия"] = list(map(lambda file_name: os.path.join(value, file_name), data))
                data = filter(lambda name_file: name_file.startswith(self.__prefix_accounting_black), files)
                result["Бухгалтерия 2"] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "ЗУП":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_salary3), files)
                result["ЗУП"] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "Охрана труда":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_ot_soft), files)
                result["Охрана труда"] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "Торговля":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_trade), files)
                result["Торговля"] = list(map(lambda file_name: os.path.join(value, file_name), data))
        return result

    def get_all_wanted_files_disk(self):
        """
        Возвращает список нужны файлов в директории где бекапы
        :return: result: dict dictionary need files
        """
        result = dict()
        for key, value in self.__dir_back__with_path.items():
            if key == "Бухгалтерия":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_accounting), files)
                result[key] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "Бухгалтерия 2":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_accounting_black), files)
                result[key] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "ЗУП":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_salary3), files)
                result[key] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "Охрана труда":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_ot_soft), files)
                result[key] = list(map(lambda file_name: os.path.join(value, file_name), data))
            elif key == "Торговля":
                files = os.listdir(value)
                data = filter(lambda name_file: name_file.startswith(self.__prefix_trade), files)
                result[key] = list(map(lambda file_name: os.path.join(value, file_name), data))
        return result

    def del_old(self, num: int,  mode: str = "usb") -> list:
        """
        Удаление старых файлов, либо на диске, либо на флешке
        :param mode: string only 2 state = usb or hd
        :param num: int The number of files to remove
        :return: result: list list deleted files
        """
        result = []
        if mode == "usb":
            files = self.get_all_wanted_files_on_usb()
        elif mode == "hd":
            files = self.get_all_wanted_files_disk()
        else:
            raise ValueError
        for key, value in files.items():
            temp = dict()
            if len(value) > num:
                for path_file in value:
                    date_create = os.path.getctime(path_file)
                    temp[date_create] = path_file
                temp = dict(sorted(temp.items(), key=lambda x: x[0], reverse=True)[num:])
                for path_file in temp.values():
                    result.append(path_file)
                    os.remove(path_file)
        return result

    def start_copy(self):
        for key, value in self.get_all_wanted_files_disk().items():
            temp = dict()
            for path_file in value:
                date_create = os.path.getctime(path_file)
                temp[date_create] = path_file
            date, path = sorted(temp.items(), key=lambda x: x[0], reverse=True)[0]
            name_file = path.rsplit(os.sep, 1)[-1]
            if key in ["Бухгалтерия", "ЗУП", "Охрана труда", "Торговля"]:
                new_full_path = os.path.join(self.__dir_hd_with_path.get(key), name_file)
                if not os.path.exists(new_full_path):
                    Thread(target=self.my_copy, args=(path, new_full_path, key)).start()
                continue
            elif key == "Бухгалтерия 2":
                new_full_path = os.path.join(self.__dir_hd_with_path.get("Бухгалтерия"), name_file)
                if not os.path.exists(new_full_path):
                    Thread(target=self.my_copy, args=(path, new_full_path, key)).start()

    def get_name_last_file(self):
        result = dict()
        for key, value in self.get_all_wanted_files_disk().items():
            temp = dict()
            for path_file in value:
                date_create = os.path.getctime(path_file)
                temp[date_create] = path_file
            date, path = sorted(temp.items(), key=lambda x: x[0], reverse=True)[0]
            name_file = path.rsplit(os.sep, 1)[-1]
            result[key] = name_file
            print("|{}| {}: {}".format(datetime.datetime.fromtimestamp(date,
                                                                       tz=datetime.UTC).strftime("%d.%m.%Y"),
                                       key,
                                       name_file))
        return result

    @staticmethod
    def my_copy(path, new_full_path, key):
        t1 = datetime.datetime.now()
        print(f"{key} начало копирования в {t1}")
        shutil.copy(path, new_full_path)
        t2 = datetime.datetime.now()
        print(f"{key} завершение копирования в {t2} | Длительность {round((t2 - t1).total_seconds() / 60, 3)} минут")


if __name__ == "__main__":
    proc = HDDir()
    proc.get_name_last_file()
    if input("Хотите начать копирование?\nВведите 1 = да, все остальное = нет:\n") == "1":
        proc.del_old(num=2, mode="usb")  # num=3, mode="usb"
        proc.del_old(num=8, mode="hd")  # num=8, mode="hd"
        proc.start_copy()

import os


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
        self.__path_on_62_main = 2 * os.sep + os.path.join("192.168.8.62","e$","Data", "Backup")
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

    def get_all_wanted_files(self) -> dict:
        """Собираем все файлы на флешке в папках которые есть. Для последующего удаления"""
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

    def del_old(self):
        """Удаление старых файлов на флешке, при условии что в папке больше трех файлов подходящих под отбор"""
        files = self.get_all_wanted_files()
        for key, value in files.items():
            temp = dict()
            if len(value) > 3:
                for path_file in value:
                    date_create = os.path.getctime(path_file)
                    temp[date_create] = path_file
                temp = dict(sorted(temp.items(), key=lambda x: x[0], reverse=True)[3:])
                for path_file in temp.values():
                    os.remove(path_file)

    def start_copy(self):
        """Возвращает список нужны файлов в директории где бекапы"""
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

if __name__ == "__main__":
    proc = HDDir()
    # proc.del_old()
    proc.start_copy()



import csv
import re

from checksum import calculate_checksum, serialize_result


VARIANT = 70
CSV_FILE = "70.csv"


PATTERNS = {
    "telephone": r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$",
    "http_status_message": r"^\d{3}\s[^\n\r]+$", 
    "inn": r"^\d{12}$",
    "identifier": r"^\d{2}-\d{2}/\d{2}$",              
    "ip_v4": r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?){4}$",  
    "latitude": r"^(?:\+|-|)(90\.0+|[0-8]\d\.\d+|\d\.\d+|0+\d\.\d+)$",  
    "blood_type": r"^(A|B|AB|O)[+-]$",                
    "isbn": r"^\d+-\d+-\d+-\d+(?:-\d+)?$",            
    "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",  
    "date": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
}


def read_csv(file_name: str) -> list:
    """
    Метод для чтения данных из CSV файла.
    :param file_name: имя файла, который необходимо прочитать.
    :return: список строк, считанных из файла, без заголовка.
    """
    data = []
    with open(file_name, "r", newline="", encoding="utf-16") as file:
        reader = csv.reader(file, delimiter=";")
        for i in reader:
            data.append(i)
        data.pop(0)
        return data 


def is_row_valid(row: list) -> bool:
    """
    Проверяет, что каждая строка в данных соответствует регулярным выражениям для каждой колонки.
    :param row: строка данных
    :return: True, если строка валидна, False — если нет.
    """
    for idx, value in enumerate(row):
        pattern = list(PATTERNS.values())[idx] 
        if not re.match(pattern, value):
            return False
    return True


def get_invalid_rows(data: list) -> list:
    """
    Метод для поиска индексов невалидных строк в данных.
    :param data: список строк данных для проверки.
    :return: список индексов невалидных строк.
    """
    invalid_indices = []
    for i, row in enumerate(data):
        if not is_row_valid(row):
            invalid_indices.append(i)
    return invalid_indices


if __name__ == "__main__":
    data = read_csv(CSV_FILE)
    invalid_indices = get_invalid_rows(data)
    checksum = calculate_checksum(invalid_indices)
    serialize_result(VARIANT, checksum)

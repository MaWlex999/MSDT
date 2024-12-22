import csv

from typing import Any


class MyCsv():
    def __init__(self, csv_path: str, names: bool,  delimiter: str = ";") -> None:
        """
        ������ csv ���� �� ���� csv_path. ��������� ���������� ���� �������, ����� ���:
        self.csv_path - ���� �� ����� csv
        self.names - �������� ��������
        self.data - ������ �� ������ ����� �� csv �����
        """
        if len(delimiter) > 1:
            raise "�������� ������ ���� �� 1 �������"
        self.csv_path = csv_path
        with open(csv_path, "r", encoding="utf-16") as csv_reader:
            reader = csv.reader(csv_reader, delimiter=delimiter)
            self.data = []
            for row in reader:
                if names:
                    self.names = row
                    names = False
                    continue
                if len(row) != 0:
                    self.data.append(row)
        pass

    def get_values_from_col(self, col_number: int) -> list[Any]:
        """
        ���������� ������ �������� ������������ ������� col_number
        """
        res = []
        for row in self.data:
            res.append(row[col_number])
        return res
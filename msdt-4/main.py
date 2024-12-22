import os
import sys

import logging
import pyqtgraph as pg
import numpy as np

from scipy.fft import fft
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QLabel, QVBoxLayout,
                             QHBoxLayout, QMainWindow,
                             QFileDialog, QListWidget)

import copy_dataset

from work_with_osc import DataOsc
from work_with_csv import MyCsv

# ������ ����������� ������ ��� ������ � osc
module_path = os.path.abspath("cpp/build/Debug")
sys.path.append(module_path)
try:
    import Aegis_osc
except ImportError as e:
    raise "�� ������� ������������� ������ ��� ������ � ���������������!"


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("main.log", mode='a', encoding='utf-8')
    ]
)


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()  # ������� ����������� ������������� ������ QWidget
        self.main_layout_v = QVBoxLayout(self)

        # ���������� �� ������ ����������
        self.label = QLabel()
        self.label.setText("����� ������� ������ 6311-100503D")
        self.label.setStyleSheet("font-size: 18px;")

        # ������ ��� �������� ����� ��������
        self.bttn_copy_dataset = QPushButton()
        self.bttn_copy_dataset.setText("������� ����� �������� � .csv ���� � ��")
        self.bttn_copy_dataset.clicked.connect(self._on_clicked_bttn_copy_dataset)

        # ������ ��� ��������� ������ �� csv �����
        self.bttn_load_csv = QPushButton()
        self.bttn_load_csv.setText("��������� ���������� �� .csv �����")
        self.bttn_load_csv.clicked.connect(self.__on_clicked_bttn_load_csv)

        # ������ ��� ��������� �������� ��������� �������������
        self.bttn_open_alone_osc = QPushButton()
        self.bttn_open_alone_osc.setText("������� �������������")
        self.bttn_open_alone_osc.clicked.connect(self._on_clicked_bttn_open_alone_osc)

        # ���� ���������� ��������� � ������� ����
        self.main_layout_v.addWidget(self.label)
        self.main_layout_v.addWidget(self.bttn_copy_dataset)
        self.main_layout_v.addWidget(self.bttn_load_csv)
        self.main_layout_v.addWidget(self.bttn_open_alone_osc)

    def _on_clicked_bttn_open_alone_osc(self) -> None:
        """���������� ������� ����� ��� ������ �������� ������ ��������"""
        path, _ = QFileDialog.getOpenFileName(self, "�������� ����", "", "OSC Files (*.osc)")
        self.__open_osc(path)

    def _on_clicked_bttn_copy_dataset(self) -> None:
        """���������� ������� ����� ��� ������ �������� ������ ��������"""
        path_from = QFileDialog.getExistingDirectory(self, "������ ����������?")
        if path_from == '':
            return
        copy_dataset.make_copy_dataset(path_from, f"{path_from}_copy")

    def __on_clicked_bttn_load_csv(self) -> None:
        """���������� ������� ����� ��� ������ �������� ������ �� csv �����"""
        path, _ = QFileDialog.getOpenFileName(self, "�������� ����", "", "CSV Files (*.csv)")
        if path == '':
            return

        # �������� ������ my_csv, ������� ������ �������� ��������,
        # �������� ������, �������� �����
        self.csv_file = MyCsv(path, names=True, delimiter=",")

        # �������� ����, ��� ����� ��������� ������������� ���� �� �����
        if not hasattr(self, "list_files"):
            self.list_files = QListWidget(self)
            self.list_files.addItems(self.csv_file.get_values_from_col(1))
            self.list_files.clicked.connect(self._on_clicked_item_list)
            self.list_files.setStyleSheet("max-height: 250px")
            # �������� � ������� ����
            self.main_layout_v.addWidget(self.list_files)
        else:
            self.list_files.clear()
            self.list_files.addItems(self.csv_file.get_values_from_col(1))
            self.list_files.clicked.connect(self._on_clicked_item_list)

        if not hasattr(self, "bttn_create_numpy_datasets"):
            self.bttn_create_numpy_datasets = QPushButton("������� numpy ����� �� ��������")
            self.bttn_create_numpy_datasets.clicked.connect(self.__on_clicked_bttn_create_numpy_datasets)
            # �������� � ������� ����
            self.main_layout_v.addWidget(self.bttn_create_numpy_datasets)
        # �������� ������ ��� �������� osc �����
        if not hasattr(self, "bttn_open_osc"):
            self.bttn_open_osc = QPushButton("������� ���� osc")
            self.bttn_open_osc.clicked.connect(self._on_clicked_bttn_open_osc)
            # �������� � ������� ����
            self.main_layout_v.addWidget(self.bttn_open_osc)
        self.bttn_open_osc.setEnabled(False)

    def __on_clicked_bttn_create_numpy_datasets(self) -> None:
        # item_count = self.list_files.count()
        all_files = self.csv_file.get_values_from_col(0)
        list_osc = [s for s in all_files if (s[s.rfind('.') + 1:] == "osc" or s[s.rfind('.') + 1:] == "OSC")]
        csv_categories = self.csv_file.get_values_from_col(2)

        spectr_list = []
        features_list = []
        # data_oscs, categories = DataOsc.create_datasets_with_osc(list_osc, csv_categories, augment=True)
        data_oscs, categories = DataOsc.create_datasets_with_osc(list_osc, csv_categories, augment=False)

        max_length = max([len(sublist) for sublist in data_oscs])
        smoothed_signal = []
        for signal in data_oscs:
            current_length = len(signal)

            features = DataOsc.get_math_features(signal)
            features_list.append([features["mean"], features["std_dev"], features["variance"],
                                  features["kurtosis"], features["min_val"], features["max_val"],
                                  features["energy"]])

            # ���� ������ ��� ������ �����, ���������� ���
            if current_length >= max_length:
                smoothed_signal.append(signal)
                # �������� ������ � ���������� ���
                spectrum = fft(signal.copy())
                spectrum_length = len(spectrum)
                spectr_list.append(spectrum)
                continue

            from_spectr = DataOsc.fill_dataset_for_normal_rule_fft(signal, max_length)

            # �������� ������ ����� ���������� � ������ ����� � ��������� ���
            spectrum = fft(from_spectr)
            spectr_list.append(spectrum)

            smoothed_signal.append(from_spectr)


        # plt.plot(range(len(data_oscs[255])), data_oscs[255])
        # plt.plot(range(len(smoothed_signal[1100])), smoothed_signal[1100], 'b')
        # plt.show()

        # np_data_oscs = np.array(padded_data_oscs)
        np_data_oscs = np.array(smoothed_signal)
        np_categories = np.array(categories)
        np_spectr_list = np.array(spectr_list)
        np_features_list = np.array(features_list)
        name = self.csv_file.csv_path[:self.csv_file.csv_path.rfind(".")]
        np.save(f"{name}_values", np_data_oscs)
        np.save(f"{name}_categories", np_categories)
        np.save(f"{name}_spectr", np_spectr_list)
        np.save(f"{name}_features", np_features_list)

    def _on_clicked_item_list(self) -> None:
        """���������� ������� ����� ��� �������� ������ ������"""
        current_item = self.list_files.currentItem()
        # �������� ���� self.current_item_value �� ��������� ���������� �������� ������
        self.current_item_value = current_item.text()
        if (current_item and
                current_item.text()[current_item.text().rfind('.') + 1:] == "osc" or
                current_item.text()[current_item.text().rfind('.') + 1:] == "OSC"):
            self.bttn_open_osc.setEnabled(True)
        else:
            self.bttn_open_osc.setEnabled(False)
            return

    def __open_osc(self, name_osc: str):
        try:
            self.osc_file = Aegis_osc.File_osc(name_osc)
            self.num_osc = self.osc_file.m_sdoHdr.NumOSC
            self.osc_datas = []
            self.start_data_osc = 0
            self.end_data_osc = 10 if self.num_osc > 10 else self.num_osc
            self.osc_datas.extend(self.osc_file.getDotsOSC(0, self.end_data_osc))

            self.plot_layout_h = QHBoxLayout(self)
            self.main_layout_v.addLayout(self.plot_layout_h)
            self.osc_now = 0
            if not hasattr(self, "now_plot"):
                self.now_plot = pg.PlotWidget(self)
                self.plot_layout_h.addWidget(self.now_plot)
                self.now_plot.setStyleSheet("min-height: 250px; max-height: 400px; min-width: 600px")
            self.now_plot.clear()
            self.now_plot.plot(self.osc_datas[self.osc_now])

            # self.plot_layout_h.addWidget(pg.plot(self.osc_datas[self.osc_now]))
            if (not hasattr(self, "bttn_next_osc") and
                    not hasattr(self, "bttn_prev_osc")):
                self.bttn_next_osc = QPushButton("��������� �������������")
                self.bttn_prev_osc = QPushButton("���������� �������������")
                self.bttn_next_osc.clicked.connect(self.open_next_osc)
                self.bttn_prev_osc.clicked.connect(self.open_prev_osc)
                self.main_layout_v.addWidget(self.bttn_next_osc)
                self.main_layout_v.addWidget(self.bttn_prev_osc)
            self.check_next_prev_osc()
        except Exception as e:
            print(f"������ ��� �������� ����� OSC: {e}")

    def __load_next_osc(self):
        if self.osc_now >= self.num_osc - 1:
            return
        # self.osc_datas = []
        # self.start_data_osc = 0
        self.end_data_osc = self.end_data_osc + 500 if (self.num_osc - self.osc_now) > 500 else self.num_osc - 1
        self.osc_datas.extend(self.osc_file.getDotsOSC(0, self.end_data_osc))


    def _on_clicked_bttn_open_osc(self) -> None:
        """���������� ������� ����� ��� ������ �������� ������������"""
        self.__open_osc(self.current_item_value)

    def check_next_prev_osc(self) -> None:
        if self.osc_now + 1 >= self.num_osc:
            self.bttn_next_osc.setEnabled(False)
        elif not self.bttn_next_osc.isEnabled():
            self.bttn_next_osc.setEnabled(True)
        if self.osc_now <= self.start_data_osc:
            self.bttn_prev_osc.setEnabled(False)
        elif not self.bttn_prev_osc.isEnabled():
            self.bttn_prev_osc.setEnabled(True)

    def open_next_osc(self) -> None:
        if self.osc_now >= self.end_data_osc - 1:
            self.__load_next_osc()
            self.check_next_prev_osc()
            if not self.bttn_next_osc.isEnabled():
                return

        self.osc_now += 1
        self.now_plot.clear()
        self.now_plot.plot(self.osc_datas[self.osc_now])
        self.check_next_prev_osc()

    def open_prev_osc(self) -> None:
        if self.osc_now <= self.start_data_osc:
            self.check_next_prev_osc()
            return
        self.osc_now -= 1
        self.now_plot.clear()
        self.now_plot.plot(self.osc_datas[self.osc_now])
        self.check_next_prev_osc()


class My_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menu()

    def create_menu(self):
        self.menu = MainMenu()

        self.setCentralWidget(self.menu)
        self.show()


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication([])
        ex = My_app()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
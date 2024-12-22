import logging
import random

from collections import Counter

import numpy as np

from numpy.fft import ifft, fft

import Aegis_osc

from fourier import Fourier


logger = logging.getLogger(__name__)


class DataOsc:
    def __init__(self):
        pass

    @staticmethod
    def create_datasets_with_osc(list_osc: list
                                 , csv_categories: list
                                 , augment: bool = False) -> (list[list], list[str]):
        """
        ���������� ������ � ��������������� � ���������. ���������� ������������ ������
        """
        try:
            logger.info("Starting create datasets with osc")

            data_oscs = []
            categories = []
            # ���� ��� ���������� ������� ���������� ������������ � ���������
            logger.info("Start get info from files .osc")
            for ind, file_name in enumerate(list_osc):
                osc_file = Aegis_osc.File_osc(file_name)
                num_osc = osc_file.m_sdoHdr.NumOSC
                categories.extend([csv_categories[ind] for _ in range(num_osc)])
                list_osc_data = osc_file.getDotsOSC(0, num_osc)
                data_oscs.extend([list_osc_data[i] for i in range(num_osc)])
            logger.info("end get info from files .osc")

            # ���� ��� �������� ���-�� ������, ����������� � ����� ���������
            counts = Counter(categories)
            delete_el: list[list] = []
            add_el: list[list] = []
            for name in counts:
                part_of_all = counts[name] / len(categories)
                # ���� ������ ����� ��������� ������� �����,
                # �� ���������� ����� ����� ����� ���������
                if part_of_all > 1/len(counts):
                    delete_el.append([name, len(categories) * 0.2])
                    continue

                if augment and part_of_all < 0.2:
                    add_el.append([name, len(categories) * 0.2])

            # ����������� ������� ���� �����������, ���� ����������
            if len(add_el) != 0:
                logger.info("Start augmentation data")
                length_cat = len(categories)
                for a in add_el:
                    count_add = a[1] - counts[a[0]]
                    for i in range(length_cat):
                        if count_add > 1 and categories[i] == a[0]:
                            new_osc = DataOsc.augmentation_on_time_cycle(data_oscs[i])
                            data_oscs.append(new_osc)
                            categories.append(a[0])
                            count_add -= 1
                        elif count_add <= 0:
                            break
                logger.info("End augmentation")

            # ��������� �������, ���� ��� ����������
            if len(delete_el) != 0:
                for d in delete_el:
                    for i in range(len(categories) - 1, -1, -1):
                        if d[1] <= counts[d[0]] and categories[i] == d[0]:
                            categories.pop(i)
                            data_oscs.pop(i)
                            counts[d[0]] -= 1
                        elif d[1] > counts[d[0]]:
                            break

            logger.info("End create datasets with osc")
            return data_oscs, categories
        except Exception as e:
            logger.error(f"Error create dataset from .osc files: %s", e)

    @staticmethod
    def augmentation_on_time_cycle(list_osc: list) -> list:
        """
        ��������� ����������� ����������� ������� �� �������
        """
        augm_list = []
        for osc in list_osc:
            augm_list.append(np.roll(osc, random.randint(5, 50)))
        return  augm_list

    @staticmethod
    def augmentation_on_time(list_osc: list) -> list:
        augm_list = []
        for osc in list_osc:
            shift = random.randint(5, 50)
            augm_list.append(np.roll(osc, shift))
            augm_list[-1][:shift] = 0
        return augm_list

    @staticmethod
    def fill_dataset_for_nulls(signal: list, target_len: int) -> list:
        """�����, ����������� ���� � ����� �������� �� ����������� �����"""
        if len(signal) >= target_len:
            return signal[:target_len]

        fill_len = target_len - len(signal)
        signal.extend([0 for _ in range(fill_len)])
        return signal

    @staticmethod
    def fill_dataset_for_normal_rule_fft(signal: list, target_len: int) -> list | np.ndarray:
        """
        �����, ����������� � ����� ������� ��������, ����������� �� ���.����������
        ��������� 30% �������� ������������, ����� �����������
        �� ���������� �� �������� ���� �� ������������ �������

        ������������ fft ����� ���������� numpy
        """
        if len(signal) >= target_len:
            return signal[:target_len]

        current_length = len(signal)

        # ������������� ������������ �������
        padded_signal = np.zeros(target_len)
        padded_signal[:current_length] = signal.copy()

        # ���������� ��� �� ������ ���������� �������
        mean = np.mean(signal[round(len(signal) * 0.7):])
        std = np.std(signal[round(len(signal) * 0.7):])
        noise = np.random.normal(loc=mean, scale=std, size=target_len - current_length)

        # ��������� ��� � ���������� ����� �������
        padded_signal[current_length:] = noise

        # ��������� � ��������� �������, ����� �������� �������
        spectrum_padded = fft(padded_signal)

        # ��������� �������� �������������� ����� ��� ��������� ������������ �������
        from_spectr = np.real(ifft(spectrum_padded))
        from_spectr[:current_length] = signal
        return from_spectr

    @staticmethod
    def fill_dataset_for_normal_rule_fourier(signal: list, target_len: int) -> list:
        """
        �����, ����������� � ����� ������� ��������, ����������� �� ���.����������
        ��������� 30% �������� ������������, ����� �����������
        �� ���������� �� �������� ���� �� ������������ �������

        ������������ �������������� �����, ������������� �� ��������� ��
        ����� �.�.�������� "���������� �� ���. � �����. �� ��. ������ ��� ����"
        """
        if len(signal) >= target_len:
            return signal[:target_len]

        current_length = len(signal)

        # ������������� ������������ �������
        padded_signal = np.zeros(target_len)
        padded_signal[:current_length] = signal.copy()

        # ���������� ��� �� ������ ���������� �������
        mean = np.mean(signal[round(len(signal) * 0.7):])
        std = np.std(signal[round(len(signal) * 0.7):])
        noise = np.random.normal(loc=mean, scale=std, size=target_len - current_length)

        # ��������� ��� � ���������� ����� �������
        padded_signal[current_length:] = noise

        # ��������� � ��������� �������, ����� �������� �������
        spectrum_padded = Fourier.four2(padded_signal)

        # ��������� �������� �������������� ����� ��� ��������� ������������ �������
        from_spectr = Fourier.four2(spectrum_padded, d=1)
        from_spectr[:current_length] = signal
        return from_spectr

    @staticmethod
    def get_math_features(signal: list) -> dict:
        """����� ������� �������������� ���. ���������� ��� �������"""
        # �������� �������� �� ���. ����������, ������� ����� ������
        # � �������� ��������� ����
        features = {"mean": np.mean(signal), "std_dev": np.std(signal), "variance": np.var(signal),
                    "min_val": np.min(signal), "max_val": np.max(signal)}
        features["kurtosis"] = np.mean((signal - features["mean"]) ** 4) / (features["std_dev"] ** 4)
        features["energy"] = np.sum([i ** 2 for i in signal])
        return features

    @staticmethod
    def get_spectr(signal: list) -> list:
        """ ������� ������ �� ������������� """
        return Fourier.four2(signal, d=-1)

    @staticmethod
    def __get_osc_from_spectr(signal: list, current_length: int) -> list:
        """ ������� ������������� �� ������� """
        return Fourier.four2(signal, d=1)